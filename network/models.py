from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404


#log = logging.getLogger("%s.%s" % (settings.LOGGING_BASE, __name__,))

class UserNetworkManager(models.Manager):

    def has_followed(self, user, follower):
        queryset = super(UserNetworkManager, self).get_queryset().filter(
            user=user, follower=follower, status=1)
        return queryset.count() > 0

    def get_followers(self, user):
        queryset = super(UserNetworkManager, self).get_queryset().filter(
            user=user, status=1)
        return [x.follower for x in queryset]

    def get_follower_count(self, user):
        queryset = super(UserNetworkManager, self).get_queryset().filter(
            user=user, status=1)
        return queryset.count()

    def get_following_users(self, user):
        queryset = super(UserNetworkManager, self).get_queryset().filter(
            follower=user, status=1)
        return [x.user for x in queryset]

    def get_following_count(self, user):
        queryset = super(UserNetworkManager, self).get_queryset().filter(
            follower=user, status=1)
        return queryset.count()

    def follow_user(self, user, following):
        if not following in self.get_following_users(user):
            user_network = UserNetwork()
            user_network.user = following
            user_network.follower = user
            user_network.save()
        else:
            # TODO : error message
            pass

    def unfollow_user(self, user, following):
        try:
            user_network = self.get_queryset().get(user=following, follower=user, status=1)
        except Exception as e:
            print(e)
        else:
            user_network.delete()

    def ban_follower(self, user, follower):
        try:
            user_network = self.get_queryset().get(user=user, follower=follower, status=1)
        except Exception as e:
            print(e)
        else:
            user_network.ban_follower()


class UserNetwork(models.Model):
    user = models.ForeignKey(User, related_name='network_user')
    follower = models.ForeignKey(User, related_name='network_follower')
    status = models.IntegerField(blank=True, default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_notified = models.BooleanField(_('Is notified ?'), default=False)
    is_show = models.BooleanField(_('Is show ?'), default=True)

    objects = UserNetworkManager()

    def has_notified(self):
        """
        changed user as notified user
        """
        self.is_notified = True
        self.save()

    def hide_notification(self):
        """
        changed is show status from True to False
        """
        self.is_show = False
        self.save()

    def approve_request(self):
        """
        Approve network request by User, 0
        """
        self.status = 1
        self.save()

    def reject_request(self):
        """
        Reject Network Request by User, 1
        """
        self.status = 2
        self.save()

    def cancel_request(self):
        """
        Cancel Network Request by Follower, 3
        """
        self.status = 3
        self.save()

    def remove_follower(self):
        """
        Remove Follower by User, 4
        """
        self.status = 4
        self.save()

    def remove_user(self):
        """
        Remove User by Follower, 5
        """
        self.status = 5
        self.save()

    def ban_follower(self):
        """
        Ban Follower by User, 6
        """
        self.status = 6
        self.save()

    def ban_user(self):
        """
        Ban User by Follower, 7
        """
        self.status = 7
        self.save()

    def status_info(self):
        """
        Show status meaning.
        """
        if self.status == 0:
            return "Waiting approval from %s" % self.user
        elif self.status == 1:
            return "Approved by %s" % self.user
        elif self.status == 2:
            return "Rejected by %s" % self.user
        elif self.status == 3:
            return "Cancelled request by %s" % self.follower
        elif self.status == 4:
            return "Removed by %s" % self.user
        elif self.status == 5:
            return "Removed by %s" % self.follower
        elif self.status == 6:
            return "Banned by %s" % self.user
        elif self.status == 7:
            return "Banned by %s" % self.follower

    status_info.allow_tags = True

    def save(self, *args, **kwargs):
        '''
        Author =
        '''
        is_new = True
        if self.id is not None:
            is_new = False

        predata = None
        if not is_new:
            predata = UserNetwork.objects.get(pk=self.id)

        super(UserNetwork, self).save(*args, **kwargs)

        if is_new:
            #            try:
            #                from feed.signals import action
            #                from feed.models import ActionType

            #                action.send(self.follower, action_object=self, action_type=get_object_or_404(ActionType, id=5), target=self.user)
            #            except Exception, e:
            #                pass

            # if follower notificaiton setting is enabled
            subject = "%(follower)s follows you on Befree" % {
                'follower': self.follower.get_full_name()}
            title = ''
            message = subject
            #push_notification.send(sender=self.user, subject=subject, title=title , message=message)
        else:
            pass
