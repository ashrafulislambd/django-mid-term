from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, ListView


from .forms import SignupForm, EditProfileForm, CommentForm
from brand.models import Brand
from .models import Car, Order, Comment

def index(request):
    brands = Brand.objects.all()
    if "brand_id" not in request.GET: 
        cars = Car.objects.all()
    else:
        brand_id = request.GET["brand_id"]
        cars = Car.objects.filter(brand__id = brand_id)
    return render(request, "car/index.html", {
        "brands": brands,
        "cars": cars,
    })

def LogOut(request):
    logout(request)
    return redirect(reverse("car:index"))

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, message="Successfully created user")
    else:
        form = SignupForm()
    return render(request, "car/signup.html", {"form": form})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("car:profile")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "car/edit_profile.html", {"form": form})

def buy(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse("car:detail", args=(id,)))
    if request.method == "POST":
        car = get_object_or_404(Car, pk=id)
        if car.quantity > 0:
            car.quantity = F("quantity") - 1
            car.save()

            order = Order(user=request.user, car=car)
            order.save()
        return redirect(reverse("car:detail", args=(id,)))
    
def add_comment(request, car_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            car = get_object_or_404(Car, pk=car_id)
            form.instance.car = car
            form.save()
            return redirect(reverse("car:detail", args=(car_id,)))

class UserLoginView(LoginView):
    def get_success_url(self):
        return reverse("car:index")
    
    template_name = "car/login.html"

class CarDetailView(DetailView):
    model = Car
    pk_url_kwarg = "id"
    template_name = "car/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.all()
        context["comment_form"] =  CommentForm()
        context["comments"] = comments
        return context
    

class OrderListView(ListView):
    model = Order
    template_name = "car/profile.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by("-time")

