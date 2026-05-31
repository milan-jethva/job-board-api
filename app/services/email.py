# app/services/email.py — no fastapi-mail needed
import aiosmtplib
from email.mime.text import MIMEText
from app.config import settings

async def send_email(to: str, subject: str, body: str):
    message = MIMEText(body, "plain")
    message["From"]    = settings.MAIL_FROM
    message["To"]      = to
    message["Subject"] = subject

    await aiosmtplib.send(
        message,
        hostname = settings.MAIL_SERVER,
        port     = settings.MAIL_PORT,
        username = settings.MAIL_USERNAME,
        password = settings.MAIL_PASSWORD,
        start_tls = True,
    )

async def send_application_email(applicant_email: str, job_title: str):
    await send_email(
        to      = applicant_email,
        subject = f"Application Received - {job_title}",
        body    = f"Your application for {job_title} has been received. We will get back to you soon."
    )

async def send_status_update_mail(applicant_email: str, job_title: str, status: str):
    await send_email(
        to      = applicant_email,
        subject = f"Application Update - {job_title}",
        body    = f"Your application for {job_title} has been {status}."
    )