from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("todos.views",
    url(r'^add_country/$', "add_country", name="add_country"),
    url(r'^add_phone_numbers/$', "add_phone_numbers", name="add_phone_numbers"),
    url(r'^add_full_name/$', "add_full_name", name="add_full_name"),
    url(r'^get_ip_address/$', "get_ip_address", name="get_ip_address"),
    url(r'^validate_email/$', "validate_email_main", name="validate_email"),
    url(r'^validate_email/resend_validation/$', "validate_email_resend_validation", name="validate_email_resend_validation"),
    url(r'^validate_email/resend_validation/force/$', "validate_email_resend_validation", {"force": True}, name="validate_email_resend_validation_force"),
    url(r'^validate_email/validation_sent/$', "validate_email_validation_sent", name="validate_email_validation_sent"),
    url(r'^validate_email/change_address/$', "validate_email_change_address", name="validate_email_change_address"),
)
