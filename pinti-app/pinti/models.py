from django.db import models
from urlparse import urlparse
from urllib import quote as q
import mimetypes
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

STATUS = (
          ('N', 'new'),
          ('C', 'confirmed'),
          ('D', 'declined'),
          )

class DownloadItem(models.Model):
    status = models.CharField(max_length=3, choices=STATUS, default='N', blank=False)
    path = models.CharField(max_length=512)
    group = models.CharField(max_length=128)
    createDate = models.DateTimeField(auto_now_add=True, blank=False)
    updateDate = models.DateTimeField(auto_now=True, blank=False)
    class Meta:
        db_table = 'DownloadItem'

    def _get_mimetype(self):
        "Returns files mime type."
        return mimetypes.guess_type(self.path)[0]
    mimetype = property(_get_mimetype)

    def _get_url(self):
        "Returns the encoded/quoted URL"
        u = urlparse(self.path)
        return '%s://%s%s' % (u.scheme, u.netloc, q(u.path))
    url = property(_get_url)
