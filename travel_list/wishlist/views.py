from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.exceptions import PermissionDenied

@login_required
def place_list(request):
    
    if request.method == "POST":
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)  # create a new place from the form
        place.user = request.user # associate place with the login user
        if form.is_valid():  # check against DB constraint, are required field present?
            place.save()  # save to the database
            return redirect(
                "place_list"
            )  # redirect to GET view with name place_list i.e. same view

    # display non visited countries, use name column to order the list

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by("name")
    
    new_place_form = NewPlaceForm()
    return render(
        request,
        "wishlist/wishlist.html",
        {"places": places, "new_place_form": new_place_form})


@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True)  # display visited countries
    return render(request, "wishlist/visited.html", {"visited": visited})


# handling a post request with PK not in database
@login_required
def place_was_visited(request):
    if request.method == "POST":
        pk = request.POST.get("pk")
        place = get_object_or_404(Place, pk=pk)
        print(place.user, request.user)
        if place.user == request.user: #only let a user visit their own places
            place.visited = True
            place.save()
        else:
            raise PermissionDenied()
            

    return redirect('place_list')


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # verify user is same as request user
    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method =='POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
# instance is the model object to update with the form data

        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # Temp error message

        return redirect('place_details', place_pk=place_pk)
    
    else: #GET place details
        if place.visited:
            review_form = TripReviewForm(instance=place) #pre-populate with data from this Place instance
            return render(request, 'wishlist/place_detail.html', {'place': place, 'review_form': review_form} )
        
        else:
            return render(request, 'wishlist/place_detail.html', {'place': place} )

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
