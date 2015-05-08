from django.conf.urls import url, patterns

from views import UserNewActivitiesCount

urlpatterns = patterns('',
    url(r'^follow/(?P<user_id>[\d]+)([L])?/$', view="social_network.views.follow", name='follow_user'),
    url(r'^try_become_friends/(?P<user_id>[\d]+)([L])?/$', view="social_network.views.try_become_friends", name='try_become_friends_with'),
    url(r'^unfollow/(?P<user_id>[\d]+)([L])?/$', view="social_network.views.unfollow", name='unfollow_user'),
    url(r'^user/new/messages/$', UserNewActivitiesCount.as_view(), name='social_network_new_activities_count'),
    url(r'^$', view="social_network.views.activities", name='user_activities'),
)
