from django.utils.translation import ugettext as txt
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import delete_object
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import permission_required
from minimar.utils import json_encode
from pinti.models import DownloadItem
from django.utils.datastructures import MultiValueDictKeyError
from minimar.pytrack.decorators import track_visitor
import logging, time

# Get an instance of a logger
logger = logging.getLogger(__name__)

@track_visitor
def index(request, context={}):
    logger.debug('index <-')
    logger.debug('request.user: %s' % request.user)
    context['user'] = request.user
    context['login_backends'] = ('google-oauth2', )
    return render_to_response("pinti/index.html", context)
    
def item_index(request, context={}):
    logger.debug('item_index <-')
    
    q = DownloadItem.objects.all().order_by('group', 'path')
    
    # Make sure page request is an int. If not, deliver first page.
    try:
        pagenum = int(request.GET.get('page', '1'))
    except ValueError:
        pagenum = 1
    logger.debug('pagenum : %d' % pagenum)

    context["title"] = txt('download items')
    context['result_headers'] = [
                                 {'text'  : txt('group'), },
                                 {'text'  : txt('path'), },
                                 {'text'  : txt('type'), },
                                 {'text'  : txt('status'), },
                                 {'text'  : txt('delete'), },
                                 ]
    return object_list(request, q, page=pagenum, paginate_by=50, template_name='pinti/item_list.html', extra_context=context)

def item_create(request):
    if request.method == 'POST':
        #do save
        rawlinks = request.POST['links']
        links = rawlinks.splitlines()
        
        logger.debug('rawlinks    : %r' % rawlinks)
        logger.debug('links       : %r' % links)
        
        group = time.strftime("%Y%m%d_%H%M%S")
        for link in links:
            item = DownloadItem(group=group, path=link)
            logger.debug('item          : %r' % item)
            new_object = item.save()
            logger.debug('new_object    : %r' % new_object)
                
        return HttpResponseRedirect(reverse('pinti.views.item_index'))
    else: 
        return HttpResponse(txt("invalid request."))

def item_edit(request, name=None):
    context = {
               'name' : name,
    }
    return item_index(request, context);

def item_delete(request, key=None):
    return delete_object(request, DownloadItem, object_id=key,
                         post_delete_redirect=reverse('pinti.views.item_index'),
                         template_name='pinti/item_confirm_delete.html')

def item_json(request, name=None):
    if name:
        q = DownloadItem.objects.filter(name__istartswith=name).order_by('group')
    else:
        q = DownloadItem.objects.all().order_by('group')
        
    data = json_encode(q, only=['name'])
    return HttpResponse(data, mimetype="text/plain")
