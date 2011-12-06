from django.conf.urls.defaults import *
from pinti.feeds import DownloadItemsFeed

# Uncomment the next line to enable the admin:
#admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',                                 'pinti.views.index'),
    (r'^item/$',                            'pinti.views.item_index'),
    (r'^item/new$',                         'pinti.views.item_create'),
    (r'^item/edit/(?P<key>[ \S]+)/$',       'pinti.views.item_edit'),
    (r'^item/delete/(?P<key>[ \S]+)/$',     'pinti.views.item_delete'),
    (r'^item/json/$',                       'pinti.views.item_json'),
    (r'^item/rss/$',                        DownloadItemsFeed()),

)
