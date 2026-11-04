from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed_view, name="feed"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="network/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("user/<str:username>/", views.profile_view, name="profile"),
    path("user/<str:username>/follow/", views.toggle_follow, name="toggle_follow"),
]
