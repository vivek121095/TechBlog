from django.conf.urls import url,include
from blog import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.PostListView.as_view(),name='post_list'),
    url(r'^post/(?P<pk>\d+)$',views.PostDetailView.as_view(),name='post_detail'),
    url(r'^post/new/$', views.CreatePostView.as_view(),name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(),name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(),name='post_remove'),
    url(r'^drafts/$',views.DraftListView.as_view(),name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/comment/$',views.add_comment_to_post,name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve,name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$',views.comment_remove,name='comment_remove'),
    url(r'^post/(?P<pk>\d+)/publish/$',views.post_publish,name='post_publish'),
    url(r'^profile-update/$',views.update_profile,name='update_profile'),
    url(r'^profile/(?P<user_id>\d+)/$',views.profile,name='profile'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns=[
        url(r'^__debug__/',include(debug_toolbar.urls))
    ]+urlpatterns