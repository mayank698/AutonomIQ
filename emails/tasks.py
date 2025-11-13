from automation_main.celery import app
from dataentry.utils import send_email_notification

# celery -A automation_main worker -l info --pool=solo


@app.task
def send_email_task(mail_subject, message, to_email, attachement, email_id):
    send_email_notification(mail_subject, message, to_email, attachement, email_id)
    return "Email sending task executed sucessfully."
