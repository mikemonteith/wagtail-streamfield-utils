import json

import pytest
from wagtail.core.blocks.stream_block import StreamValue

from streamfieldutils.indexer import indexer
from streamfieldutils.indexer.models import BlockTypes, IndexEntry

from .testapp.models import HomePage

# Define a mark for all tests in this file
pytestmark = pytest.mark.django_db

BLOCKS = [
    {"type": "heading", "value": "This is a test homepage"},
    {"type": "description", "value": "We use it for unit tests"},
    {"type": "email", "value": "user@example.com"},
    {"type": "number", "value": 123},
    {"type": "paragraph", "value": "Richtext can have some <strong>bold</strong> or <em>italics</em>"},
    {
        "type": "author",
        "value": {
            "name": "Aneurin Bevan",
            "bio": "<em>Nye Bevan</em> was a Welsh Labour Party politician who was the Minister for Health in the UK from 1945 to 1951.",
            "body": [
                {"type": "heading", "value": "Birth"},
                {
                    "type": "paragraph",
                    "value": "Aneurin Bevan was born on 15 November 1897 at 32 Charles Street in Tredegar, Monmouthshire.",
                },
            ],
        },
    },
]


def get_blocks(seed):
    """
    Return a selection of blocks using a seed (from 0 to 2^len(BLOCKS)).
    The seed number's binary representation will be used as a filter of the BLOCKS list.
    e.g seed = 13 in binary is 1011 so the 1st, 3rd and 4th blocks will be returned.
    """
    return [block for i, block in enumerate(BLOCKS) if (seed & pow(2, i))]


@pytest.fixture
def many_pages(root_page):
    pages = []

    # Create 10 pages containing a range of different content blocks
    for i in range(0, 20):
        body_data = get_blocks(seed=i)
        stream_block = HomePage.body.field.stream_block
        page = HomePage(
            body=StreamValue(stream_block, [], is_lazy=True, raw_text=json.dumps(body_data)),
            title=f"Home Page {i}",
            slug=f"homepage-{i}",
        )
        root_page.add_child(instance=page)
        page.refresh_from_db()
        pages.append(page)
    return pages


def test_index_all_pages(many_pages):
    assert IndexEntry.objects.count() == 0

    # Run indexing
    indexer.index_all()

    # all of the pages in many_pages contain 40 blocks in total.
    assert IndexEntry.objects.count() == 40
    assert IndexEntry.objects.filter(block_name="description").count() == 10
    assert IndexEntry.objects.filter(page__title="Home Page 1").get().block_name == "heading"
    assert IndexEntry.objects.filter(page__title="Home Page 19").count() == 3


def test_index_overwrites_previous(many_pages):
    assert IndexEntry.objects.count() == 0

    # Run the indexing twice.
    indexer.index_all()
    indexer.index_all()

    # The index should not have duplicate entries
    assert IndexEntry.objects.count() == 40


def test_index_custom_query(many_pages):
    assert IndexEntry.objects.count() == 0

    # Select homepage-1 and homepage-10 through 19
    query = HomePage.objects.filter(slug__startswith="homepage-1").specific()
    indexer.index_all(page_query=query)

    assert IndexEntry.objects.count() == 26


def test_index_one_page(many_pages):
    assert IndexEntry.objects.count() == 0
    indexer.index_page(many_pages[1].specific)

    # many_pages[1] contains only one block, so we expect one index
    assert IndexEntry.objects.count() == 1


def test_index_block_name(home_page):
    indexer.index_page(home_page)
    assert IndexEntry.objects.all()[0].block_name == "heading"
    assert IndexEntry.objects.all()[1].block_name == "description"
    assert IndexEntry.objects.all()[2].block_name == "email"


def test_index_block_type(home_page):
    indexer.index_page(home_page)
    assert IndexEntry.objects.filter(block_name="heading")[0].block_type == BlockTypes.OTHER
    assert IndexEntry.objects.filter(block_name="author")[0].block_type == BlockTypes.STRUCT
    assert IndexEntry.objects.filter(block_name="body")[0].block_type == BlockTypes.STREAM


def test_index_block_value(home_page):
    indexer.index_page(home_page)
    assert IndexEntry.objects.filter(block_name="heading")[0].block_value == "This is a test homepage"
    assert IndexEntry.objects.filter(block_name="number")[0].block_value == "123"
    assert IndexEntry.objects.filter(block_name="author")[0].block_value == ""
    assert IndexEntry.objects.filter(block_name="body")[0].block_value == ""


def test_index_block_path(home_page):
    indexer.index_page(home_page)
    assert IndexEntry.objects.all()[0].block_path == "0/heading"
    assert IndexEntry.objects.all()[6].block_path == "5/author/name"
    assert IndexEntry.objects.all()[10].block_path == "5/author/body/1/paragraph"


def test_index_block_(home_page):
    indexer.index_page(home_page)
    assert IndexEntry.objects.all()[0].field_name == "body"
