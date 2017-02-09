from django.utils.translation import ugettext as _
 
ITEM_ARTICLE = 'AR'
ITEM_BOOK = 'BK'
ITEM_AUDIO = 'AU'
ITEM_VIDEO = 'VI'
ITEM_WEBSITE = 'WS'

ITEM_TYPE_CHOICES = (
	(ITEM_ARTICLE, _('Article')),
	(ITEM_BOOK, _('Book')),
	(ITEM_AUDIO, _('Audio')),
	(ITEM_VIDEO, _('Video')),
	(ITEM_WEBSITE, _('Website')),
)


TEACHER_TEACHER = 'T'
TEACHER_MASTER = 'M'


TEACHER_TYPE_CHOICES = (
	(TEACHER_TEACHER, _('Teacher')),
	(TEACHER_MASTER, _('Master')),
)