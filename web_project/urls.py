from django.contrib import admin
from django.urls import path
from my_app import views  # Combined imports into one clean line

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Pages ---
    path('', views.default_greet, name='home'),                      # Home page
    path('second/', views.second_page, name='second_page'),          # Notes page

    # --- Authentication ---
    path('login/', views.login_page, name='login_page'),             # Login page
    path('signup/', views.signup_page, name='signup_page'),          # Signup page
    path('logout/', views.logout_view, name='logout'),               # Logout (Uses your custom view)

    # --- Forum Main ---
    path('forum/', views.forum_view, name='forum'),

    # --- Forum Messages (Posts) ---
    path('forum/post/', views.post_message, name='post_message'),
    path('forum/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('forum/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    
    # Specific reply page (if used separately from the main forum view)
    path('forum/reply/<int:message_id>/', views.reply_message, name='reply_message'),

    # --- Forum Replies (Edit/Delete) ---
    # These match the new functions we added to views.py
    path('reply/edit/<int:pk>/', views.edit_reply, name='edit_reply'),
    path('reply/delete/<int:pk>/', views.delete_reply, name='delete_reply'),

    # --- Composition ---
    # Uncommented because we fixed the view in the previous step
    path('save/', views.save_composition, name='save_composition'),  
]