from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, MessageForm
from .models import CustomUser, Message
from django.http import JsonResponse

@login_required
def view_profile(request):
    return render(request, 'view_profile.html', {'user': request.user})

@login_required
def chat_with_user(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'Message sent'})
            return redirect('chat_with_user', user_id=user_id)
    else:
        form = MessageForm()
    received_messages = Message.objects.filter(receiver=request.user, sender=other_user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user, receiver=other_user).order_by('-timestamp')
    return render(request, 'chat.html', {
        'form': form,
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'other_user': other_user
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
    users = CustomUser.objects.all()
    return render(request, 'home.html', {'users': users})
