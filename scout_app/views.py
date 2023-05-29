from django.shortcuts import render, redirect, get_object_or_404
from .models import Search
from .forms import NewSearchForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def new_search(request):

    """ This is the main page.
        Displays the map and a search form for address input.
        """
    
    if request.method == 'POST':
        new_search_form = NewSearchForm(request.POST)
        new_search = new_search_form.save(commit=False)     # Create a new Place from the form
        new_search.user = request.user                      # Associate the search with the logged in user
        if new_search_form.is_valid():                      # Checks against DB constraints, for example, are required fields present?
            new_search.save()                               # Saves to the database
            return redirect('search_results', search_pk=new_search.pk)

    new_search_form = NewSearchForm()
    return render(request, 'scout_app/search.html', { 'new_search_form': new_search_form })
    

@login_required
def search_results(request, search_pk):

    """ This will take the coordinates from the new_search_form
        make a call to the geocoder
        pass the results to the apis
        then display the search_results.html page 
        """
    
    search = get_object_or_404(Search, pk=search_pk)

    return render(request, 'scout_app/search_results.html', { 'search': search })
    
    
@login_required
def bookmarked_searches(request):

    """ If this is a POST request, the user clicked the Scout button
        in the form. Check if the new search is valid, if so, save a 
        new Search to the database, and redirect to this same page.
        This creates a GET request to this same route.
        
        If not a POST route, or Search is not valid, display a page with
        a list of searches and a form to sdd a new search.
        """

    searches = Search.objects.filter(user=request.user).order_by('name')
    return render(request, 'scout_app/bookmarked_searches.html', { 'searches': searches })