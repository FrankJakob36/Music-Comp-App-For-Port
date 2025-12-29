import json  # <--- Added this to fix the "json is not defined" error
import os
import io

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# ----------- Consolidated Imports -----------
# I combined your duplicate imports here. 
# Note: If 'Post' is not in your models.py, remove it from this list.
# Your main forum uses 'Message', so 'Post' might be a typo in the new function.
from .models import Message, Reply, Composition
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
            return redirect('home') # Changed to redirect to home/greet
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login_page.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login_page')
    
    # Fallback if accessed via GET (though your template now uses POST)
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

def forum_view(request):
    # 1. Check if user is logged in
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access the forums.")
        return redirect('login_page')

    # 2. If logged in, proceed as normal
    posts = Message.objects.all().order_by('-created_at')
    reply_form = ReplyForm()
    
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            msg_id = request.POST.get('message_id')
            
            # --- NEW: Check if msg_id exists before using it ---
            if msg_id: 
                parent = get_object_or_404(Message, id=msg_id)
                reply = reply_form.save(commit=False)
                reply.user = request.user
                reply.message = parent
                reply.save()
                messages.success(request, "Reply posted successfully!")
                return redirect('forum')
            else:
                # If no ID (user didn't click reply on a specific post)
                messages.error(request, "To reply, please click the 'Reply' link on a specific post.")
                # If they were trying to make a NEW post, they should use the other page
    
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
    
    # UPDATED: Allow if user is Author OR Superuser
    if message.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to edit this message.")
        
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, "Message updated successfully.")
            return redirect('forum')
    else:
        form = MessageForm(instance=message)
    return render(request, 'forum/edit_message.html', {'form': form, 'message': message})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # UPDATED: Allow if user is Author OR Superuser
    if message.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to delete this message.")
    
    # If POST request, actually delete
    if request.method == 'POST':
        message.delete()
        messages.success(request, "Message deleted.")
        return redirect('forum')
        
    # If GET request, show confirmation page
    return render(request, 'forum/delete_confirm.html', {'message': message})

# ----------- Composition Views -----------

def save_composition(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            received_notes = data.get('notes', [])
            received_title = data.get('title', 'Untitled Beat')
            user_instance = request.user if request.user.is_authenticated else None

            new_comp = Composition.objects.create(
                user=user_instance,
                title=received_title,
                note_data=received_notes
            )
            return JsonResponse({'status': 'success', 'id': new_comp.id})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# ----------- New / Redundant Views -----------

# This function uses 'Post' instead of 'Message'. 
# If your model is named 'Message', this function will fail unless you rename 'Post' to 'Message'.
def delete_post(request, pk):
    # 1. Get the post object or show 404 if not found
    post = get_object_or_404(Post, pk=pk)

    # 2. If the user clicked "Confirm" (POST request), delete it
    if request.method == "POST":
        post.delete()
        return redirect('forum') # Redirects back to the main forum page

    # 3. If it's a GET request, show the confirmation page
    return render(request, 'forum/delete_confirm.html', {'post': post})

@login_required
def edit_reply(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    
    # Security check: Ensure user owns the reply or is superuser
    if request.user != reply.user and not request.user.is_superuser:
        messages.error(request, "You are not allowed to edit this reply.")
        return redirect('forum') # Redirect back to forum

    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            messages.success(request, "Reply updated successfully!")
            return redirect('forum')
    else:
        form = ReplyForm(instance=reply)

    return render(request, 'forum/edit_reply.html', {'form': form, 'reply': reply})

@login_required
def delete_reply(request, pk):
    reply = get_object_or_404(Reply, pk=pk)

    # Security check
    if request.user != reply.user and not request.user.is_superuser:
        messages.error(request, "You cannot delete this reply.")
        return redirect('forum')

    if request.method == 'POST':
        reply.delete()
        messages.success(request, "Reply deleted.")
        return redirect('forum')

    # Ask for confirmation before deleting
    return render(request, 'forum/delete_confirm.html', {'object': reply})