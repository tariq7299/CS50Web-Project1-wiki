from django.shortcuts import render
from django.http import HttpResponse
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_wiki_page(request, page_title):
    md_content = util.get_entry(page_title)
    if not md_content:
        return HttpResponse("No page found with title: " + page_title)
    html_content = markdown.markdown(md_content)
    return render(request, 'encyclopedia/page.html', {'title': page_title, 'content': html_content})
