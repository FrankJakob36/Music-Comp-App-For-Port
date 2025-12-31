from django.contrib import admin
from django.urls import path
from django.conf import settings             # New: Needed for MEDIA_URL
from django.conf.urls.static import static   # New: Needed to serve files
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Pages ---
    path('', views.default_greet, name='home'),
    path('second/', views.second_page, name='second_page'),

    # --- Authentication ---
    path('login/', views.login_page, name='login_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('logout/', views.logout_view, name='logout'),

    # --- Forum Main ---
    path('forum/', views.forum_view, name='forum'),

    # --- Forum Messages (Posts) ---
    path('forum/post/', views.post_message, name='post_message'),
    path('forum/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('forum/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    
    # Specific reply page
    path('forum/reply/<int:message_id>/', views.reply_message, name='reply_message'),

    # --- Forum Replies ---
    path('reply/edit/<int:pk>/', views.edit_reply, name='edit_reply'),
    path('reply/delete/<int:pk>/', views.delete_reply, name='delete_reply'),

    # --- Composition ---
    # UPDATED: Changed 'save/' to 'save-composition/' to match your JavaScript fetch call!
    path('save-composition/', views.save_composition, name='save_composition'),  
]

# --- ADD THIS BLOCK ---
# This is what allows you to hear the files you uploaded while working on your computer.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)