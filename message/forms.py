from userena.contrib.umessages.forms import ComposeForm
from django.utils.translation import ugettext_lazy as _


class ComposeMessageForm(ComposeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to'].widget.attrs.update(
            {'placeholder': _('Enter a User Name')})
