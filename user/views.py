from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from core.models import UserProfile
# Create your views here.
def myregister(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            htmly = get_template('user/email.html')
            d = {'username':username}
            subject, from_email, to = 'Welcome', 'namanmonga27@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

            profile = UserProfile()
            profile.user = user
            profile.fname = fname
            profile.lname = lname
            profile.save()

            messages.success(request, 'Your Account has been successfully created!')
            return redirect('login')
    context = {'form':form}
    return render(request, 'user/signup.html', context)

def mylogin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request,user)
            messages.success(request, 'welcome to the forum clone!')
            return redirect('home')
        else:
            messages.error(request, "your account doesn't exist yet, noob!")

    return render(request, 'user/login.html', {'form':form})