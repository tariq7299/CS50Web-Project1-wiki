from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_title>/", views.get_wiki_page, name="wiki_page"),
    path("search", views.search, name="search"),
    path("new-entry", views.create_new_entry, name="new_entry"),
    path("edit-entry/<str:title>/", views.edit_entry, name="edit_entry"),
    path("random-entry", views.get_random_page, name="random_entry"),
]
