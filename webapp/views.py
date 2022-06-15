from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from authentication.models import User
from base import settings
from . import forms, models


@login_required
def flux(request):
    following_user_list = []
    user_follow = models.UserFollows.objects.filter(followed_user=request.user)
    for i in user_follow:
        following_user_list.append(i.user.id)
    tickets = models.Ticket.objects.filter(Q(user__in=following_user_list) | Q(user=request.user))
    reviews = models.Review.objects.filter(Q(user__in=following_user_list) | Q(user=request.user))
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
    follow_form = forms.FollowForm(instance=request.user)
    following_user = models.UserFollows.objects.filter(followed_user=request.user).exclude(user=request.user)
    # following_user = test(request)
    followed_user = models.UserFollows.objects.filter(user=request.user).exclude(followed_user=request.user)
    if request.method == 'POST':
        follow_form = forms.FollowForm(request.POST)
        if follow_form.is_valid():
            try:
                form = follow_form.save(commit=False)
                user_follow = models.UserFollows(user=form.followed_user, followed_user=request.user)
                user_follow.save()
                return redirect('follow_page')
            except IntegrityError:
                message = "Vous êtes deja abonné a cet utilisateur"
                print(message)

    return render(request, 'webapp/follow_page.html', context={'form': follow_form,
                                                               'following_user': following_user,
                                                               'followed_user': followed_user})


def test(request):
    print(request.method)
    # t = models.UserFollows.objects.filter(followed_user=request.user)
    # for i in t:
    #     print("i = ", i)
    #     print('i.followed_user = ', i.followed_user)
    #     print('i.user = ', i.user)
    #     print("request = ", request.user)
    # following_user = models.UserFollows.objects.filter(followed_user=request.user).exclude(user=request.user)
    # if request.POST:
    #     t = models.UserFollows.objects.get(followed_user=request.user, user=user_id)
        # t = models.UserFollows.objects.all()
        # print(t)
        # return redirect('follow-page')


