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
