# Python imports
import os
import requests
import json
import logging


# Django imports
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# Third party imports
from celery import shared_task
from sentry_sdk import capture_exception
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Module imports
from plane.db.models import Workspace, WorkspaceMemberInvite, User
from plane.license.utils.instance_value import get_email_configuration


@shared_task
def workspace_invitation(email, workspace_id, token, current_site, invitor):
    print("Invitation code")
    
    try:
        print("In try",email)
        
        user = User.objects.get(email=invitor)

        workspace = Workspace.objects.get(pk=workspace_id)
        workspace_member_invite = WorkspaceMemberInvite.objects.get(
            token=token, email=email
        )
        print("In try",email)
        # Relative link
        relative_link = f"/workspace-invitations/?invitation_id={workspace_member_invite.id}&email={email}&slug={workspace.slug}"

        # The complete url including the domain
        abs_url = str(current_site) + relative_link


        (
            EMAIL_HOST,
            EMAIL_HOST_USER,
            EMAIL_HOST_PASSWORD,
            EMAIL_PORT,
            EMAIL_USE_TLS,
            EMAIL_FROM,
        ) = get_email_configuration()
        print("Check 3")
        print("Data" ,EMAIL_HOST,EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,EMAIL_PORT,EMAIL_FROM,EMAIL_USE_TLS,"  End")
        # Subject of the email
        subject = f"{user.first_name or user.display_name or user.email} has invited you to join them in {workspace.name} on Plane"

        context = {
            "email": email,
            "first_name": user.first_name or user.display_name or user.email,
            "workspace_name": workspace.name,
            "abs_url": abs_url,
        }
        print("Check 4")
        html_content = render_to_string(
            "emails/invitations/workspace_invitation.html", context
        )
        
        text_content = strip_tags(html_content)

        workspace_member_invite.message = text_content
        workspace_member_invite.save()
        print("Check 5",EMAIL_HOST, EMAIL_USE_TLS,type(EMAIL_USE_TLS))
        connection = get_connection(
            host=EMAIL_HOST,
            port=int(EMAIL_PORT),
            username=EMAIL_HOST_USER,
            password=EMAIL_HOST_PASSWORD,
            use_tls=(EMAIL_USE_TLS=="True") ,
        )
        print("Check 6")

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=EMAIL_FROM,
            to=[email],
            connection=connection,
        )
        recepient = [email]
        cont_tent = "This is content"
        print("Recepient",recepient)
        print("Data" ,subject,cont_tent,EMAIL_FROM,recepient)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("message sent successfully from  ",EMAIL_FROM, "  to ",email)
        
        
        # Send message on slack as well
        if settings.SLACK_BOT_TOKEN:
            client = WebClient(token=settings.SLACK_BOT_TOKEN)
            try:
                _ = client.chat_postMessage(
                    channel="#trackers",
                    text=f"{workspace_member_invite.email} has been invited to {workspace.name} as a {workspace_member_invite.role}",
                )
            except SlackApiError as e:
                print(f"Got an error: {e.response['error']}")

        return
    except (Workspace.DoesNotExist, WorkspaceMemberInvite.DoesNotExist) as e:
        print("Workspace or WorkspaceMember Invite Does not exists")
        return
    except Exception as e:
        # Print logs if in DEBUG mode
        if settings.DEBUG:
            print(e)
        capture_exception(e)
        return
    print("Code ended")




# 1041409647284-bpbfdl1a2paprtf50dfa11b1vmlk3jj8.apps.googleusercontent.com