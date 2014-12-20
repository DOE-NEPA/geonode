from django import forms
from django.core.validators import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

from geonode.icons.models import IconProfile


class IconForm(forms.ModelForm):

    slug = forms.SlugField(
        max_length=20,
        help_text=_("a short version of the name consisting only of letters, numbers, underscores and hyphens."),
        widget=forms.HiddenInput,
        required=False)

    def clean_slug(self):
        if IconProfile.objects.filter(
                slug__iexact=self.cleaned_data["slug"]).count() > 0:
            raise forms.ValidationError(
                _("A icon already exists with that slug."))
        return self.cleaned_data["slug"].lower()

    def clean_title(self):
        if IconProfile.objects.filter(
                title__iexact=self.cleaned_data["title"]).count() > 0:
            raise forms.ValidationError(
                _("A icon already exists with that name."))
        return self.cleaned_data["title"]

    def clean(self):
        cleaned_data = self.cleaned_data

        name = cleaned_data.get("title")
        slug = slugify(name)

        cleaned_data["slug"] = slug

        return cleaned_data

    class Meta:
        model = IconProfile
        exclude = ['icon']


class IconUpdateForm(forms.ModelForm):

    def clean_name(self):
        if IconProfile.objects.filter(
                name__iexact=self.cleaned_data["title"]).count() > 0:
            if self.cleaned_data["title"] == self.instance.name:
                pass  # same instance
            else:
                raise forms.ValidationError(
                    _("A icon already exists with that name."))
        return self.cleaned_data["title"]

    class Meta:
        model = IconProfile
        exclude = ['icon']
