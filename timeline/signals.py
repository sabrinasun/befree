from django.dispatch import receiver
from django.utils.text import slugify
from timeline.models import TimelineItem, ItemTopic
from django.db.models.signals import pre_save
import itertools


@receiver(pre_save, sender=TimelineItem)
def save_timelineItem(sender, instance, **kwargs):
    slug = slugify(instance.title, allow_unicode=True)
    instance.slug = orig = slug[:222]

# handle duplicate slug
    for x in itertools.count(1):
        if not TimelineItem.objects.filter(slug=instance.slug).exists():
            break
        instance.slug = '%s-%d' % (orig, x)


@receiver(pre_save, sender=ItemTopic)
def save_itemTopic(sender, instance, **kwargs):
    slug = slugify(instance.name, allow_unicode=True)
    instance.slug = orig = slug[:222]

# handle duplicate slug
    for x in itertools.count(1):
        if not ItemTopic.objects.filter(slug=instance.slug).exists():
            break
        instance.slug = '%s-%d' % (orig, x)
