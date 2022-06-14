from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from authentication.models import User
from base import settings
from . import forms, models


@login_required
def flux(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(request, 'webapp/flux.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def posts_by_user(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    return render(request, 'webapp/posts.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    return render(request, 'webapp/create_ticket.html', context={'form': form})


@login_required
def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('flux')
    context = {'ticket_form': ticket_form, 'review_form': review_form}
    return render(request, 'webapp/create_ticket_and_review.html', context=context)


@login_required
def follow_users(request):
    follow_form = forms.FollowForm()
    if request.method == 'POST':
        follow_form = forms.FollowForm(request.POST)
        if follow_form.is_valid():
            form = follow_form.save(commit=False)
            print('mon print', form)
            user_follow = models.UserFollows(user=form.followed_user, followed_user=request.user)
            user_follow.save()
            print('mon print', user_follow)
            return redirect('follow_page')
    return render(request, 'webapp/follow_page.html', context={'form': follow_form})

