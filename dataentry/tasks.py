from automation_main.celery import app
from django.core.management import call_command
from django.conf import settings
from .utils import send_email_notification, generate_csv_file

# celery -A automation_main worker -l info --pool=solo


@app.task
def import_data_task(full_path, model_name):
    try:
        call_command("importData", full_path, model_name)
    except Exception as e:
        raise e
    to_email = settings.DEFAULT_TO_EMAIL
    mail_subject = "Import Data"
    message = "Data imported successfully check your database."
    send_email_notification(mail_subject, message, [to_email])
    return "Data uploaded successfully."


@app.task
def export_data_task(model_name):
    try:
        call_command("exportData", model_name)
    except Exception as e:
        raise e

    file_path = generate_csv_file(model_name)
    # Send email with the attachement
    mail_subject = "Export data"
    message = "Data exported sucessfully check the attachment."
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, [to_email], attachment=file_path)
    return "Data exported sucessfully"
