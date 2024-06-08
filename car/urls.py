from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "car"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.LogOut, name="logout"),    
    path("signup/", views.signup, name="signup"),
    path("profile/", login_required(views.OrderListView.as_view()), name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("car/<int:id>/", views.CarDetailView.as_view(), name="detail"),
    path("car/buy/<int:id>", views.buy, name="buy"),
    path("car/add_comment/<int:car_id>/", views.add_comment, name="add_comment"),
]
