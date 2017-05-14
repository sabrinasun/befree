# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth.models import User
from timeline.models import ItemCategory, ItemTopic, TimelineItem


class Command(BaseCommand):

    help = "Populate initial value for UserLanguages"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--commit',
                            action='store_true',
                            dest='commit',
                            default=False,
                            help='Commit the transaction')

    @transaction.atomic
    def handle(self, **options):
        try:
            sid = transaction.savepoint()

            for instance in ItemCategory.objects.all():
                instance.slug = slugify(instance.name, allow_unicode=True)
                instance.save()
                pass

            for instance in ItemTopic.objects.all():
                instance.slug = slugify(instance.name, allow_unicode=True)
                instance.save()
                pass

            for instance in TimelineItem.objects.all():
                instance.save()
                pass

            eid = transaction.savepoint()
        except Exception as ex:
            print('Error occurred, transaction rollback.')
            transaction.savepoint_rollback(sid)
            raise
        else:
            if options['commit']:
                print('Successful commit')
                transaction.savepoint_commit(eid)
            else:
                print('Successful dry-run')
                transaction.savepoint_rollback(sid)
