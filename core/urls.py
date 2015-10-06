from django.conf.urls import url
from django.contrib import auth
import django.contrib.auth.views

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', auth.views.logout, {'template_name': 'user/logged_out.html'}, name='logout'),
    url(r'^password_change$', auth.views.password_change, {'template_name': 'user/password_change_form.html'}, name='password_change'),
    url(r'^password_change/done$', auth.views.password_change_done, {'template_name': 'user/password_change_done.html'}, name='password_change_done'),
    url(r'^password_reset$', auth.views.password_reset, {'template_name': 'user/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done$', auth.views.password_reset_done, {'template_name': 'user/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        auth.views.password_reset_confirm, {'template_name': 'user/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done$', auth.views.password_reset_complete, {'template_name': 'user/password_reset_complete.html'}, name='password_reset_complete'),

    url(r'^dashboard$', views.dashboard, name='dashboard'),

    url(r'^kanji/(?P<kanji_id>[0-9]+)$', views.kanji_detail, name='kanji-detail'),
    url(r'^kanji/list$', views.kanji_list, name='kanji-list'),
    url(r'^kanji/collection/(?P<collection_id>[0-9]+)$', views.kanji_collection_detail, name='kanji-collection-detail'),
    url(r'^kanji/collection/list/(?P<category>[a-zA-Z0-9]+)$', views.kanji_collection_list, name='kanji-collection-list'),
    url(r'^kanji/collection/list$', views.kanji_collection_list_all, name='kanji-collection-list-all'),

    url(r'api/mark/kanji$', views.mark_kanji, name='api-mark-kanji'),
    url(r'api/unmark/kanji$', views.unmark_kanji, name='api-unmark-kanji'),

    url(r'^word/(?P<word_id>[0-9]+)$', views.word_detail, name='word-detail'),
    url(r'^word/list$', views.word_list, name='word-list'),
]
