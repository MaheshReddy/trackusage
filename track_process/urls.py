from django.conf.urls import patterns, url

from track_process import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^charts/$',views.charts,name='charts'),
   #url(r'^(?P<question_id>\d+)/$',views.details,name='details'),
)
