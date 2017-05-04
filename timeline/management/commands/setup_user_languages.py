# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from django.contrib.auth.models import User
from timeline.models import UserLanguage, Language


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

            language = Language.objects.get(pk=1)
            for instance in User.objects.all():
                # create user langauges record here
                ul, created = UserLanguage.objects.get_or_create(
                    user=instance, language=language)
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
