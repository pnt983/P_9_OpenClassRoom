from django import forms

from authentication.models import User
from . import models


class FollowForm(forms.Form):
    """Form to follow a user"""
    user_to_follow = forms.ModelChoiceField(label='Utilisateur', queryset=User.objects.all())


class TicketForm(forms.ModelForm):
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder': 'Description'}))

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    headline = forms.CharField(label='Titre', widget=forms.TextInput(attrs={'placeholder': 'Titre'}))
    rating = forms.ChoiceField(label='Note', choices=RATING_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': 'd-flex justify-content-between'}))
    body = forms.CharField(label='Commentaire', widget=forms.Textarea(attrs={'placeholder': 'Commentaire'}))

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


class AnswerTicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description']


class UpdateTicketForm(TicketForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description']
