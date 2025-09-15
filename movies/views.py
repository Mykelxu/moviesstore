from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Length
from django.db.models import Count
from .models import Movie, Review, ReviewFunnyVote
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})
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

# Create your views here.
