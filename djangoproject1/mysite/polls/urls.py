from django.conf.urls import url
from polls import views 
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views




app_name = 'polls'

urlpatterns = [
    url(r'^index/$', views.IndexView, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<question_id>[0-9]+)/choice/$', views.add_choice, name='add_choice'),
    url(r'^(?P<question_id>[0-9]+)/delete/$', views.delete_question, name='delete_question'),
    url(r'^add$', views.add_poll, name='add_polls'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', views.profile, name='profile'),
    url(r'^email/$', views.email, name='email'),
    url(r'^viewall/$', views.viewAllResults, name='viewAllResults'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', auth_views.login, name='login'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'logout/$', auth_views.login, name='login'),
  
    
    


    
    

]
