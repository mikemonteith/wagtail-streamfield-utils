from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

from . import blocks


class HomePage(Page):

    body = StreamField(blocks.BodyBlock)

    content_panels = Page.content_panels + [StreamFieldPanel("body")]
