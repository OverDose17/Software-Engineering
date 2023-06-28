from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .forms import  UpdateUserForm, UpdateProfileForm

# Create your views here.
@never_cache
def index(request): # for testing
    return render(request, "index.html")

def dashboard(request):
    # User.objects.all().delete() # to reset database
    return render(request, "dashboard.html")

def about(request):
    return render(request, "about.html")

def SignupPage(request):
    if request.method=='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1 != pass2:
            messages.error(request, 'Your password and confirm password are not Same!!')
            return render (request,'signup.html')
        else:
            my_user = User.objects.create_user(username = uname, email = email, password = pass1, first_name = fname, last_name = lname)
            my_user.save()
            msg_html = render_to_string('success_registration.html', {'uname': uname})
            send_mail(
                "Welcome to Calendar System 2023",
                msg_html,
                "settings.EMAIL_HOST_USER",
                [email],
            )
            messages.success(request, 'Signup Successfully')
            return redirect('users:login')
    return render (request,'signup.html')

def SignupAdmin(request):
    if request.method=='POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            messages.error(request, 'Your password and confirm password are not Same!!')
            return redirect('users:signup')
        else:
            my_user = User.objects.create_user(username = uname, email = email, password = pass1, first_name = fname, last_name = lname, is_superuser = 1, is_staff = 1)
            my_user.save()
            msg_html = render_to_string('success_registration.html', {'uname': uname})
            send_mail(
                "Welcome to Calendar System 2023",
                msg_html,
                "settings.EMAIL_HOST_USER",
                [email],
            )
            messages.success(request, 'Signup Successfully')
            return redirect('users:login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        user=authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request,user)
            messages.success(request, 'Login Successfully')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Username or Password is incorrect!!')
            return render (request,'login.html')
    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    messages.success(request, 'logout success')
    return redirect('users:login')

def changepass(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            pass0=request.POST.get('password0') # old
            pass1=request.POST.get('password1') # new
            pass2=request.POST.get('password2') # confirm
            user=authenticate(request, username=request.user.username, password=pass0)
            if user is None: 
                messages.error(request, 'Please input the right password')
                return render (request,'changepass.html')
            if pass0 == pass1 :
                messages.error(request, 'New password must be different from old password')
                return render (request,'changepass.html')
            elif pass1 != pass2 :
                messages.error(request, 'Confirmation password must match New password')
                return render (request,'changepass.html')
            else:
                messages.success(request, 'password has been successfully changed')
                my_user = User.objects.get(username = request.user.username)
                my_user.set_password(pass1)
                my_user.save()
                msg_html = render_to_string('reset_notification.html', {'uname': request.user.username})
                send_mail(
                    "Password Change Notification",
                    msg_html,
                    "settings.EMAIL_HOST_USER",
                    [request.user.email],
                )
                logout(request) # let user logout automatically
                return redirect('users:login')
        else:
            return render (request,'changepass.html')
    else:
        return redirect("/login") 
    
def subscription(request):
    if request.method == 'POST':
        email = request.POST.get('email') 
        msg_html = render_to_string('subscription_notification.html', {'uname': request.user.username})
        send_mail(
            "Subscription Success Notification",
            msg_html,
            "settings.EMAIL_HOST_USER",
            [email],
        )
        messages.success(request, 'Subscribe Successfully')
        return redirect('users:dashboard')
    return render(request, "dashboard.html")

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Saved Succeed')
                return redirect('users:profile')
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        return redirect("/login") 
    