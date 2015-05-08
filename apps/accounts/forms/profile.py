from django import forms

from accounts.models import UserProfile
from image_crop.utils import retrieve_cropped_image, idnormalizer
from main.utils import absolute_uri

attrs_dict = {'class': 'required'}


class UserProfileForm(forms.ModelForm):
    """Profile form to be used at registration"""

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs.update({'class': 'select'})

    class Meta:
        model = UserProfile
        fields = ['avatar', 'gender', 'send_newsletters']


class DetailedUserProfileForm(forms.ModelForm):
    """Profile form that is used in account/profile settings"""
    def __init__(self, *la, **kwa):
        self.request = kwa.pop('request', None)
        super(DetailedUserProfileForm, self).__init__(*la, **kwa)

        # self.fields['avatar'].widget = CroppableFileInput()
        self.fields['avatar'].widget.attrs.update({'class': 'avatar-picker'})
        self.fields['gender'].widget.attrs.update({'class': 'select'})

    def _save_avatar(self, user_profile):
        # TODO: fix naming wrongness!

        avatar_file = self.request.POST.get('image_filename')
        if not avatar_file or not '.' in avatar_file:
            return

        avatar_title = self.request.POST.get('image_title')
        avatar = retrieve_cropped_image(avatar_file)

        if avatar_title:
            avatar_ext = avatar_file.split('.').pop().lower()
            avatar_filename = '%s.%s' % (
                idnormalizer.normalize(avatar_title),
                avatar_ext)
        else:
            avatar_filename = avatar_file[37:]

        if avatar:
            coords = avatar['coords']
            user_profile.data.update(
                {'image_crop': [coords['xl'],
                                coords['xr'],
                                coords['yt'],
                                coords['yb']]})

            user_profile.avatar.save(
                avatar_filename, avatar['content'],
                True,
                [coords['xl'], coords['yt'],
                 coords['xr'], coords['yb']])

    def save(self, *la, **kwa):
        user_profile = super(DetailedUserProfileForm, self).save()
        self._save_avatar(user_profile)
        return user_profile

    class Meta:
        model = UserProfile
        fields = ['avatar', 'gender', 'birthday', 'city', 'about_me']
        widgets = {
            'birthday': forms.TextInput(attrs={'class': 'date-picker'}),
        }
