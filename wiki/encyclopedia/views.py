from django.shortcuts import render
from django.http import HttpResponse
import markdown
import difflib
import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_wiki_page(request, page_title):
    md_page = util.get_entry(page_title)
    
    # This will mean that the title typed in the url doseno't represent any entries's page found in storage!
    if not md_page:
        return HttpResponse("No page found with title: " + page_title)
    
    # Here I am converting the markdown content into html, in order to be viewed appropriately in the page
    html_page = markdown.markdown(md_page)
    return render(request, 'encyclopedia/page.html', {'title': page_title, 'content': html_page})

# This function handles the search functionality.
def search(request):
    # Check if the request method is GET.
    if request.method == "GET":
        # Get the query parameter 'q' from the GET request.
        q = request.GET.get("q", None)
        # If 'q' is None or empty, return a response indicating no page was found.
        if not q:
            return HttpResponse("No page found with title: " + q )
        
        # Try to get the page with the title 'q'.
        md_page = util.get_entry(q)
        # If the page exists, render it.
        if md_page:
            html_page = markdown.markdown(md_page)            
            return render(request, 'encyclopedia/page.html', {'title': q, 'content': html_page})
        
        # If the page doesn't exist, get a list of all entries and find close matches to 'q'.
        entries = [entry.lower() for entry in util.list_entries()]
        search_results = difflib.get_close_matches(q.lower(), entries)
        
        # If there are no close matches, return a response indicating no page was found.
        if not search_results:
            return HttpResponse("No page found with title: " + q )
        
        # If there are close matches, render the search results page.
        return render(request, 'encyclopedia/search_results.html', {'title': q, 'search_results': search_results})

# This function handles the creation of new entries.
def create_new_entry(request):
    # Check if the request method is POST.
    if request.method == "POST":
        # Create a form instance with the data from the POST request.
        form = util.NewEntryForm(request.POST)
        # Check if the form is valid.
        if form.is_valid():
            # Get the title and content from the form.
            title = form.cleaned_data['title']
            md_entry_content = form.cleaned_data['md_entry_content']
            
            # Check if an entry with the given title already exists.
            entry = util.get_entry(title)
            if entry:
                # If the entry exists, return a response indicating the entry already exists.
                return HttpResponse("Entry already exists")
            # If the entry doesn't exist, save the new entry.
            util.save_entry(title, md_entry_content)
            # Render the new entry.
            html_page = markdown.markdown(md_entry_content)
            return render(request, 'encyclopedia/page.html', {'title': title, 'content': html_page})
    
    # If the request method is not POST, render the new entry form.
    return render(request, "encyclopedia/create_new_entry.html", {'form': util.NewEntryForm()})

# This function handles the editing of entries.
def edit_entry(request, title):
    # Check if the request method is POST.
    if request.method == "POST":
        # Create a form instance with the data from the POST request.
        form = util.NewEntryForm(request.POST)
        # Check if the form is valid.
        if form.is_valid():
            # Get the title and content from the form.
            title = form.cleaned_data['title']
            md_entry_content = form.cleaned_data['md_entry_content']
            # Save the edited entry.
            util.save_entry(title, md_entry_content)
            # Render the edited entry.
            html_page = markdown.markdown(md_entry_content)
            return render(request, 'encyclopedia/page.html', {'title': title, 'content': html_page})
    
    # If the request method is not POST, get the current entry and render the edit entry form.
    md_entry_content = util.get_entry(title)
    form = util.NewEntryForm(initial={'title': title, 'md_entry_content': md_entry_content})
   
    return render(request, "encyclopedia/edit_entry.html", {'title': title, 'form': form})

# This function returns a random page.
def get_random_page(request):
    # Get a list of all entries.
    entries = util.list_entries()
    # Choose a random entry.
    page_title = random.choice(entries)
    # Get the content of the random entry.
    md_page = util.get_entry(page_title)
    # Render the random entry.
    html_page = markdown.markdown(md_page)
    return render(request, 'encyclopedia/page.html', {'title': page_title, 'content': html_page})
