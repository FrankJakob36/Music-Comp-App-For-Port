from django import forms
from .models import Message, Reply

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
