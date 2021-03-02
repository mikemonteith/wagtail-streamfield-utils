from django.core.management.base import BaseCommand

from streamfieldutils.indexer import indexer


class Command(BaseCommand):
    """
    """

    help = ""

    def handle(self, *args, **kwargs):

        indexer.index_all()
