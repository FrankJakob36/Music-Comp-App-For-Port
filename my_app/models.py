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

# === MUSIC COMPOSITION MODEL (New) ===
class Composition(models.Model):
    # Link to the user (optional, so guests could theoretically save if you wanted later)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Title of the track
    title = models.CharField(max_length=200, default="Untitled Beat")
    
    # The JSONField stores the entire song data (e.g., [{"drum": "Kick", "time": 0.5}, ...])
    note_data = models.JSONField(default=list) 
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title