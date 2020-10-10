from wagtail.core import hooks

from .indexer import index_page


@hooks.register("after_create_page")
def index_after_create_page(request, page):
    index_page(page)


@hooks.register("after_edit_page")
def index_after_edit_page(request, page):
    index_page(page)
