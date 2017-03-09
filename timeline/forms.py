# coding=utf-8
from django import forms
from .models import TimelineItem, ItemCategory, Language, Teacher, ItemTopic, TimelineItemComment
import json
import magic

ALLOWED_UPLOAD_FILE_TYPES = [
    'application/pdf',
    'text/html',
    'text/htm',
    'image/jpeg',
    'image/gif',
    'image/bmp',
    'image/png',
    'image/tiff',
    'image/svg+xml',
]


class PostBaseForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=None, empty_label=None)
    teacher_name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Enter the name of the teacher who gave the teaching', 'class': 'ui-autocomplete-input', 'autocomplete': 'off'}))
    topic_list = forms.CharField(max_length=12, required=False, widget=forms.TextInput(
        attrs={'style': 'width:80px;', 'class': 'ui-autocomplete-input', 'autocomplete': 'off'}))

    def __init__(self, *args, **kwargs):
        current_request = kwargs.pop('request')
        self.topics = current_request.POST.getlist('topic_list')
        self.user = current_request.user
        super(PostBaseForm, self).__init__(*args, **kwargs)

        if self.user.languages.filter(users=self.user).exists():
            self.fields['language'].queryset = self.user.languages.filter(
                users=self.user)
        else:
            self.fields[
                'language'].queryset = Language.objects.filter(id=1)

        self.existing_topic = json.dumps([])
        # update case
        if self.instance.pk:
            if self.instance.teacher:
                self.fields[
                    'teacher_name'].initial = self.instance.teacher.name
                itemtopics = [
                    topic.name for topic in self.instance.topics.all()]
                self.existing_topic = json.dumps(itemtopics)
            self.fields['item_category'].initial = self.instance.item_category

    class Meta:
        model = TimelineItem
        fields = ('item_category', 'title', 'content',
                  'language', 'is_original', 'topic_list',)

    def save(self, commit=True):
        data = self.cleaned_data
        instance = super(PostBaseForm, self).save(commit=False)
        instance.created_user = self.user
        if data['teacher_name']:
            teacher, created = Teacher.objects.get_or_create(
                name=data['teacher_name'])
            instance.teacher = teacher
        instance.created_user = self.user

        if commit:
            instance.save()

        for topic_name in self.topics:
            topic, created = ItemTopic.objects.get_or_create(
                name=topic_name)
            instance.topics.add(topic)

        instance.users.add(self.user)

        return instance


class LinkForm(PostBaseForm):

    item_category = forms.ModelChoiceField(
        queryset=ItemCategory.objects.get_link_form_categories(), empty_label=None, widget=forms.RadioSelect, initial=1)

    class Meta(PostBaseForm.Meta):
        model = TimelineItem
        fields = PostBaseForm.Meta.fields + ('title_link',)


class TextForm(PostBaseForm):

    item_category = forms.ModelChoiceField(
        queryset=ItemCategory.objects.get_text_form_categories(), empty_label=None, widget=forms.RadioSelect, initial=1)

    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)
        self.fields['teacher_name'].required = False

    def clean_uploaded_file(self):
        uploaded_file = self.cleaned_data['uploaded_file']
        if uploaded_file:
            if not self.file_type in ALLOWED_UPLOAD_FILE_TYPES:
                raise forms.ValidationError("Unsupported file type")
            self.file_type = magic.from_buffer(uploaded_file.read(), mime=True)
            self.file_name = uploaded_file.name
        return uploaded_file

    def save(self):
        instance = super(TextForm, self).save(commit=True)
        if instance.uploaded_file:
            instance.file_name = self.file_name
            instance.file_type = self.file_type
        instance.save()
        return instance

    class Meta(PostBaseForm.Meta):
        model = TimelineItem
        fields = PostBaseForm.Meta.fields + ('uploaded_file',)


class UpdateLinkForm(LinkForm):

    def __init__(self, *args, **kwargs):
        super(UpdateLinkForm, self).__init__(*args, **kwargs)


class CommentForm(forms.ModelForm):

    class Meta:
        model = TimelineItemComment
        fields = ('text',)
