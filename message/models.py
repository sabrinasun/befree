from django.db import models
from userena.utils import user_model_label
from userena.utils import truncate_words
from django.utils.translation import ugettext_lazy as _


class BoardMessage(models.Model):
    body = models.TextField(_("body"))
    sender = models.ForeignKey(user_model_label,
                               related_name='post_board_messages',
                               verbose_name=_("sender"))

    recipient = models.ForeignKey(user_model_label,
                                  related_name="board_messages",
                                  verbose_name=_("recipient"))

    sent_at = models.DateTimeField(_("sent at"),
                                   auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        """ Human representation, displaying first ten words of the body. """
        truncated_body = truncate_words(self.body, 10)
        return "%(truncated_body)s" % {'truncated_body': truncated_body}
