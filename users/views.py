from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .forms import RegistrationForm, LoginForm, EventForm
from .models import Event, Feedback, Profile, Item


def home(request):
	events = Event.objects.all()
	return render(request, 'home.html', {'events': events})

def contact(request):
    return render(request, 'contact.html')

def menu(request):
    return render(request, 'menu.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def password_reset_question(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            request.session['user_id'] = user.id  # Store user ID in session
            return render(request, 'security_question.html', {'question': profile.security_question})
        except User.DoesNotExist:
            messages.error(request, 'Username not found')
            return redirect('password_reset_question')

    return render(request, 'password_reset_question.html')

def security_question_answer(request):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        user_id = request.session.get('user_id')
        if user_id:
            profile = Profile.objects.get(user_id=user_id)
            if check_password(answer, profile.security_answer):
                # Redirect to reset password page
                return redirect('password_reset_form', user_id=user_id)
            else:
                messages.error(request, 'Incorrect answer')
                return redirect('password_reset_question')

    return render(request, 'security_question.html')

def password_reset_form(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect('login')  # Redirect to the login page or any other appropriate page

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'password_reset_form.html', {'user_id': user_id})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_signup(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.participants.add(request.user)
        return render(request, 'redirect.html')
    
def item(request):
    item = Item.objects.all()
    return render(request, 'item.html', {'items': item})


def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Create and save the feedback object
        feedback = Feedback(name=name, email=email, message=message)
        feedback.save()

        return redirect('feedback_thank_you')  # Redirect to a thank you page or similar
    
    return render(request, 'feedback.html')

def feedback_thank_you(request):
    return render(request, 'feedback_thank_you.html')

def event_unsignup(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.participants.remove(request.user)
        return render(request, 'home.html')

@login_required
def create_event(request):
    if not request.user.groups.filter(name='organisers').exists():
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})
