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

# Create your models here.
