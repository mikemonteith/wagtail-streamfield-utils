from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class AuthorBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    bio = blocks.RichTextBlock()
    body = blocks.StreamBlock(
        [("heading", blocks.CharBlock()), ("paragraph", blocks.RichTextBlock()), ("image", ImageChooserBlock())]
    )


class BodyBlock(blocks.StreamBlock):

    heading = blocks.CharBlock()
    description = blocks.TextBlock()
    email = blocks.EmailBlock()
    number = blocks.IntegerBlock()
    paragraph = blocks.RichTextBlock()
    image = ImageChooserBlock()
    author = AuthorBlock()
