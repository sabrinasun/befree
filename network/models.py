from django.db import models

from userena.utils import get_user_model


class Post(models.Model):
    user = models.OneToOneField(get_user_model(), unique=True)
    content = models.TextField()
    title = models.CharField(max_length=255)
    link = models.SlugField()
    lang = models.CharField(max_length=5)
    last_update = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __str__(self):
        return unicode(self.user.username + " | " + self.title)


class Category(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post)

    class Meta:

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return unicode(self.name)
