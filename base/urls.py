"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import webapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='authentication/connection_or_inscription.html',
                               redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('flux/', webapp.views.flux, name='flux'),
    path('posts/', webapp.views.posts_by_user, name='posts'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('ticket/create/', webapp.views.create_ticket, name='create_ticket'),
    path('ticket/create/ticket-and-review/', webapp.views.create_ticket_and_review,
         name='create_ticket_and_review'),
    path('ticket/answer/<int:id>', webapp.views.answer_ticket, name='answer_ticket'),
    path('follow-users/', webapp.views.follow_users, name='follow_page'),
    path('follow-users/unfollow/<int:id>', webapp.views.unfollow, name='unfollow'),
    path('ticket/update/<int:id>', webapp.views.update_ticket, name='update_ticket'),
    path('ticket/delete/<int:id>', webapp.views.delete_ticket, name='delete_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
