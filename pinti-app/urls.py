from django.conf.urls.defaults import include, patterns

# Uncomment the next line to enable the admin:
#admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$',                        'djangoappengine.views.warmup'),
    (r'',                                   include('pinti.urls')),
    (r'^accounts/',                         include('registration.backends.default.urls')),

)
