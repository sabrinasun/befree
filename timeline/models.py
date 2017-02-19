from django.db import models
from django.utils.translation import ugettext as _
from userena.utils import user_model_label


from .const import TEACHER_TYPE_CHOICES
# Create your models here.


class Language(models.Model):
    code = models.CharField(max_length=10, null=False, blank=True)
    name = models.CharField(max_length=50, null=False, blank=True)
    order = models.IntegerField()
    users = models.ManyToManyField(user_model_label, through='UserLanguage')


class UserLanguage(models.Model):
    user = models.ForeignKey(
        user_model_label, related_name='user_userlanguages')
    language = models.ForeignKey(
        Language, related_name='language_userlanguages')


class ItemCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True)


class ItemTopic(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True)


class Teacher(models.Model):
    name = models.CharField(max_length=200, null=False, blank=True)
    teacher_type = models.CharField(max_length=200, choices=TEACHER_TYPE_CHOICES)


class TimelineItem(models.Model):
    """
    Generic/Base model for all TimelineItem type , Article/Audio/Video etc Post , Link,
    """
    item_type = models.CharField(max_length=200)
    total_likes = models.IntegerField(default=0)
    total_reblogs = models.IntegerField(default=0)
    created_user = models.OneToOneField(
        user_model_label, related_name='timeline_item_creator')
    created = models.DateTimeField(_("Created Date Time"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified Date Time"), auto_now=True)

    title = models.CharField(max_length=500, db_index=True, blank=True, default="")
    title_link = models.URLField(max_length=500)
    category = models.ForeignKey(ItemCategory)
    content = models.TextField()
    language = models.ForeignKey(Language)
    teacher = models.ForeignKey(Teacher)
    is_original = models.BooleanField()
    topics = models.ManyToManyField(ItemTopic)
    users = models.ManyToManyField(
        user_model_label, through='UserTimelineItem')

    def like(self, user_id):
        self.total_likes += 1
        self.save()

    def unlike(self, user_id):
        if self.total_likes > 0:
            self.total_likes -= 1
            self.save()


class TimelineItemComment(models.Model):
    """
    Keep the comment of a timeline item
    """
    item = models.ForeignKey(TimelineItem)
    text = models.TextField()
    created = models.DateTimeField(_("Created Date Time"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified Date Time"), auto_now=True)


class UserTimelineItem(models.Model):
    user = models.ForeignKey(
        user_model_label, related_name='user_timelineitems')
    item = models.ForeignKey(TimelineItem, related_name='item_timelineitems')
