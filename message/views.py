from userena.contrib.umessages.views import MessageDetailListView, message_compose
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, CreateView
from network.models import UserNetwork
from timeline.views import SubHeaderCategoryMixin
from timeline.models import ItemCategory
from userena.contrib.umessages.models import MessageContact
from .forms import ComposeMessageForm
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import BoardMessage
from django.shortcuts import get_object_or_404


class ChatFollowMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(ChatFollowMixin,
                        self).get_context_data(**kwargs)

        return get_extra_context(context, self.request)


class UserMessageDetailListView(SubHeaderCategoryMixin, ChatFollowMixin, MessageDetailListView):

    template_name = 'message/message_list_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserMessageDetailListView,
                        self).get_context_data(**kwargs)
        context['to_username'] = self.kwargs['username']
        return context


def get_extra_context(extra_context, request):
    if not extra_context:
        extra_context = dict()
    extra_context['following_users'] = UserNetwork.objects.get_following_users(
        request.user)
    message_contacts = MessageContact.objects.get_contacts_for(
        request.user)
    to_from_users = []
    distinct_users = set(to_from_users)

    for contact in message_contacts:
        if contact.um_from_user != request.user and contact.um_from_user not in distinct_users:
            distinct_users.add(contact.um_from_user)
            to_from_users.append(contact.um_from_user)
        if contact.um_to_user != request.user and contact.um_to_user not in distinct_users:
            to_from_users.append(contact.um_to_user)
    extra_context['to_from_users'] = to_from_users
    return extra_context


@login_required
def send_message(request, recipients=None, compose_form=ComposeMessageForm,
                 success_url=None, template_name="message/message_form.html",
                 recipient_filter=None, extra_context=None):

    if request.method == "POST":
        if recipients:
            username_list = [r.strip() for r in recipients.split("+")]
            recipients = [u for u in get_user_model().objects.filter(
                username__in=username_list)]
            success_url = reverse('user_message_list_detail', kwargs={
                'username': recipients[0].username})
    elif request.method == "GET":
        if not extra_context:
                extra_context = dict()
        extra_context['categories'] = ItemCategory.objects.get_all_catergories()

    return message_compose(request, recipients, compose_form, success_url, template_name, recipient_filter, get_extra_context(extra_context, request))


class BoardMessageListView(SubHeaderCategoryMixin, ListView):
    template_name = 'message/user_board_message.html'

    def get_context_data(self, **kwargs):
        context = super(BoardMessageListView, self).get_context_data(**kwargs)
        context['board_owner'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        messageboard_owner = get_object_or_404(User, pk=self.kwargs['pk'])
        return BoardMessage.objects.filter(recipient=messageboard_owner)


class BoardMessageCreateView(CreateView):
    template_name = 'message/user_board_message.html'
    model = BoardMessage
    fields = ['body']

    def form_valid(self, form):
        form.instance.recipient_id = self.kwargs.get('pk')
        form.instance.sender = self.request.user
        return super(BoardMessageCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('boardmessage_list', kwargs={
            'pk': self.kwargs['pk']})
