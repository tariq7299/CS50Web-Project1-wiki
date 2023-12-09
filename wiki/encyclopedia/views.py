from django.shortcuts import render
from django.http import HttpResponse
import markdown
import difflib


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_wiki_page(request, page_title):
    md_page = util.get_entry(page_title)
    if not md_page:
        return HttpResponse("No page found with title: " + page_title)
    html_page = markdown.markdown(md_page)
    return render(request, 'encyclopedia/page.html', {'title': page_title, 'content': html_page})

def search(request):
    if request.method == "GET":
        
        q = request.GET.get("q", None)
        if not q:
            return HttpResponse("No page found with title: " + q )
        
        md_page = util.get_entry(q)
        if md_page:
            html_page = markdown.markdown(md_page)            
            return render(request, 'encyclopedia/page.html', {'title': q, 'content': html_page})
        
        entries = [entry.lower() for entry in util.list_entries()]
        search_results = difflib.get_close_matches(q.lower(), entries)
        
        if not search_results:
            return HttpResponse("No page found with title: " + q )
        
        return render(request, 'encyclopedia/search_results.html', {'title': q, 'search_results': search_results})