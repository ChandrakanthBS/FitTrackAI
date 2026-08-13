from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('signin/', views.signin_view, name='signin'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('signout/', views.signout_view, name='signout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('visualize/', views.visualization_view, name='visualize'),
    path('workout-lobby/', views.workout_lobby_view, name='workout_lobby'),
    path('reports/', views.reports_view, name='reports'),
    path('reports/export/csv/', views.export_report_csv, name='export_report_csv'),
    path('reports/export/excel/', views.export_report_excel, name='export_report_excel'),
    path('reports/export/json/', views.export_report_json, name='export_report_json'),
    path('reports/export/html/', views.export_report_html, name='export_report_html'),
    path('api/trigger-sos/', views.api_trigger_sos, name='api_trigger_sos'),
    path('api/ai-analyze/', views.api_ai_analyze, name='api_ai_analyze'),
    path('api/chatbot/', views.api_chatbot, name='api_chatbot'),
]

