from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from core.models import UserProfile, FoodLog, ExerciseLog

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='Password123!',
            first_name='Test',
            last_name='User'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            sos_contact='9998887776',
            age=30,
            gender='Male',
            height_cm=180.0,
            weight_kg=80.0,
            activity_level='moderate',
            goal='weight_loss'
        )

    def test_bmi_and_bmr_calculation(self):
        # BMI = 80 / (1.8^2) = 24.69 -> 24.7 (Normal)
        self.assertEqual(self.profile.bmi, 24.7)
        self.assertEqual(self.profile.bmi_category, "Normal")
        
        # BMR (Male) = 10*80 + 6.25*180 - 5*30 + 5 = 800 + 1125 - 150 + 5 = 1780
        self.assertEqual(self.profile.bmr, 1780)
        
        # TDEE = 1780 * 1.55 = 2759
        self.assertEqual(self.profile.tdee, 2759)
        
        # Un-set targets return None (so frontend displays --)
        self.assertIsNone(self.profile.get_daily_calorie_target())
        self.assertIsNone(self.profile.get_daily_protein_target())

    def test_profile_view_and_edit(self):
        client = Client()
        client.login(username='testuser@example.com', password='Password123!')
        
        response = client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile & Daily Targets')
        
        # Edit profile POST with 2 custom targets (Calorie & Protein)
        post_data = {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'updated@example.com',
            'sos_contact': '1112223334',
            'age': 32,
            'gender': 'Male',
            'height_cm': 185.0,
            'weight_kg': 82.0,
            'activity_level': 'active',
            'goal': 'muscle_gain',
            'daily_calorie_target': 3000,
            'daily_calorie_burn_target': 400,
            'daily_protein_target': 180.0
        }
        res = client.post(reverse('profile'), post_data)
        self.assertEqual(res.status_code, 302)
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.get_daily_calorie_target(), 3000)
        self.assertEqual(self.profile.get_daily_protein_target(), 180.0)

    def test_remove_profile_photo(self):
        client = Client()
        client.login(username='testuser@example.com', password='Password123!')
        
        # Test photo remove post
        res = client.post(reverse('profile'), {'remove_picture': '1'})
        self.assertEqual(res.status_code, 302)
        
        self.profile.refresh_from_db()
        self.assertFalse(bool(self.profile.profile_picture))

    def test_dashboard_recommendations(self):
        client = Client()
        client.login(username='testuser@example.com', password='Password123!')
        
        response = client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Daily Goals & Recommendation Center')
        self.assertContains(response, 'Daily Protein Goal')

    def test_daily_target_reset_on_new_day(self):
        client = Client()
        client.login(username='testuser@example.com', password='Password123!')

        from datetime import timedelta

        # Create food log and exercise log from YESTERDAY
        yesterday = timezone.now() - timedelta(days=1)
        fl = FoodLog.objects.create(
            user=self.user,
            food_name='Yesterday Meal',
            calories=800,
            protein=40.0,
            carbs=90.0,
            fats=20.0
        )
        FoodLog.objects.filter(pk=fl.pk).update(created_at=yesterday)

        ex = ExerciseLog.objects.create(
            user=self.user,
            exercise_name='Yesterday Workout',
            category='Cardio',
            duration_minutes=45,
            calories_burned=400
        )
        ExerciseLog.objects.filter(pk=ex.pk).update(created_at=yesterday)

        response = client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        # Today's daily target counters must be 0
        self.assertEqual(response.context['total_calories'], 0)
        self.assertEqual(response.context['total_protein'], 0.0)
        self.assertEqual(response.context['total_burned'], 0)

    def test_api_trigger_sos(self):
        client = Client()
        client.login(username='testuser@example.com', password='Password123!')
        
        res = client.post(
            reverse('api_trigger_sos'),
            data={'latitude': 37.7749, 'longitude': -122.4194},
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('SOS Emergency Alert', data.get('message', ''))

    def test_api_chatbot(self):
        client = Client()
        client.login(username='testuser@example.com', password='Password123!')
        
        # Test macro inquiry
        res = client.post(
            reverse('api_chatbot'),
            data={'message': 'What are my remaining calories and protein?'},
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('Macro Telemetry Summary', data.get('reply', ''))

        # Test food recommendation inquiry
        res2 = client.post(
            reverse('api_chatbot'),
            data={'message': 'Recommend a meal for lunch'},
            content_type='application/json'
        )
        self.assertEqual(res2.status_code, 200)
        data2 = res2.json()
        self.assertEqual(data2.get('status'), 'success')
        self.assertIn('Recommendations', data2.get('reply', ''))

        # Test user info / profile query
        res3 = client.post(
            reverse('api_chatbot'),
            data={'message': 'Tell me about my profile and stats'},
            content_type='application/json'
        )
        self.assertEqual(res3.status_code, 200)
        data3 = res3.json()
        self.assertEqual(data3.get('status'), 'success')
        self.assertIn('User Profile & Biometric Card', data3.get('reply', ''))
        self.assertIn('24.7', data3.get('reply', ''))  # Calculated BMI in setUp

        # Test conversational greeting
        res4 = client.post(
            reverse('api_chatbot'),
            data={'message': 'Hello'},
            content_type='application/json'
        )
        self.assertEqual(res4.status_code, 200)
        data4 = res4.json()
        self.assertEqual(data4.get('status'), 'success')
        self.assertIn('Hello', data4.get('reply', ''))

        # Test science/health query (creatine & supplements)
        res5 = client.post(
            reverse('api_chatbot'),
            data={'message': 'Tell me about creatine supplements'},
            content_type='application/json'
        )
        self.assertEqual(res5.status_code, 200)
        data5 = res5.json()
        self.assertEqual(data5.get('status'), 'success')
        self.assertIn('Supplement Science', data5.get('reply', ''))





