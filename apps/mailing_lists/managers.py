from django.db.models import Manager

from django.contrib.auth.models import User

from mailing_lists.constants import MemberTypes


class MailingListManager(Manager):
    def create_from_email(self, email_address, **kwargs):
        """
        Ensure there is a MailingListSignup object for that e-mail
        """
        try:
            user = User.objects.get(email=email_address)
            return self.create_from_user(user)
        except User.DoesNotExist:
            return self.create(email_address=email_address, **kwargs)

    def create_from_user(self, user):
        """
        Create (or update) a MailingListSignup object for the user
        """
        profile = user.get_profile()
        member_type = (MemberTypes.SELLER
                       if profile.is_seller else MemberTypes.NORMAL)
        if self.filter(email_address=user.email).count() != 0:
            instance = self.get(email_address=user.email)
            instance.member_type = MemberTypes.NORMAL
            instance.first_name = user.first_name
            instance.last_name = user.last_name
            instance.user = user
            instance.save()
            return instance
        return self.create(email_address=user.email,
                           user=user,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           member_type=member_type)
