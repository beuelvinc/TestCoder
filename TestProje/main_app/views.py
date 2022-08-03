from django.shortcuts import render, redirect
from .models import Product, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    """Home render"""

    return render(request, "index.html")


def privacy(request):
    """Privacy"""

    return render(request, "privacy.html")


def login(request):
    """Login"""

    return redirect("/accounts/login/")


@login_required
def logout(request):
    """Logout"""
    return redirect("/accounts/logout/")


@login_required
def products(request):
    """
    This function opens list of products
    @param : request:  request type data
    """
    objects = Product.objects.all()
    if request.method == "GET" and request.GET.get('q'):  # search by fields
        query = request.GET.get("q")
        objects = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if request.user.is_staff:
        return render(request, "products.html", {"staff": True, "products": objects})

    return render(request, "products.html", {"staff": False, "products": objects})


@login_required
def create_user(request):
    """
    This function creates a user
    @param : request:  request type data
    """
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('/')

    else:
        f = CustomUserCreationForm()

    return render(request, 'user_create.html', {'form': f})


@login_required
def edit_profile(request):
    """
    This function updates user's profile
    @param : request:  request type data
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == "POST":
        update_user_form = UserForm(data=request.POST, instance=request.user)
        update_profile_form = UserProfileForm(
            data=request.POST, instance=user_profile)

        if update_user_form.is_valid() and update_profile_form.is_valid():

            user = update_user_form.save()
            profile = update_profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            messages.success(request, 'Profile Updated successfully')

        else:
            print(update_user_form.errors, update_profile_form.errors)
    else:
        update_user_form = UserForm()
        update_profile_form = UserProfileForm(instance=user_profile)

    return render(request,
                  'edit_profile.html',
                  {'update_user_form': update_user_form,
                      'update_profile_form': update_profile_form}
                  )


@login_required
def my_profile(request):
    """
    This function opens user's profile
    @param : request:  request type data
    """
    try:
        user_obj = User.objects.get(id=request.user.id)

    except User.DoesNotExist:
        user_obj = None

    try:
        user_profile = UserProfile.objects.get(user=request.user)

    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request,
                  'my_profile.html',
                  {'user_obj': user_obj, 'user_profile': user_profile}
                  )


@login_required
def product_detail(request, id):
    """
    This function opens a product
    @param : request:  request type data
    @param :id: int 
    """
    obj = Product.objects.get(id=id)

    if request.user.is_staff:
        return render(request, "product_detail.html", {"editable": True, "product": obj})

    if obj.created_by == request.user:
        editable = True
    else:
        editable = False

    return render(request, "product_detail.html", {"editable": editable, "product": obj})


@login_required
def edit_product(request, id):
    """
    This function updates a product
    @param : request:  request type data
    @param :id: int 
    """
    obj = Product.objects.get(id=id)

    if request.user.is_staff or obj.created_by == request.user:
        form = ProductForm(request.POST or None, instance=obj)

        context = {}
        if form.is_valid():
            form.save()
            return redirect("main:product_detail", str(id))

        # add form dictionary to context
        context["form"] = form

        return render(request, "edit_product.html", context)

    return render(request, "edit_product.html", {"editable": editable, "product": obj})


@login_required
def create_product(request):
    """
    This function creates a product
    @param : request:  request type data
    """
    # dictionary for initial data with
    context = {}

    # add the dictionary during initialization
    form = ProductFormCreate(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.created_by = request.user

            if 'image_product' in request.FILES:
                checkout.image_product = request.FILES['image_product']

            checkout.save()

        context['form'] = form
        messages.success(request, "Created Successfully")
        return redirect('main:product_page')
    else:
        context['form'] = form
        return render(request, "create_product.html", context)
