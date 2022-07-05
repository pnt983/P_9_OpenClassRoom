from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, CharField, Value, Count
from itertools import chain

from authentication.models import User
from . import forms, models


@login_required
def flux(request):
    following_user_list = []
    users_followed = models.UserFollows.objects.filter(followed_user=request.user)
    for user in users_followed:
        following_user_list.append(user.user)
    following_user_list.append(request.user)
    tickets = models.Ticket.objects.filter(Q(user__in=following_user_list))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    tickets = tickets.annotate(review_number=Count('review'))
    reviews = models.Review.objects.filter(Q(user__in=following_user_list) | Q(ticket__user=request.user))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(tickets, reviews),
                   key=lambda post: post.time_created, reverse=True)
    return render(request, 'webapp/flux.html', context={'posts': posts})


@login_required
def posts_by_user(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = models.Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(tickets, reviews),
                   key=lambda post: post.time_created, reverse=True)
    context = {'posts': posts, 'user_post': True}
    return render(request, 'webapp/posts.html', context=context)


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
    user_following_list = []
    following_user = models.UserFollows.objects.filter(followed_user=request.user).exclude(user=request.user)
    for user in following_user:
        user_following_list.append(user.user.id)
        user_following_list.append(user.followed_user.id)
    followed_user = models.UserFollows.objects.filter(user=request.user).exclude(followed_user=request.user)
    follow_form = forms.FollowForm()
    follow_form.fields['user_to_follow'].queryset = User.objects.exclude(id__in=user_following_list)
    if request.method == 'POST':
        follow_form = forms.FollowForm(request.POST)
        if follow_form.is_valid():
            try:
                user_follow = models.UserFollows(user=follow_form.cleaned_data['user_to_follow'], followed_user=request.user)
                user_follow.save()
                return redirect('follow_page')
            except IntegrityError:
                message = "Vous êtes deja abonné a cet utilisateur"
                print(message)

    return render(request, 'webapp/follow_page.html', context={'form': follow_form,
                                                               'following_user': following_user,
                                                               'followed_user': followed_user})


@login_required
def unfollow(request, id):
    try:
        user = models.UserFollows.objects.get(id=id)
        user.delete()
    except user.DoesNotExist:
        pass
    return redirect('follow_page')


@login_required
def answer_ticket(request, id):
    ticket = models.Ticket.objects.get(id=id)
    form = forms.ReviewForm()
    if request.POST:
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')
    return render(request, 'webapp/answer_ticket.html', context={'ticket': ticket, 'form': form})


@login_required
def update_ticket(request, id):
    ticket = models.Ticket.objects.get(id=id)
    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request, 'webapp/update_ticket.html', context={'form': form})


@login_required
def delete_ticket(request, id):
    if request.method == 'POST':
        ticket = models.Ticket.objects.get(id=id)
        if ticket.user == request.user:
            ticket.delete()
    return redirect('posts')


@login_required
def update_review(request, id):
    review = models.Review.objects.get(id=id)
    ticket = review.ticket
    print('mon print', review.rating)
    form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request, 'webapp/update_review.html', context={'form': form, 'ticket': ticket})


@login_required
def delete_review(request, id):
    if request.method == 'POST':
        review = models.Review.objects.get(id=id)
        if review.user == request.user:
            review.delete()
    return redirect('posts')

