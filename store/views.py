from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from store.forms import UserForm, UserDetailForm, VendorForm, VendorDetailForm
from django.urls import reverse
from .models import Item

def index(request):
    if request.user.is_authenticated and request.user.vendordetail.is_vendor:
        return redirect('vendorDashboard')
    else:
        store_items = Item.objects.all()
        return render(request, 'store/index.html', {'store_items':store_items})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not found !")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'store/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_detail_form = UserDetailForm(request.POST)
        if user_form.is_valid() and user_detail_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = user_detail_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, user_detail_form.errors)
    else:
        user_form = UserForm()
        user_detail_form = UserDetailForm()
    return render(request,'store/signup.html',
                          {'user_form':user_form,
                           'user_detail_form':user_detail_form,
                           'registered':registered})

def vendorlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        vendor = authenticate(username=username, password=password)
        if vendor:
            if vendor.is_active:
                login(request,vendor)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not found !")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'store/vendor/login.html')

def vendorsignup(request):
    registered = False
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST)
        vendor_detail_form = VendorDetailForm(request.POST)
        if vendor_form.is_valid() and vendor_detail_form.is_valid():
            vendor = vendor_form.save()
            vendor.set_password(vendor.password)
            vendor.save()
            profile = vendor_detail_form.save(commit=False)
            profile.vendor = vendor
            profile.save()
            registered = True
        else:
            print(vendor_form.errors, vendor_detail_form.errors)
    else:
        vendor_form = VendorForm()
        vendor_detail_form = VendorDetailForm()
    return render(request,'store/vendor/signup.html',
                          {'vendor_form':vendor_form,
                           'vendor_detail_form':vendor_detail_form,
                           'registered':registered})

@login_required
def vendorDashboard(request):
    return render(request, 'store/vendor/dashboard.html')