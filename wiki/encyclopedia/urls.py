from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_title>/", views.get_wiki_page, name="wiki_page"),
    path("search", views.search, name="search"),
    path("new-entry", views.create_new_entry, name="new_entry"),
]
