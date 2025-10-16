from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from mysocial_media import settings
from django.core.mail import send_mail

def home(request):
    return render(request, "core/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        # validation
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
            
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numaric!")
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request, "username must be under 10 characters")
            
            
        # Create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "Your Account has been successfully created.")


        #Weclome Email
        subject = "Welcome To DursaTech"
        message = "Hello" + myuser.first_name + "!! \n " + "Welcome To DursaTech!! \n Thank You for visiting our website \n we have also sent you a confirmation email, please confirm your email address inorder to activate your account. \n \n Thank You" 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')
    
    return render(request, "core/signup.html")

def signin(request):

    if request.method =='POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "core/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signin')
    return render(request, "core/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('home')
