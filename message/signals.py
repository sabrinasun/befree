from django.dispatch import receiver
from core.views import send_email
from django.template import Context
from userena.contrib.umessages.signals import email_sent


@receiver(email_sent)
def email_sent_signal(sender, **kwargs):
    msg = kwargs['msg']
    from_user_name = msg.sender.profile.get_display_name()
    title = "User %s has sent you a message via BuddhistExchange. " % from_user_name

    for recipient in msg.recipients.all():
        context = Context({'to_user': recipient.profile.get_display_name(),
                           'from_user': from_user_name,
                           'message': msg
                           })
        send_email('message-user.txt', context, title, recipient.email)
