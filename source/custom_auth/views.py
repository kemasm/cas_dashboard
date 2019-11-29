from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django_cas_ng.utils import get_cas_client, get_service_url
from django.contrib.auth import login, authenticate
import json, pdb
from django.urls import reverse
import django_cas_ng.views as cas_views


# Create your views here.

def home(request):
    return JsonResponse({
        'is_authenticated': request.user.is_authenticated,
        'user': str(vars(request.user)),
        'message': str(vars(request)),
        'username': request.user.username,
    })

def login(request, force_login=True):
    # request.path = fix_request_path_on_proxy(request.path)
    service_url = get_service_url(request)
    client = get_cas_client(service_url=service_url)
    login_url = client.get_login_url()

    ticket = request.GET.get('ticket')
    if ticket:
        sso_profile = authenticate2(ticket, client)

        if sso_profile is None and force_login:
            return HttpResponseRedirect(login_url)

        z = {'sso': sso_profile, 'is_auth':request.user.is_authenticated}
        return HttpResponse(json.dumps(z))
    else:
        return HttpResponseRedirect(login_url)


def authenticate2(ticket, client):
    username, attributes, _ = client.verify_ticket(ticket)

    if not username:
        return None

    # if "kd_org" in attributes:
    #     attributes.update(get_additional_info(attributes["kd_org"]) or {})

    sso_profile = {"username": username, "attributes": attributes}
    return sso_profile

class LoginView(cas_views.LoginView):
    def successful_login(self, request, next_page):
        # ticket = request.GET.get('ticket')
        # service_url = get_service_url(request, next_page)
        # if ticket:
        #     user = authenticate(ticket=ticket, service=service_url, request=request)

        return super(LoginView, self).successful_login(request, next_page)
