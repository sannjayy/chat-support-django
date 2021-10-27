from django import forms 
from .models import Chat, ChatSession, ChatTemplate


class ChatTemplateForm(forms.ModelForm):    
    
    class Meta:
        model = ChatTemplate
        fields = ['message', 'image', 'status']
        common_attrs = {'class' : 'form-control'}
        widgets = {
            'message' : forms.Textarea(attrs={**common_attrs, 'placeholder':'Type your message template here', 'rows':'3'}),           
        }
        error_messages = {
            'message' : {'required':'Message is a required field.'},
        }