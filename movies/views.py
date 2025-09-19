from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Length
from django.db.models import Count
from .models import Movie, Review, ReviewFunnyVote, HiddenMovie, Petition, PetitionVote
def index(request):
    movies = Movie.objects.all()
    if request.user.is_authenticated:
        movies = movies.exclude(
            id__in=HiddenMovie.objects.filter(user=request.user).values('movie_id')
        )
    template_data = {'title': 'Movies', 'movies': movies}
    return render(request, 'movies/index.html', {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = (
        Review.objects
        .filter(movie=movie)
        .annotate(num_funny=Count('funny_votes', distinct=True))
        .order_by('-date')  # keep your existing order; we just add the count
    )
    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews,
    }
    return render(request, 'movies/show.html', {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)


@login_required
def toggle_funny(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, movie_id=id)
    vote, created = ReviewFunnyVote.objects.get_or_create(review=review, user=request.user)
    if not created:
        vote.delete()  # un-funny (toggle off)
    return redirect('movies.show', id=id)

def top_funny_comments(request):
    # site-wide funniest comments: most funny votes first, then newest
    reviews = (
        Review.objects
        .annotate(num_funny=Count('funny_votes', distinct=True))
        .select_related('movie', 'user')
        .order_by('-num_funny', '-date')
    )
    template_data = {'title': 'Top Comments (Funniest)', 'reviews': reviews}
    return render(request, 'movies/top_comments.html', {'template_data': template_data})

@login_required
def hidden_movies(request):
    movies = Movie.objects.filter(hidden_by__user=request.user).distinct()
    template_data = {'title': 'Hidden Movies', 'movies': movies}
    return render(request, 'movies/hidden.html', {'template_data': template_data})

@login_required
def hide_movie(request, id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=id)
        HiddenMovie.objects.get_or_create(movie=movie, user=request.user)
    return redirect('movies.index')

@login_required
def unhide_movie(request, id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=id)
        HiddenMovie.objects.filter(movie=movie, user=request.user).delete()
    # If you unhide from the hidden page, keep them there:
    return redirect('movies.hidden')

def petitions_index(request):
    petitions = (Petition.objects
                 .annotate(yes_count=Count('votes', distinct=True))
                 .order_by('-yes_count', '-created'))
    return render(request, 'movies/petitions_index.html',
                  {'template_data': {'title': 'Petitions', 'petitions': petitions}})

@login_required
def petitions_new(request):
    if request.method == 'POST':
        title = (request.POST.get('movie_title') or '').strip()
        details = (request.POST.get('details') or '').strip()
        if title:
            Petition.objects.create(movie_title=title, details=details, requested_by=request.user)
            return redirect('movies.petitions')
    return render(request, 'movies/petitions_new.html',
                  {'template_data': {'title': 'New Petition'}})

@login_required
def petitions_vote(request, petition_id):
    # Idempotent "Yes" vote: creates if missing; if already voted, do nothing
    if request.method == 'POST':
        petition = get_object_or_404(Petition, id=petition_id)
        PetitionVote.objects.get_or_create(petition=petition, user=request.user)
    return redirect('movies.petitions')


# Create your views here.
