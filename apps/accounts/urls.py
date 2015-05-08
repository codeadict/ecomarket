# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import \
    password_reset, password_reset_done, password_reset_complete
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from accounts.forms import PasswordResetForm
from main.utils import redirect_to

from accounts.views import (
    AccountPromotionDiscountsView,
    AccountPromotionStallStoryView,
    AccountPromotionWelcomeVideoView,
    custom_password_reset_confirm
)
from accounts.views import account as account_views
from accounts.views import bought as bought_views
from accounts.views import dashboard as dashboard_views
from accounts.views import selling as selling_views
from accounts.views import stall as stall_views
from accounts.views import sold as sold_views
from accounts.views import profile as profile_views
from accounts.views.invoice import InvoiceView
from accounts.views import stockcheck as stockcheck_views
from accounts.views import video as video_views

from todos.decorators import ignore_todos

urlpatterns = patterns(
    'accounts.views',
    url(r'^register/success/$',
        TemplateView.as_view(template_name='accounts/register_success.html'),
        name='register_success'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),

    # password reset
    url(r'^password/reset/$',
        password_reset,
        {'template_name': 'accounts/password_reset.html',
         'password_reset_form': PasswordResetForm,
         'post_reset_redirect': None},
        name='password_reset'),
    url(r'^password/reset/done/$',
        password_reset_done,
        {'template_name': 'accounts/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^pasword/reset/'
        + '(?P<uidb36>[0-9A-Za-z]{1,13})'
        + '-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        custom_password_reset_confirm,
        {'template_name': 'accounts/password_reset_confirm.html',
         'post_reset_redirect': None},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        password_reset_complete,
        {'template_name': 'accounts/password_reset_complete.html'},
        name='password_reset_complete'),
    url(r'^verify/success/$',
        TemplateView.as_view(template_name='accounts/verify_success.html'),
        name='verify_success'),
    url(r'^new-users-redirect-url/$',
        redirect_to(
            'register_success',
            permanent=True,
            pass_params=False)),
    url(r'^verify/failure/$',
        ignore_todos(TemplateView.as_view(template_name='accounts/verify_failure.html')),
        name='verify_failure'),
    url(r'^verify/(?P<token>\w+)/$', 'verify', name='verify'),

    # accounts tabs
    url(r'^promotion/$',
        login_required(AccountPromotionDiscountsView.as_view()),
        name="promotion"),
    url(r'^promotion/discounts/$',
        login_required(AccountPromotionDiscountsView.as_view()),
        name="promotion_discounts"),
    url(r'^promotion/stall_story/$',
        login_required(AccountPromotionStallStoryView.as_view()),
        name="promotion_stall_story"),
    url(r'^promotion/welcome_video/$',
        login_required(AccountPromotionWelcomeVideoView.as_view()),
        name="promotion_welcome_video"))

# Dashboard
urlpatterns += patterns(
    'accounts.views.dashboard',
    url(r'^dashboard/$',
        dashboard_views.DashboardRedirectView.as_view(),
        name="dashboard"),
    url(r'^dashboard/awaiting_delivery/$',
        dashboard_views.DashboardAwaitingDeliveryView.as_view(),
        name="dashboard_awaiting_delivery"),
    url(r'^dashboard/waiting_feedback/$',
        dashboard_views.DashboardWaitingFeedbackView.as_view(),
        name="dashboard_waiting_feedback"),
    url(r'^dashboard/unresolved_questions/$',
        dashboard_views.DashboardUnresolvedQuestionsView.as_view(),
        name="dashboard_unresolved_questions"))

# Sold
urlpatterns += patterns(
    'accounts.views.sold',
    url(r'^sold/$',
        sold_views.SoldRedirectView.as_view(),
        name="sold"),
    url(r'^sold/awaiting_shipping/$',
        sold_views.SoldAwaitingShippingView.as_view(),
        name="sold_awaiting_shipping"),
    url(r'^sold/awaiting_feedback/$',
        sold_views.SoldAwaitingFeedbackView.as_view(),
        name="sold_awaiting_feedback"),
    url(r'^sold/completed/$',
        sold_views.SoldCompletedView.as_view(),
        name="sold_completed"),
    url(r'^sold/all/$',
        sold_views.SoldAllView.as_view(),
        name="sold_all"),
    url(r'^sold/(?P<order_id>\d+)$',
        sold_views.SoldOrderDetailView.as_view(),
        name='seller_order_detail'))

# Selling
urlpatterns += patterns(
    'accounts.views.selling',
    url(r'^selling/$',
        selling_views.SellingRedirectView.as_view(),
        name="selling"),
    url(r'^selling/published/$',
        selling_views.SellingPublishedLiveView.as_view(),
        name="selling_published_live"),
    url(r'^selling/unpublished/$',
        selling_views.SellingUnpublishedView.as_view(),
        name="selling_unpublished"),
    url(r'^selling/sold_out/$',
        selling_views.SellingSoldOutView.as_view(),
        name="selling_sold_out"))

# Bought
urlpatterns += patterns(
    'accounts.views.bought',
    # url(r'^bought/$',
    # bought_views.AccountBoughtBoughtView.as_view(),
    # name="bought"),
    url(r'^bought/$',
        bought_views.BoughtView.as_view(),
        name="bought"),
    url(r'^bought/awaiting_feedback/$',
        bought_views.BoughtAwaitingFeedbackView.as_view(),
        name="bought_awaiting_feedback"),
    url(r'^bought/feedback_given/$',
        bought_views.BoughtFeedbackGivenView.as_view(),
        name="bought_feedback_given"))

# invoice
urlpatterns += patterns(
    'account.views.invoice',
    url(r'^invoice/(?P<order_id>\d+)$', InvoiceView.as_view(),  name='invoice'))

# Stall
urlpatterns += patterns(
    'accounts.views.stall',
    url(r'^stall/$',
        stall_views.AccountStallTabRedirectView.as_view(),
        name="stall"),
    url(r'^stall/appearance/$',
        stall_views.AccountStallAppearanceView.as_view(),
        name="stall_appearance"),

    url(r'^stall/shipping/$',
        stall_views.AccountStallShippingView.as_view(),
        name="stall_shipping"),

    url(r'^stall/address/$',
        stall_views.AccountStallAddressView.as_view(),
        name="stall_address"),

    url(r'^stall/payment/$',
        stall_views.AccountStallPaymentView.as_view(),
        name="stall_payment"),
    url(r'^stall/policies/$',
        stall_views.AccountStallPoliciesView.as_view(),
        name="stall_policies"),
    url(r'^stall/faq/$',
        stall_views.AccountStallFaqView.as_view(),
        name="stall_faq"),
    url(r'^stall/options/$',
        stall_views.AccountStallOptionsView.as_view(),
        name="stall_options"))

# Account
urlpatterns += patterns(
    'accounts.views.account',
    url(r'^account/$',
        account_views.AccountTabAccountRedirectView.as_view(),
        name="account"),
    url(r'^account/account/$',
        account_views.AccountTabAccountView.as_view(),
        name="account_account"),
    url(r'^account/delivery_addresses/(?P<address_id>\d+)?$',
        account_views.AccountTabDeliveryAddressesView.as_view(),
        name="account_delivery_addresses"),
    url(r'^account/update_address/(?P<pk>\d+)/$',
        account_views.AccountDeliveryAddressUpdateView.as_view(),
        name="account_delivery_address_update"),
    url(r'^account/delete_address/(?P<pk>\d+)/$',
        'account_delivery_address_delete',
        name="account_delivery_address_delete"),
    url(r'^account/connected_accounts/$',
        account_views.AccountTabConnectedAccountsView.as_view(),
        name="account_connected_accounts"),
    url(r'^account/email_notifications/$',
        account_views.AccountTabEmailNotificationsView.as_view(),
        name="account_email_notifications"),
    url(r'^account/privacy/$',
        account_views.AccountTabPrivacyView.as_view(),
        name="account_privacy"))

# Profile
urlpatterns += patterns(
    'accounts.views.profile',
    url(r'^profile/$', 'profile', name='profile'),
)

# Avatar
urlpatterns += patterns(
    'accounts.views.profile',
    url(r'avatar/upload/$', profile_views.AvatarUploaderAjax.as_view(), name='avatar_upload'),
)

# Currency
urlpatterns += patterns(
    'accounts.views',
    url(r'currency/save/$',
        'save_currency_preference',
        name='save_currency_preference'),
)

# Stock Check, Card #183 on Trello
# https://trello.com/c/YVF5y7EI/183
urlpatterns += patterns('accounts.views.stockcheck',
    url(r'stockcheck/start/',
        stockcheck_views.stockcheck_start,
        name='stockcheck_landing'),
    url(r'stockcheck/update/',
        stockcheck_views.StockcheckUpdateView.as_view(),
        name='stockcheck_update'),
)


# Video system
urlpatterns += patterns('accounts.views.video',
    url(
        r'video/$',
        video_views.VideoAdminView.as_view(),
        name='video'
    ),
    url(
        r'video/create/$',
        video_views.VideoCreateView.as_view(),
        name='video_create'
    ),
    url(
        r'video/edit/(?P<pk>[-_\d]+)/$',
        video_views.VideoEditView.as_view(),
        name='video_edit'
    ),
)