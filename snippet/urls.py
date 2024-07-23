from django.urls import path
from snippet_project.settings import DEBUG
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    path("", views.snippet_filter_list, name="snippet_filter_list"),
    path("snippet/<int:pk>/", views.snippet_detail, name="snippet_detail"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.update_profile, name="edit_profile"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("generate/", views.generate_snippet, name="generate_snippet"),
]

# 4XX/5XX Handling

if not settings.DEBUG:
    urlpatterns += [
        path("test_400/", views.test_400, name="test_400"),
        path("test_403/", views.test_403, name="test_403")
    ]