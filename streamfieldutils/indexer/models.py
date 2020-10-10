from django.db import models


class BlockTypes:
    OTHER = 0
    STRUCT = 1
    STREAM = 2


class IndexEntry(models.Model):

    BLOCK_TYPE_CHOICES = [(BlockTypes.OTHER, "Other"), (BlockTypes.STRUCT, "Struct"), (BlockTypes.STREAM, "Stream")]

    block_name = models.CharField(max_length=255)
    block_type = models.IntegerField(choices=BLOCK_TYPE_CHOICES)
    block_value = models.TextField(blank=True)
    block_path = models.TextField()
    field_name = models.CharField(max_length=255)

    page = models.ForeignKey("wagtailcore.Page", on_delete=models.CASCADE)

    def get_bound_block(self):
        field_value = getattr(self.page.specific, self.field_name)
        path = self.block_path.split("/")

        iterator = iter(path)
        block = field_value
        for path_item in iterator:
            if path_item.isdigit():
                block = block[int(path_item)]
                next(iterator)  # Iterate past the next item, it is the block's name which we don't need.
            else:
                block = block.value[path_item]

        return block

    def __str__(self):
        return f"<IndexEntry {self.page.title}::{self.field_name}::{self.block_path}>"

    class Meta:
        verbose_name_plural = "Index Entries"
