from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django_cas_ng.utils import get_cas_client, get_service_url
# from django.contrib.auth import login, authenticate
import json
from django.urls import reverse

# Create your views here.

def home(request):
    return JsonResponse({
        'is_authenticated': request.user.is_authenticated,
        'user': str(vars(request.user))
    })

def login(request, force_login=True):
    # request.path = fix_request_path_on_proxy(request.path)
    service_url = get_service_url(request)
    client = get_cas_client(service_url=service_url)
    login_url = client.get_login_url()

    ticket = request.GET.get('ticket')
    if ticket:
        sso_profile = authenticate(ticket, client)

        if sso_profile is None and force_login:
            return HttpResponseRedirect(login_url)

        return HttpResponse(json.dumps(sso_profile))
    else:
        return HttpResponseRedirect(login_url)


def authenticate(ticket, client):
    username, attributes, _ = client.verify_ticket(ticket)

    if not username:
        return None

    # if "kd_org" in attributes:
    #     attributes.update(get_additional_info(attributes["kd_org"]) or {})

    sso_profile = {"username": username, "attributes": attributes}
    return sso_profile
