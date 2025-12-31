from django.db import models
from django.contrib.auth.models import User

# === FORUM MODELS (Existing) ===
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message by {self.user.username} on {self.created_at}"

class Reply(models.Model):
    message = models.ForeignKey(Message, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.created_at}"

# === MUSIC COMPOSITION MODEL (Existing) ===
class Composition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, default="Untitled Beat")
    note_data = models.JSONField(default=list) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# === USER SOUNDS MODEL (New) ===
class UserSound(models.Model):
    # Link the sound to the user who uploaded it
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The name they give the sound (e.g. "My Kick Drum")
    name = models.CharField(max_length=50)
    
    # The actual file. 'upload_to' tells Django which subfolder in 'media' to use.
    audio_file = models.FileField(upload_to='user_samples/')

    def __str__(self):
        return f"{self.name} ({self.user.username})"