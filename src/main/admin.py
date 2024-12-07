from django.contrib import admin
from .models import Listing,LikedListing
class ListingAdmin(admin.ModelAdmin):
    readonly_fields=('id',)  #This are the read only fields which you cant change

class LikedListingAdmin(admin.ModelAdmin):
    readonly_fields=('id',)  #This are the read only fields which you cant change
admin.site.register(Listing,ListingAdmin)
admin.site.register(LikedListing,LikedListingAdmin)
