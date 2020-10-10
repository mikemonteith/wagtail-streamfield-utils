# wagtail-streamfield-utils

## API

### iterators

`flatten_streamfield(streamvalue)`

Returns a generator, yielding (block, path) tuple to each block in a streamfield.

```py
from streamfieldutils.iterators import flatten_streamfield

page = MyPage.objects.first()
# Print a slash-separated path to each block followed by the block's value.
for block, path in flatten_streamfield(page.body):
    print("/".join(path), block.value)
```

### indexer

The indexer creates an index of all of the blocks that are in use in streamfields in your page models.

Add `streamfieldutils.indexer` to your installed apps.

```py
INSTALLED_APPS = [
    ...
    "streamfieldutils.indexer",
    ...
]
```

Run `python manage.py streamfieldutils_index` to index all pages.

After indexing, your database will contain one `IndexEntry` for every block found in a page model.

#### ModelAdmin

If you would like to see a list of indexed blocks in your wagtail admin interface, you can register the [modeladmin](https://docs.wagtail.io/en/latest/reference/contrib/modeladmin/index.html)

Make sure modeladmin app is installed:
```py
INSTALLED_APPS = [
    ...
    "wagtail.contrib.modeladmin",
    ...
]
```

Register the `IndexEntryAdmin` in a wagtail_hooks.py file:
```py
from wagtail.contrib.modeladmin.options import modeladmin_register
from streamfieldutils.indexer.modeladmin import IndexEntryAdmin

modeladmin_register(IndexEntryAdmin)
```

#### IndexEntry model

##### Fields

`block_name`
The name that you gave to your block in the streamfield definition.
e.g "author" or "heading" in the following example:
```py
my_field = StreamField([
    ('author', AuthorBlock()),
    ('heading', CharBlock()),
])
```

`block_value`
The value of the block if it can be converted to a string. `StructBlock` and `StreamBlock`s have an empty string as the block_value since you can inspect the contents of those blocks by looking at their sub-blocks.

`block_path`
A slash-delimited path to the location of the block within the streamfield.
E.g. if block_path = `5/author/title`

1. `5`. The 6th block in the streamfield.
2. `author`. The 6th block is named `author`.
3. `title`. The `title` sub-block of `author`.

`field_name`
The name of the field where the block was found.

`page`
The page where the block was found.

`get_bound_block()`
Returns a Wagtail `BoundBlock` instance of the block. See the [Wagtail docs](https://docs.wagtail.io/en/v2.0/topics/streamfield.html#boundblocks-and-values) for explaination of `BoundBlock`s.

##### Example usage

If you had an `author` block and wanted to find all usage of that block:

```py
from streamfieldutils.indexer.models import IndexEntry

for index_entry in IndexEntry.objects.filter(block_name="author"):
    print(index_entry.page.id) # Print the page ID where the block is found
    print(index_entry.field_name) # Print the field where the block is found
    print(index_entry.block_path) # Print a slash-separated path to the block inside the field
```

## Contributing

### Getting started

1. Clone the repo `git clone https://github.com/mikemonteith/wagtail-streamfield-utils.git`
2. Install dependencies `pip install -e .[testing]`

### Formatting

`black .`

### Linting

`flake8 .`

### Tests

`pytest`
