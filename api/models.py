from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models



class User(models.Model):
    pass


class Genre(models.Model):
    pass


class Category(models.Model):
    pass


class Title(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        null=False
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews", 
        null=False
    )
    score = models.IntegerField(
        "score",
        null=False,
        validators=[MinValueValidator(1, "Необходимо > 1"),
                    MaxValueValidator(10, "Необходимо < 10")]
    )
    pub_date = models.DateTimeField(
        "review pub date",
        auto_now_add=True
    )

    class Meta:
        ordering = ("-pub_date",)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        null=False
    )
    text = models.TextField(
        "text of comment",
        null=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        null=False
    )
    pub_date = models.DateTimeField(
        "comment pub date",
        auto_now_add=True
    )

    class Meta:
        ordering = ("-pub_date",)

