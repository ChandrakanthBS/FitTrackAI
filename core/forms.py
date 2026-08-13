import re
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, FoodLog, ExerciseLog

class CustomRegisterForm(forms.Form):
    GENDER_CHOICES = UserProfile.GENDER_CHOICES
    ACTIVITY_CHOICES = UserProfile.ACTIVITY_CHOICES
    GOAL_CHOICES = UserProfile.GOAL_CHOICES

    first_name = forms.CharField(
        label="First Name",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label="Last Name",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'name@example.com'})
    )
    sos_contact = forms.CharField(
        label="SOS Email / Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Emergency Email or Mobile Number'})
    )
    age = forms.IntegerField(
        label="Age",
        min_value=1,
        max_value=120,
        initial=25,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 25'})
    )
    gender = forms.ChoiceField(
        label="Gender",
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    height_cm = forms.FloatField(
        label="Height (cm)",
        min_value=50.0,
        max_value=250.0,
        initial=170.0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 175'})
    )
    weight_kg = forms.FloatField(
        label="Weight (kg)",
        min_value=20.0,
        max_value=300.0,
        initial=70.0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 70'})
    )
    activity_level = forms.ChoiceField(
        label="Activity Level",
        choices=ACTIVITY_CHOICES,
        initial='moderate',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    goal = forms.ChoiceField(
        label="Fitness Goal",
        choices=GOAL_CHOICES,
        initial='weight_loss',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'At least 8 chars, 1 number, 1 special char'})
    )
    confirm_password = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Repeat your password'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number (0-9).")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\/;]', password):
            raise forms.ValidationError("Password must contain at least one special character (e.g. !@#$%^&*).")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. John'})
    )
    last_name = forms.CharField(
        label="Last Name",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Doe'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'name@example.com'})
    )

    class Meta:
        model = UserProfile
        fields = [
            'sos_contact', 'age', 'gender', 'height_cm', 'weight_kg',
            'activity_level', 'goal', 'daily_calorie_target',
            'daily_calorie_burn_target', 'daily_protein_target', 'profile_picture'
        ]
        widgets = {
            'sos_contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Emergency Contact Email / Phone'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '25'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'height_cm': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '170.0'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '70.0'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
            'goal': forms.Select(attrs={'class': 'form-select'}),
            'daily_calorie_target': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 2000 (0 for --)'}),
            'daily_calorie_burn_target': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 400 (0 for --)'}),
            'daily_protein_target': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 120 (0 for --)'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
        }



class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your registered Email ID'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your password'})
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your registered Email ID'})
    )

class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        fields = ['food_name', 'calories', 'protein', 'carbs', 'fats', 'meal_type']
        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Search or enter food (e.g. Chicken Biryani, Paneer, Dosa)...', 'list': 'foodOptionsDatalist'}),
            'calories': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 520'}),
            'protein': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Protein (g)'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Carbs (g)'}),
            'fats': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Fats (g)'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
        }

class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['exercise_name', 'category', 'duration_minutes', 'calories_burned']
        widgets = {
            'exercise_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Outdoor Running / HIIT'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Duration (minutes)'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Calories Burned (kcal)'}),
        }
