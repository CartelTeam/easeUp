from django.conf.urls import url, include
from . import views
from django.conf.urls import url, include
from django.contrib import admin
from webapp.views import twitter_login, twitter_logout,twitter_authenticated,login1,twitter_signup,loginauth
admin.autodiscover()
urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login1),
    url(r'^loginauth/$', loginauth),
    url(r'^twitter_signup/$', twitter_signup),
    url(r'^twitter_login/?$', twitter_login),
    url(r'^logout/?$', twitter_logout),
    url(r'^login/authenticated/?$', twitter_authenticated),
    url(r'^login/authenticated/search', views.search, name='search'),
    url(r'^login/authenticated/sub', views.sub, name='sub'),
    url(r'^login/authenticated/globe', views.globe, name='globe'),
]
