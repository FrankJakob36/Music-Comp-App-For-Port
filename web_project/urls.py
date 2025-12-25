from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Pages
    path('', views.default_greet, name='home'),                 # Home page
    path('second/', views.second_page, name='second_page'),      # Notes page

    # Authentication
    path('login/', views.login_page, name='login_page'),         # Login page
    path('signup/', views.signup_page, name='signup'),           # Signup page
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Logout

    # Forum
    path('forum/', views.forum_view, name='forum'),
    path('forum/post/', views.post_message, name='post_message'),
    path('forum/reply/<int:message_id>/', views.reply_message, name='reply_message'),
    path('forum/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('forum/delete/<int:message_id>/', views.delete_message, name='delete_message'),

    # Composition
    #path('save/', views.save_composition, name='save_composition'),  # Save composition endpoint
]
