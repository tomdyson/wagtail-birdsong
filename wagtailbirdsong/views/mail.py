from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper

from ..models import Receipt, Contact


def redirect_helper(campaign):
    url_helper = AdminURLHelper(type(campaign))
    campaign_list_url = url_helper.get_action_url('index')

    return redirect(campaign_list_url)


def send_campaign(backend, request, campaign, contacts):
    success = backend.send_campaign(
        request, campaign, campaign.subject, contacts)

    Receipt.objects.bulk_create([
        Receipt(campaign=campaign, contact=c, success=success) for c in contacts
    ])
    if success:
        for contact in contacts:
            Receipt.objects.create(campaign=campaign, contact=contact, sent_date=timezone.now())
        messages.add_message(
            request, messages.SUCCESS, f"Campaign '{campaign.name}' sent to {len(contacts)} contacts")
    else:
        messages.add_message(request, messages.ERROR,
                             f"Campaign '{campaign.name}' failed to send")

    return redirect_helper(campaign)


def send_test(backend, request, campaign):
    test_email = request.POST.get('test_email', False)

    # FIXME this won't work with a custom contact model
    test_contact = Contact(email=test_email)
    success = backend.send_campaign(
        request, campaign, f"[TEST] {campaign.subject}.", [test_contact])

    if success:
        messages.add_message(request, messages.SUCCESS, f"Test email sent, please check your inbox")
    else:
        messages.add_message(request, messages.ERROR, f"Test email failed to send")

    return redirect_helper(campaign)
