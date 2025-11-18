from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/',
        views.delete_review, name='movies.delete_review'),
    path('top-comments/', views.top_funny_comments, name='movies.top_comments'),
    path('<int:id>/review/<int:review_id>/funny/', views.toggle_funny, name='movies.toggle_funny'),
    path('hidden/', views.hidden_movies, name='movies.hidden'),
    path('<int:id>/hide/', views.hide_movie, name='movies.hide'),
    path('<int:id>/unhide/', views.unhide_movie, name='movies.unhide'),
    path('petitions/', views.petitions_index, name='movies.petitions'),
    path('petitions/new/', views.petitions_new, name='movies.petitions_new'),
    path('petitions/<int:petition_id>/vote/', views.petitions_vote, name='movies.petitions_vote'),
    path('watchlist/', views.watchlist_index, name='movies.watchlist'),
    path('<int:id>/watchlist/add/', views.watchlist_add, name='movies.watchlist_add'),
    path('<int:id>/watchlist/remove/', views.watchlist_remove, name='movies.watchlist_remove'),
]