from django.db import models
from userena.utils import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, default='', db_index=True, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return unicode(self.name)


class Post(models.Model):
    user = models.OneToOneField(get_user_model())
    content = models.TextField()
    title = models.CharField(max_length=255, db_index=True)
    link = models.URLField(max_length=255, default=None, null=True, blank=True)
    link_http_mode = models.CharField(max_length=255, default=None, null=True, blank=True)
    language = models.CharField(max_length=5, default='en', db_index=True)
    last_update = models.DateTimeField(auto_now=True, auto_now_add=True)
    category = models.ForeignKey(Category, db_index=True, default=1)

    def __str__(self):
        return unicode(self.user.username + " | " + self.title)

    def __repr__(self):
        return str(self)


class Keyword(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return unicode(self.name)
