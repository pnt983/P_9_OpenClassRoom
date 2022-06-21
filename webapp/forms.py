from django import forms
from django.contrib.auth import get_user_model

from . import models


# User = get_user_model()
from .models import UserFollows


class FollowForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    headline = forms.CharField(widget=forms.TextInput(attrs={'label': 'Titre', 'placeholder': 'Titre'}))
    rating = forms.ChoiceField(choices=RATING_CHOICES,
                               widget=forms.RadioSelect(attrs={'class': 'd-flex justify-content-between',
                                                               'label': 'Note'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Commentaire'}))

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
