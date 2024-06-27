from django.urls import path
from . import views

urlpatterns = [
    path("", views.snippet_list, name="snippet_list"),
    path("snippet/<int:pk>/", views.snippet_detail, name="snippet_detail"),
    path("signup/", views.signup, name="signup"),
    path("create/", views.create_snippet, name="create_snippet"),
]
