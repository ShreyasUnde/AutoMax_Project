from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from .forms import UserForm,ProfileForm,LocationForm
from main.models import Listing,LikedListing
from django.core.mail import send_mail

def login_view(request):
    if request.method=="POST":
        login_form=AuthenticationForm(request=request,data=request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data.get('username')
            password=login_form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)  
                messages.success(request,f' Hello {username}!! AutoMax Welcomes You To The Car Enthusiastic Community!! ') 
#                 send_mail(
#     "AutoMax Testing",
#     "Hello I am the Tester from AutoMax",
#     "ST.Django.Developer2114@gmail.com",
#     ["sahilthorat68@gmail.com"],
#     fail_silently=False,
# )
                return redirect('home')
            else:
                messages.error(request,f'An error occured while trying to login')
        else:
                messages.error(request,f'An error occured while trying to login')
    elif request.method=="GET":
        login_form=AuthenticationForm()
    return render(request,'views/login.html',{'login_form':login_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


class RegisterView(View):
    def get(self,request):
        register_form=UserCreationForm()
        return render(request,'views/register.html',{'register_form':register_form})

    def post(self,request):
        register_form=UserCreationForm(data=request.POST)
        if register_form.is_valid():
            user=register_form.save()
            user.refresh_from_db()
            login(request,user)
            messages.success(request,f'Hello {user.username} !! You are registerd Successfully!! AutoMax Welcomes You To The Car Enthusiastic Community!!')
     
            return redirect('home')

        else:
            messages.error(request,f'An error occured while trying to login')
            return render(request,'views/register.html',{'register_form':register_form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):  

    def get(self,request):
        user_listings = Listing.objects.filter(seller=request.user.profile)
        user_liked_listings=LikedListing.objects.filter(profile=request.user.profile).all()
        
        user_form=UserForm(instance=request.user)
        profile_form=ProfileForm(instance=request.user.profile)
        location_form=LocationForm(instance=request.user.profile.location)

        context={
            'user_form':user_form,
            'profile_form':profile_form,
            'location_form':location_form,
            'user_listings':user_listings,
            'user_liked_listings':user_liked_listings,

        }
        return render(request,'views/profile.html',context)  
        
    def post(self,request):
        user_form=UserForm(request.POST,instance=request.user)
        user_liked_listings=LikedListing.objects.filter(profile=request.user.profile).all()
     
        profile_form=ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        location_form=LocationForm(request.POST,instance=request.user.profile.location)

        if user_form.is_valid() and profile_form.is_valid()  and location_form.is_valid() : 
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request,f'Profile Updated Successfully!!')
            return redirect('profile')
        else:
            messages.error(request,f'There was an error while updating the profile')

           
        return render(request,'views/profile.html',{'user_form':user_form,'profile_form':profile_form,'location_form':location_form,'user_listings':user_listings,'user_liked_listings':user_liked_listings,})