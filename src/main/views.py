from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Listing,LikedListing
from .forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter
from django.contrib import messages 
from importlib import reload
from django.core.mail import send_mail
import logging


def main(request):
    # return HttpResponse("Hello Welocome To Main Page")
    return render(request,"views/main.html")

def domain(request):
    # return HttpResponse("Hello Welocome To Domain Page")
    return render(request,"views/domain.html")

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listings = LikedListing.objects.filter(
        profile=request.user.profile).values_list('listing')
    liked_listings_ids = [l[0] for l in user_liked_listings]
    context = {
        'listing_filter': listing_filter,
        'liked_listings_ids': liked_listings_ids,
    }
    return render(request, "views/home.html", context)


@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST, )
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(
                    request, f'{listing.model} Listing Posted Successfully!')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error(
                request, 'An error occured while posting the listing.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html', {'listing_form': listing_form, 'location_form': location_form, })


@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request, 'views/listing.html', {'listing': listing, })
    except Exception as e:
        messages.error(request, f'Invalid UID {id} was provided for listing.')
        return redirect('home')


@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(
                request.POST, request.FILES, instance=listing)
            location_form = LocationForm(
                request.POST, instance=listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()
                messages.info(request, f'Listing {id} updated successfully!')
                return redirect('home')
            else:
                messages.error(
                    request, f'An error occured while trying to edit the listing.')
                return reload()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
        context = {
            'location_form': location_form,
            'listing_form': listing_form
        }
        return render(request, 'views/edit.html', context)
    except Exception as e:
        messages.error(
            request, f'An error occured while trying to access the edit page.')
        return redirect('home')


@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)

    liked_listing, created = LikedListing.objects.get_or_create(
        profile=request.user.profile, listing=listing)

    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user': created,
    })

logger = logging.getLogger(__name__)  # Initialize a logger for better error handling

@login_required
def inquire_listing_using_email(request, id):
    # Retrieve the listing based on the ID or return a 404 error
    listing = get_object_or_404(Listing, id=id)
    try:
        # Construct the email details
        email_subject = f'{request.user.username} is interested in {listing.model}'
        email_message = (
            f'Hi {listing.seller.user.username},\n\n'
            f'{request.user.username} is interested in your {listing.model} listing on AutoMax.\n\n'
            f'Reply to this email to get in touch with the buyer.'
        )

        # Send the email
        send_mail(
            email_subject,
            email_message,
            'ST.Django.Developer2114@gmail.com',  # Sender's email
            [listing.seller.user.email],  # Recipient's email
            fail_silently=False,  # Do not silently fail to ensure proper error handling
        )

        # Return success response
        return JsonResponse({
            "success": True,
            "message": "Inquiry email sent successfully."
        })

    except Exception as e:
        # Log the exception
        logger.error(f"Error while sending inquiry email: {e}")

        # Return failure response with error details
        return JsonResponse({
            "success": False,
            "error": str(e),  # Serialize the exception to a string
        }, status=500)
#                 send_mail(
#     "AutoMax Testing",
#     "Hello I am the Tester from AutoMax",
#     "ST.Django.Developer2114@gmail.com",
#     ["sahilthorat68@gmail.com"],
#     fail_silently=False,
# )