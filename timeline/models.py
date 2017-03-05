from django.db import models
from django.utils.translation import ugettext as _
from userena.utils import user_model_label
from .const import TEACHER_TYPE_CHOICES, TEACHER_TEACHER
import uuid

PDF_HTML_HTM_FILE_TYPES = [
    'application/pdf',
    'text/html',
    'text/htm',
]


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
    teacher = models.ForeignKey(Teacher, null=True)
    is_original = models.BooleanField()
    uploaded_file = models.FileField(
        upload_to=text_form_file_name, null=True, blank=True)
    file_type = models.CharField(
        max_length=50, null=False, blank=True, default='')
    file_name = models.CharField(
        max_length=50, null=False, blank=True, default='')
    topics = models.ManyToManyField(ItemTopic, related_name='timelineitems')
    users = models.ManyToManyField(
        user_model_label, related_name='user_items')
    likes = models.ManyToManyField(
        user_model_label, related_name='like_items')

    @property
    def total_likes(self):
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

    @property
    def total_comments(self):
        return self.comments.count()

    def like(self, user):
        self.likes.add(user)
        self.save()

    def unlike(self, user):
        self.likes.remove(user)
        self.save()

    def is_uploaded_file_pdfhtml(self):
        if self.uploaded_file and self.file_type in PDF_HTML_HTM_FILE_TYPES:
            return True
        return False

    def is_uploaded_file_pdf(self):
        return self.file_type == 'application/pdf'

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
