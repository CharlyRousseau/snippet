from django.urls import URLPattern, path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns: list[URLPattern] = [
    path("", views.snippet_filter_list, name="snippet_filter_list"),
    path("snippet/<int:pk>/", views.snippet_detail, name="snippet_detail"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("for_you/", views.for_you, name="for_you_list"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.update_profile, name="edit_profile"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("generate/", views.generate_snippet, name="generate_snippet"),
    path("liked/", views.liked_snippet_list, name="liked_snippet_list"),
    path("like/<int:snippet_id>/", views.like_snippet, name="like_snippet"),
    path("is_liked/<int:snippet_id>", views.is_snippet_liked, name="is_snippet_liked"),
    path("snippet/delete/<int:pk>", views.delete_snippet, name="delete_snippet"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="reset_password/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="reset_password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="reset_password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="reset_password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

# 4XX/5XX Handling

if not settings.DEBUG:
    urlpatterns += [
        path("test_400/", views.test_400, name="test_400"),
        path("test_403/", views.test_403, name="test_403"),
    ]
