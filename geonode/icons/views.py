from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from actstream.models import Action

from geonode.icons.forms import IconForm, IconUpdateForm
from geonode.icons.models import IconProfile


@login_required
def icon_create(request):
    if request.method == "POST":
        form = IconForm(request.POST, request.FILES)
        if form.is_valid():
            icon = form.save(commit=False)
            icon.save()
            form.save_m2m()
            #icon.join(request.user, role="owner")
            return HttpResponseRedirect(
                reverse(
                    "icon_detail",
                    args=[
                        icon.slug]))
    else:
        form = IconForm()

    return render_to_response("icons/icon_create.html", {
        "form": form,
    }, context_instance=RequestContext(request))

@login_required
def icon_update(request, slug):
    icon = IconProfile.objects.get(slug=slug)
    if not icon.owner(request.user, role="owner"):
        return HttpResponseForbidden()

    if request.method == "POST":
        form = IconUpdateForm(request.POST, request.FILES, instance=icon)
        if form.is_valid():
            icon = form.save(commit=False)
            icon.save()
            form.save_m2m()
            return HttpResponseRedirect(
                reverse(
                    "icon_detail",
                    args=[
                        icon.slug]))
    else:
        form = IconForm(instance=icon)

    return render_to_response("icons/icon_update.html", {
        "form": form,
        "icon": icon,
    }, context_instance=RequestContext(request))


class IconDetailView(ListView):

    """
    Mixes a detail view (the icon) with a ListView (the members).
    """
    model = get_user_model()
    template_name = "icons/icon_detail.html"
    paginate_by = None
    icon = None

#    def get_queryset(self):
#        return self.icon.member_queryset()
#
#    def get(self, request, *args, **kwargs):
#        self.icon = get_object_or_404(IconProfile, slug=kwargs.get('slug'))
#        return super(IconDetailView, self).get(request, *args, **kwargs)

#    if icon.user_is_role(request.user,owner"):
#        ctx["owner_form"] = IconMemberForm()

#    ctx.update({
#        "object": icon,
#        "members": icon.member_queryset(),
#        "is_member": icon.user_is_member(request.user),
#        "is_manager": icon.user_is_role(request.user, "manager"),
#    })
#    ctx = RequestContext(request, ctx)
#    return render_to_response("icons/icon_members.html", ctx)


@login_required
def icon_remove(request, slug):
    icon = get_object_or_404(IconProfile, slug=slug)
    if request.method == 'GET':
        return render_to_response(
            "icons/icon_remove.html", RequestContext(request, {"icon": icon}))
    if request.method == 'POST':

        if not icon.user_is_role(request.user, role="owner"):
            return HttpResponseForbidden()

        icon.delete()
        return HttpResponseRedirect(reverse("icon_list"))
    else:
        return HttpResponseNotAllowed()
