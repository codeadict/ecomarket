from login import LoginForm
LoginForm

from password_reset import PasswordResetForm
PasswordResetForm

from registration import RegistrationForm
RegistrationForm

from settings import SettingsForm
SettingsForm

from profile import UserProfileForm, DetailedUserProfileForm
UserProfileForm, DetailedUserProfileForm

# this doesnt seem to be used
def order_fields(form, field_list, throw_away=False):
    """
    Accepts a form and a list of dictionary keys which map to the
    form's fields. After running the form's fields list will begin
    with the fields in field_list. If throw_away is set to true only
    the fields in the field_list will remain in the form.

    example use:
    field_list = ['first_name', 'last_name']
    order_fields(self, field_list)
    """
    if throw_away:
        form.fields.keyOrder = field_list
    else:
        for field in field_list[::-1]:
            form.fields.insert(0, field, form.fields.pop(field))

