from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser, Message
from .forms import MessageForm

@login_required
def view_profile(request):
    return render(request, 'view_profile.html', {'user': request.user})

@login_required
def chat(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('chat')  # Redirect to the chat page
    else:
        form = MessageForm()
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'chat.html', {
        'form': form,
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request,'home.html')