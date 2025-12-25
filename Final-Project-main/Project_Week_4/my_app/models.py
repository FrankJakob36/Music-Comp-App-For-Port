from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who posted the message
    content = models.TextField()  # Content of the message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the message was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the message was last updated

    def __str__(self):
        return f"Message by {self.user.username} on {self.created_at}"

class Reply(models.Model):
    message = models.ForeignKey(Message, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.created_at}"
