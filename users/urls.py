from django.urls import path
from . import views

urlpatterns = [

    # Authentication
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    # User Management
    path(
        "users/",
        views.user_list,
        name="user_list"
    ),

    path(
        "users/add/",
        views.user_add,
        name="user_add"
    ),

    path(
        "users/<int:pk>/edit/",
        views.user_edit,
        name="user_edit"
    ),

    path(
        "users/<int:pk>/reset-password/",
        views.reset_password,
        name="reset_password"
    ),

]