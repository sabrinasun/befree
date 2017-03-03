from django.db import models
from django.utils.translation import ugettext as _
from userena.utils import user_model_label
from .const import TEACHER_TYPE_CHOICES, TEACHER_TEACHER
import uuid


class Language(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True)
    order = models.IntegerField()
    users = models.ManyToManyField(
        user_model_label, through='UserLanguage', related_name='languages')

    def __str__(self):
        return self.name


class UserLanguage(models.Model):
    user = models.ForeignKey(
        user_model_label, related_name='user_userlanguages')
    language = models.ForeignKey(
        Language, related_name='language_userlanguages')


class ItemCategoryManager(models.Manager):

    def get_all_catergories(self):
        return super(ItemCategoryManager, self).get_queryset().order_by('order')

    def get_link_form_categories(self):
        return super(ItemCategoryManager, self).filter(link_form=True).order_by('order')

    def get_text_form_categories(self):
        return super(ItemCategoryManager, self).filter(text_form=True).order_by('order')


class ItemCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True)
    order = models.PositiveIntegerField()
    link_form = models.BooleanField()
    text_form = models.BooleanField()
    order = models.IntegerField()
    objects = ItemCategoryManager()

    def __str__(self):
        return self.name


class ItemTopic(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True)


class Teacher(models.Model):
    name = models.CharField(max_length=200, null=False, blank=True)
    teacher_type = models.CharField(
        max_length=200, choices=TEACHER_TYPE_CHOICES, default=TEACHER_TEACHER)


def text_form_file_name(instance, filename):
    return '/'.join(['timeline', str(uuid.uuid4()) + '_' + filename])


class TimelineItem(models.Model):
    """
    Generic/Base model for all TimelineItem type , Article/Audio/Video etc Post , Link,
    """
    #total_likes = models.IntegerField(default=0)
    #total_reblogs = models.IntegerField(default=0)
    created_user = models.ForeignKey(
        user_model_label, related_name='timeline_item_creator')
    created = models.DateTimeField(_("Created Date Time"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified Date Time"), auto_now=True)

    title = models.CharField(
        max_length=500, db_index=True)
    title_link = models.URLField(max_length=500)
    item_category = models.ForeignKey(ItemCategory)
    content = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Language)
    teacher = models.ForeignKey(Teacher)
    is_original = models.BooleanField()
    uploaded_file = models.FileField(
        upload_to=text_form_file_name, null=True, blank=True)
    topics = models.ManyToManyField(ItemTopic, related_name='timelineitems')
    users = models.ManyToManyField(
        user_model_label, related_name='users')
    likes = models.ManyToManyField(
        user_model_label, related_name='like_users')

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()

    @property
    def content_length(self):
        return len(self.content)

    @property
    def total_reblogs(self):
        count = self.users.count()
        if count > 0:
            return self.users.count() - 1
        else:
            return 0

    def like(self, user):
        self.likes.add(user)
        self.save()

    def unlike(self, user):
        self.likes.remove(user)
        self.save()

    def has_pdf_html(self):
        if self.uploaded_file and self.uploaded_file.name.endswith(('.pdf', '.htm', '.html')):
            return True
        return False

    def reblog(self, user):
        self.users.add(user)
        self.save()


class TimelineItemComment(models.Model):
    """
    Keep the comment of a timeline item
    """
    item = models.ForeignKey(TimelineItem, related_name='comments')
    comment_user = models.ForeignKey(
        user_model_label, related_name='comment_user')
    text = models.TextField()
    created = models.DateTimeField(_("Created Date Time"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified Date Time"), auto_now=True)

"""
class UserTimelineItem(models.Model):
    user = models.ForeignKey(
        user_model_label, related_name='user_timelineitems')
    item = models.ForeignKey(TimelineItem, related_name='item_timelineitems')


class LikeUserTimelineItem(models.Model):
    user = models.ForeignKey(
        user_model_label, related_name='likeuser_timelineitems')
    item = models.ForeignKey(
        TimelineItem, related_name='likeitem_timelineitems')
"""
