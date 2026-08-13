from django.contrib import admin
from .models import UserProfile, FoodLog, ExerciseLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'sos_contact', 'age', 'gender', 'height_cm', 'weight_kg', 'get_bmi', 'get_bmi_category')
    search_fields = ('user__username', 'user__email', 'sos_contact')
    list_filter = ('gender',)

    def get_bmi(self, obj):
        return obj.bmi
    get_bmi.short_description = 'BMI Score'

    def get_bmi_category(self, obj):
        return obj.bmi_category
    get_bmi_category.short_description = 'BMI Category'


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'user', 'meal_type', 'calories', 'protein', 'carbs', 'fats', 'created_at')
    list_filter = ('meal_type', 'created_at')
    search_fields = ('food_name', 'user__username', 'user__email')


@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('exercise_name', 'user', 'category', 'duration_minutes', 'calories_burned', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('exercise_name', 'user__username', 'user__email')
