from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary (Little or no exercise)'),
        ('light', 'Lightly Active (Exercise 1-3 days/week)'),
        ('moderate', 'Moderately Active (Exercise 3-5 days/week)'),
        ('active', 'Very Active (Exercise 6-7 days/week)'),
        ('extra_active', 'Extra Active (Hard exercise / physical job)'),
    ]

    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss / Fat Burn'),
        ('maintenance', 'Maintain Weight & Fitness'),
        ('muscle_gain', 'Muscle Gain / Build Strength'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    sos_contact = models.CharField(max_length=100, help_text="Email or Phone Number for SOS Emergency")
    age = models.PositiveIntegerField(default=25)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Male')
    height_cm = models.FloatField(help_text="Height in cm", default=170.0)
    weight_kg = models.FloatField(help_text="Weight in kg", default=70.0)
    
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='moderate')
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='weight_loss')
    
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Target Goals (If set to 0, system auto-calculates based on BMR/TDEE and Goal)
    daily_calorie_target = models.PositiveIntegerField(default=0, help_text="Custom Daily Calorie Target (kcal)")
    daily_calorie_burn_target = models.PositiveIntegerField(default=0, help_text="Custom Daily Active Calorie Burn Goal (kcal)")
    daily_protein_target = models.FloatField(default=0.0, help_text="Custom Daily Protein Goal (g)")

    @property
    def bmi(self):
        if self.height_cm and self.height_cm > 0:
            height_m = self.height_cm / 100.0
            return round(self.weight_kg / (height_m ** 2), 1)
        return 0.0

    @property
    def bmi_category(self):
        val = self.bmi
        if val < 18.5:
            return "Underweight"
        elif 18.5 <= val < 25.0:
            return "Normal"
        elif 25.0 <= val < 30.0:
            return "Overweight"
        else:
            return "Obese"

    @property
    def bmr(self):
        # Mifflin-St Jeor Equation
        w = self.weight_kg or 70.0
        h = self.height_cm or 170.0
        a = self.age or 25
        if self.gender == 'Male':
            return round((10 * w) + (6.25 * h) - (5 * a) + 5)
        elif self.gender == 'Female':
            return round((10 * w) + (6.25 * h) - (5 * a) - 161)
        else:
            return round((10 * w) + (6.25 * h) - (5 * a) - 78)

    @property
    def tdee(self):
        multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'extra_active': 1.9,
        }
        mult = multipliers.get(self.activity_level, 1.55)
        return round(self.bmr * mult)

    @property
    def recommended_daily_calories(self):
        base_tdee = self.tdee
        if self.goal == 'weight_loss':
            return max(1200, base_tdee - 500)
        elif self.goal == 'muscle_gain':
            return base_tdee + 400
        else:
            return base_tdee

    @property
    def recommended_daily_burn(self):
        burn_map = {
            'sedentary': 250,
            'light': 350,
            'moderate': 450,
            'active': 550,
            'extra_active': 650,
        }
        base_burn = burn_map.get(self.activity_level, 400)
        if self.goal == 'weight_loss':
            base_burn += 100
        return base_burn

    @property
    def recommended_daily_protein(self):
        w = self.weight_kg or 70.0
        if self.goal == 'muscle_gain':
            return round(w * 2.0, 1)
        elif self.goal == 'weight_loss':
            return round(w * 1.8, 1)
        else:
            return round(w * 1.5, 1)

    def get_daily_calorie_target(self):
        if self.daily_calorie_target and self.daily_calorie_target > 0:
            return self.daily_calorie_target
        return None

    def get_daily_calorie_burn_target(self):
        if self.daily_calorie_burn_target and self.daily_calorie_burn_target > 0:
            return self.daily_calorie_burn_target
        return None

    def get_daily_protein_target(self):
        if self.daily_protein_target and self.daily_protein_target > 0:
            return round(self.daily_protein_target, 1)
        return None

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return None

    def __str__(self):
        return f"Profile of {self.user.email} - BMI: {self.bmi} ({self.bmi_category})"



class FoodLog(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_logs')
    food_name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField()
    protein = models.FloatField(default=0.0)
    carbs = models.FloatField(default=0.0)
    fats = models.FloatField(default=0.0)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES, default='Breakfast')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.food_name} ({self.calories} kcal) - {self.user.username}"


class ExerciseLog(models.Model):
    CATEGORY_CHOICES = [
        ('Cardio', 'Cardio / Running'),
        ('HIIT', 'HIIT Workout'),
        ('Strength', 'Strength Training'),
        ('Yoga', 'Yoga & Flexibility'),
        ('Sports', 'Outdoor Sports'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_logs')
    exercise_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Cardio')
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    calories_burned = models.PositiveIntegerField(help_text="Estimated calories burned")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.exercise_name} ({self.duration_minutes} mins, {self.calories_burned} kcal) - {self.user.username}"
