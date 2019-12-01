import json
import pytest
from wagtail.core.blocks.stream_block import StreamValue
from wagtail.core.models import Page

from .testapp.models import HomePage


@pytest.fixture
def root_page():
    return Page.objects.get(slug="root", depth=1)


@pytest.fixture
def home_page(root_page):
    body_data = [
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
    stream_block = HomePage.body.field.stream_block
    home_page = HomePage(
        body=StreamValue(stream_block, [], is_lazy=True, raw_text=json.dumps(body_data)),
        title="Home Page",
        slug="homepage",
    )
    root_page.add_child(instance=home_page)
    home_page.refresh_from_db()
    return home_page
