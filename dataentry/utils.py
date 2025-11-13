from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import hashlib
import time
import os
from emails.models import Email, Sent, EmailTracking, Subscriber
from bs4 import BeautifulSoup


def get_custom_models():
    default_models = [
        "ContentType",
        "Session",
        "Group",
        "Permission",
        "LogEntry",
        "Upload",
        "TaskResult",
        "ChordCounter",
        "GroupResult",
        "User",
    ]
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models


def check_csv_errors(file_path, model_name):
    # Search for model across all installed apps.
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue

    if not model:
        raise CommandError(f"Model {model_name} not found in any app.")

    model_fields = [
        field.name
        for field in model._meta.fields
        if field.name not in ["id", "created_at", "updated_at"]
    ]

    # get all the field names of the model that we have found.
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            # compare csv header with model's field names.
            if csv_header != model_fields:
                raise DataError(
                    f"CSV file doesn't match with the {model_name} table fields."
                )
    except Exception as e:
        raise e

    return model


def send_email_notification(
    mail_subject, message, to_email, attachment=None, email_id=None
):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recepient_mail in to_email:
            new_message = message
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(
                    email_list=email.email_list, email_address=recepient_mail
                )
                timestamp = str(time.time())
                data_to_hash = f"{recepient_mail}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email=email, subscriber=subscriber, unique_id=unique_id
                )

                # Generate tracking pixel URL.
                base_url = settings.BASE_URL
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"

                # Search for the links in the email
                soup = BeautifulSoup(message, "html.parser")
                urls = [a["href"] for a in soup.find_all("a", href=True)]

                # If there are links or urls in the email body, inject our click tracking url in that original link
                if urls:
                    for url in urls:
                        # make the final tracking url
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")

                # Create the email content with tracking pixel image
                open_tracking_img = (
                    f"<img src='{open_tracking_url}' width='1' height='1'>"
                )
                new_message += open_tracking_img

        mail = EmailMessage(mail_subject, new_message, from_email, to=[recepient_mail])
        if attachment:
            mail.attach_file(attachment)
        mail.content_subtype = "html"
        mail.send()
        # Store the total sent emails inside the Sent model

        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_email()
            sent.save()
    except Exception as e:
        raise e


def generate_csv_file(model_name):
    # Generating timestamp
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y")

    # define the csv file name/path
    export_dir = "exported_data"
    file_name = f"exported_{model_name}_data_{timestamp}.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path
