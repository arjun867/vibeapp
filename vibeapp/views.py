from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, MessageForm
from .models import CustomUser, Message,BlockedUser
from django.http import JsonResponse
import random
from django.db.models import Q

@login_required
def suggest_user(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    if users.exists():
        suggested_user = random.choice(users)
        return redirect('chat_with_user', user_id=suggested_user.id)
    else:
        return redirect('home')
    
@login_required
def recent_chats(request):
    recent_messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
    recent_chatted_users = set()
    for message in recent_messages:
        if message.sender == request.user:
            recent_chatted_users.add(message.receiver)
        else:
            recent_chatted_users.add(message.sender)
    
    return render(request, 'recent_chats.html', {'recent_chatted_users': recent_chatted_users})

@login_required
def view_profile(request):
    return render(request, 'view_profile.html', {'user': request.user})

@login_required
def block_user(request, user_id):
    user_to_block = CustomUser.objects.get(pk=user_id)
    BlockedUser.objects.create(blocker=request.user, blocked=user_to_block)
    return redirect('home')

@login_required
def chat_with_user(request, user_id):
    receiver = CustomUser.objects.get(pk=user_id)
    if BlockedUser.objects.filter(blocker=request.user, blocked=receiver).exists() or BlockedUser.objects.filter(blocker=receiver, blocked=request.user).exists():
        return redirect('home')  # Or handle this case appropriately
    
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) |
        (Q(sender=receiver) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('chat_with_user', user_id=user_id)
    else:
        form = MessageForm()
    
    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages,
        'form': form,
        'user': request.user,
        'receiver_id': user_id
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
    users = CustomUser.objects.exclude(id=request.user.id)
    user_ids = [user.id for user in users]
    return render(request, 'home.html', {'user_ids': user_ids})
