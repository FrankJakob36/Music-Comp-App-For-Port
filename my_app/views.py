import json
import os
import io

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from .models import Message, Reply
from .forms import MessageForm, ReplyForm

# ----------- Public Views -----------

def default_greet(request):
    return render(request, 'greet.html')

def second_page(request):
    return render(request, 'second_page.html')

# ----------- Authentication Views -----------

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login_page.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_page')

def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login_page')
    else:
        form = UserCreationForm()
    return render(request, 'signup_page.html', {'form': form})

# ----------- Forum Views -----------

@login_required
def forum_view(request):
    posts = Message.objects.all().order_by('-created_at')
    reply_form = ReplyForm()
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            msg_id = request.POST.get('message_id')
            parent = get_object_or_404(Message, id=msg_id)
            reply = reply_form.save(commit=False)
            reply.user = request.user
            reply.message = parent
            reply.save()
            messages.success(request, "Reply posted successfully!")
            return redirect('forum')
    return render(request, 'forum/forum.html', {
        'posts': posts,
        'reply_form': reply_form,
    })

@login_required
def post_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()
            messages.success(request, "Message posted successfully!")
            return redirect('forum')
    else:
        form = MessageForm()
    return render(request, 'forum/create_message.html', {'form': form})

@login_required
def reply_message(request, message_id):
    parent_message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.message = parent_message
            reply.save()
            messages.success(request, "Reply posted successfully!")
            return redirect('forum')
    else:
        form = ReplyForm()
    return render(request, 'forum/reply_message.html', {
        'form': form,
        'parent_message': parent_message
    })

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.user != request.user:
        messages.error(request, "You don't have permission to edit this message.")
        return redirect('forum')
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, "Message updated successfully.")
            return redirect('forum')
    else:
        form = MessageForm(instance=message)
    return render(request, 'forum/edit_message.html', {'form': form})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.user == request.user:
        message.delete()
        messages.success(request, "Message deleted.")
    else:
        messages.error(request, "You cannot delete someone else’s message.")
    return redirect('forum')

# ----------- Composition Views -----------

#@csrf_exempt
#def save_composition(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            composition = data.get('composition', [])
            print("Received composition:", composition)
            # Here you can save it to a database if you want
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
