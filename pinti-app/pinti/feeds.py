from django.contrib.syndication.views import Feed
from pinti.models import DownloadItem
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class DownloadItemsFeed(Feed):
    title = "pinti download items"
    link = "/item/rss/"
    description = "Download links for pinti."
    mime_type = 'text/xml'

    def items(self):
        items = DownloadItem.objects.all().order_by('group')
        for item in items:
            logger.debug('item          : %r' % item)
        return items

    def item_title(self, item):
        return "%s - %s" %(item.group, item.path)

    def item_description(self, item):
        return "%s %s" % (item.group, item.path)
    
    def item_link(self, item):
        return item.path

    def item_pubdate(self, item):
        return item.updateDate

    def item_enclosure_url(self, item):
        return item.path
    
    def item_enclosure_length(self, item):
        return "42"

    def item_enclosure_mime_type(self, item):
        return item.mimetype
