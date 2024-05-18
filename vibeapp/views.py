from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, MessageForm
from .models import CustomUser, Message,BlockedUser,VibeMatch
from django.http import JsonResponse
from django.template.loader import render_to_string
import random
from django.db.models import Q

@login_required
def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(CustomUser, pk=user_id)
    blocked_user = get_object_or_404(BlockedUser, blocker=request.user, blocked=user_to_unblock)
    blocked_user.delete()
    return redirect('blocked_users_list')

@login_required
def blocked_users_list(request):
    blocked_users = BlockedUser.objects.filter(blocker=request.user)
    return render(request, 'blocked_users.html', {'blocked_users': blocked_users})
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
    receiver = get_object_or_404(CustomUser, pk=user_id)

    if BlockedUser.objects.filter(Q(blocker=request.user, blocked=receiver) | Q(blocker=receiver, blocked=request.user)).exists():
        return redirect('home')

    vibe_match, created = VibeMatch.objects.get_or_create(
        user1=min(request.user, receiver, key=lambda u: u.id),
        user2=max(request.user, receiver, key=lambda u: u.id)
    )
    if request.method == 'POST' and 'vibe_action' in request.POST:
        action = request.POST.get('vibe_action')
        vibe_match, created = VibeMatch.objects.get_or_create(
            user1=min(request.user, receiver, key=lambda u: u.id), 
            user2=max(request.user, receiver, key=lambda u: u.id)
        )
        
        if vibe_match.user1 == request.user:
            vibe_match.user1_vibe = action == 'vibe_match'
        else:
            vibe_match.user2_vibe = action == 'vibe_match'
        
        vibe_match.check_match()
        
        if action == 'vibe_not_match':
            BlockedUser.objects.get_or_create(blocker=request.user, blocked=receiver)
            return redirect('home')


    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) |
        (Q(sender=receiver) & Q(receiver=request.user))
    ).order_by('timestamp')

    if request.method == 'POST' and 'content' in request.POST:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()

            messages_html = render_to_string('messages_partial.html', {'messages': messages, 'user': request.user})

            if request.is_ajax():
                return JsonResponse({'messages_html': messages_html})

            return redirect('chat_with_user', user_id=user_id)
    elif 'fetch_new' in request.GET:
        messages_html = render_to_string('messages_partial.html', {'messages': messages, 'user': request.user})
        return JsonResponse({'messages_html': messages_html})
    else:
        form = MessageForm()

    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages,
        'form': form,
        'user': request.user,
        'receiver_id': user_id,
        'vibe_match': vibe_match,
        'show_profile': vibe_match.matched
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
