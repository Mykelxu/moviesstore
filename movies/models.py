from django.db import models
from django.contrib.auth.models import User
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class ReviewFunnyVote(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='funny_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='funny_votes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f"FunnyVote(user={self.user_id}, review={self.review_id})"

class HiddenMovie(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='hidden_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_hides')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')  # one hide per user per movie

    def __str__(self):
        return f"Hidden(movie={self.movie_id}, user={self.user_id})"

# Create your models here.

class Petition(models.Model):
    movie_title = models.CharField(max_length=255)
    details = models.TextField(blank=True)            # optional description
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie_title

class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petition_votes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'user')       # 1 affirmative vote per user per petition