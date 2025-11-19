# blog/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager

User = get_user_model()


# --- Модель 1: Категория ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL Slug")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# --- Модель 2: Пост ---
class Post(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Title")
    content = models.TextField(verbose_name="Content of the text")
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        verbose_name="Cover"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name="Author"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        verbose_name="Category"
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Approved by the administrator"
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name="View count"
    )
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="to the post"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Author"
    )
    content = models.TextField(verbose_name="Comment Text")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ('created_at',)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title[:20]}"