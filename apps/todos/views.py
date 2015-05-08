from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views.decorators.http import require_safe
from django.views.generic import View

from django.utils.decorators import classonlymethod

from mailing_lists.models import MailingListSignup

from todos import forms
from todos.decorators import todo_depends, todo_function

from notifications import Events


class BaseView(View):

    @classonlymethod
    def as_view(cls, **kwargs):
        func = View.as_view.im_func(cls, **kwargs)
        # Pass dependencies onto 'view' function
        if hasattr(cls, "todo_depends"):
            func.todo_depends = cls.todo_depends
        return func

    def render(self, context):
        return render(self.request, self.template_name, context)

    def delete_todo(self):
        self.request.user.todos.filter(
                view_name=self.__class__.__name__).delete()


@todo_function
class add_country(BaseView):

    template_name = "todos/add_country.html"

    def get(self, request):
        profile = request.user.get_profile()
        form = forms.CountryForm(instance=profile)
        return self.render({"form": form})

    def post(self, request):
        profile = request.user.get_profile()
        form = forms.CountryForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            self.delete_todo()
            return redirect("home")
        return self.render({"form": form})


@todo_function
@todo_depends("add_country")
class add_phone_numbers(BaseView):

    template_name = "todos/add_phone_numbers.html"

    def get(self, request):
        # Just in case the user has no country set
        try:
            request.user.get_profile().country
        except ObjectDoesNotExist:
            request.user.todos.get_or_create(view_name="add_country")
            return redirect("todos:add_country")

        use_old_as = request.GET.get("use_old_as", None)
        stall = request.user.stall
        try:
            phone_old = stall.phone_old
        except ObjectDoesNotExist:
            phone_old = None
        else:
            if use_old_as is None:
                return self.render({"phone_old": phone_old,
                                    "second_page": True})
        initial = {}
        if phone_old is not None:
            if use_old_as == "fixed":
                initial["phone_landline"] = phone_old.phone_number
            elif use_old_as == "mobile":
                initial["phone_mobile"] = phone_old.phone_number
        form = forms.AddPhoneNumbersForm(instance=stall, initial=initial)
        return self.render({"form": form})

    def post(self, request):
        stall = request.user.stall
        form = forms.AddPhoneNumbersForm(request.POST, instance=stall)
        if form.is_valid():
            form.save()
            try:
                phone_old = stall.phone_old
            except ObjectDoesNotExist:
                pass
            else:
                phone_old.delete()
            self.delete_todo()
            return redirect("home")
        return self.render({"form": form})


@todo_function
class add_full_name(BaseView):

    template_name = "todos/add_full_name.html"

    def get(self, request):
        form = forms.FullNameForm(instance=request.user)
        return self.render({"form": form})

    def post(self, request):
        form = forms.FullNameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            self.delete_todo()
            return redirect("home")
        return self.render({"form": form})


@todo_function
class get_ip_address(BaseView):

    def get(self, request):
        mlss = request.user.mailinglistsignup_set.all()
        if mlss.count() == 0:
            # This should never be the case, but just in case...
            mlss = [MailingListSignup.objects.create_from_user(request.user)]
        for mls in mlss:
            mls.set_ip_address(request)
            mls.save()
        self.delete_todo()
        return redirect("home")


@todo_function("validate_email")
@todo_depends("add_full_name")
@require_safe
def validate_email_main(request,
                        template_name="todos/validate_email_main.html"):
    return render(request, template_name, {})


@todo_function("validate_email")
@todo_depends("add_full_name")
def validate_email_resend_validation(request, force=False):
    profile = request.user.get_profile()
    if force or profile.activation_key_expired():
        profile.generate_activation_key_and_save()
    Events(request).user_signup(request.user)    
    return redirect("todos:validate_email_validation_sent")


@todo_function("validate_email")
@todo_depends("add_full_name")
@require_safe
def validate_email_validation_sent(
        request, template_name="todos/validate_email_validation_sent.html"):
    return render(request, template_name, {
        "email": request.user.email,
    })


@todo_function("validate_email")
@todo_depends("add_full_name")
class validate_email_change_address(BaseView):

    template_name = "todos/validate_email_change_address.html"

    def get(self, request):
        form = forms.ChangeEmailAddressForm(instance=request.user)
        return self.render({
            "email": request.user.email,
            "form": form,
        })

    def post(self, request):
        form = forms.ChangeEmailAddressForm(request.POST,
                                            instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("todos:validate_email_resend_validation_force")
        return self.render({
            "email": request.user.email,
            "form": form,
        })
