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
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

