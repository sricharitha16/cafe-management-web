from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ...
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/thank-you/', views.feedback_thank_you, name='feedback_thank_you'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu, name='menu'),
    path('items/', views.item, name='item'),
    path('about/', views.about, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset-question/', views.password_reset_question, name='password_reset_question'),
    path('security-question-answer/', views.security_question_answer, name='security_question_answer'),
    path('password-reset-form/<int:user_id>/', views.password_reset_form, name='password_reset_form'),
    path('register/', views.register, name='register'),
    path('event_list', views.event_list, name='event_list'),
    path('redirect', views.redirect, name='redirect'),
    path('<int:event_id>/signup/', views.event_signup, name='event_signup'),
    path('<int:event_id>/unsignup/', views.event_unsignup, name='event_unsignup'),
    path('create_event/', views.create_event, name='create_event')
    
    
]
