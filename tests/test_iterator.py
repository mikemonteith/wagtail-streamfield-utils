import pytest
from streamfieldutils.iterators import flatten_streamfield
from wagtail.core.blocks import CharBlock, IntegerBlock, RichTextBlock

# Define a mark for all tests in this file
pytestmark = pytest.mark.django_db


def test_iterate_count(home_page):
    count = sum(1 for _ in flatten_streamfield(home_page.body))
    assert count == 11


def test_iterate_values(home_page):
    values = [block.value for block, path in flatten_streamfield(home_page.body)]
    assert values[0] == "This is a test homepage"
    assert values[6] == "Aneurin Bevan"
    assert values[9] == "Birth"


def test_iterate_blocks(home_page):
    blocks = [block.block for block, path in flatten_streamfield(home_page.body)]
    assert isinstance(blocks[0], CharBlock)
    assert isinstance(blocks[3], IntegerBlock)
    assert isinstance(blocks[4], RichTextBlock)


def test_iterate_paths(home_page):
    paths = ["/".join(path) for block, path in flatten_streamfield(home_page.body)]
    assert paths[0] == "0/heading"
    assert paths[6] == "5/author/name"
    assert paths[9] == "5/author/body/0/heading"
