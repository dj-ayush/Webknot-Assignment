from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Event, Registration
from .forms import AdminLoginForm, EventForm, UserRegistrationForm, UserEventRegistrationForm
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def adminlogin_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid admin credentials.")
    else:
        form = AdminLoginForm()

    return render(request, 'adminlogin.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email notification (optional)
        try:
            send_mail(
                f'Contact Form Message from {name}',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Send to yourself
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
        except:
            messages.success(request, 'Thank you for your message!')
        
        return redirect('contact')
    
    return render(request, 'contact.html')

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def home(request):
    sports_events = Event.objects.filter(category='Sports')
    cultural_events = Event.objects.filter(category='Cultural')
    gaming_events = Event.objects.filter(category='Gaming')
    return render(request, 'home.html', {
        'sports_events': sports_events,
        'cultural_events': cultural_events,
        'gaming_events': gaming_events
    })

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    events = Event.objects.all()
    total_registrations = Registration.objects.count()

    if request.method == 'POST':
        if 'delete_event' in request.POST:
            event_id = request.POST.get('delete_event')
            event_to_delete = get_object_or_404(Event, id=event_id)
            event_to_delete.delete()
            messages.success(request, "Event deleted successfully.")
            return redirect('admin_dashboard')

        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('admin_dashboard')
    else:
        form = EventForm()

    return render(request, 'admin_dashboard.html', {
        'form': form,
        'events': events,
        'total_registrations': total_registrations,
    })

@login_required
@user_passes_test(is_superuser)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('admin_dashboard')

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if user already registered for this event
    existing_registration = Registration.objects.filter(event=event, user=request.user).first()
    if existing_registration:
        messages.warning(request, "You are already registered for this event.")
        return redirect('home')

    if request.method == 'POST':
        form = UserEventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        # Pre-fill with user data
        initial_data = {
            'name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'email': request.user.email
        }
        form = UserEventRegistrationForm(initial=initial_data)

    return render(request, 'event_reg.html', {'form': form, 'event': event})

@login_required
@user_passes_test(is_superuser)
def event_registrations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event)
    data = {
        "registrations": [
            {"name": reg.name, "email": reg.email, "phone": reg.phone} for reg in registrations
        ]
    }
    return JsonResponse(data)

@login_required
def manage_registrations(request):
    user_registrations = Registration.objects.filter(user=request.user)
    return render(request, 'manage_reg.html', {'registrations': user_registrations})

@login_required
def delete_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    registration.delete()
    messages.success(request, "Registration deleted successfully.")
    return redirect('manage_registrations')