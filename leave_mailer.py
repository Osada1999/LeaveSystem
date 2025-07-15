import smtplib
from email.mime.text import MIMEText
from config import HR_MANAGER_EMAIL, HR_ASSISTANT_EMAIL, DEPARTMENT_HEADS
from dotenv import load_dotenv
import os

load_dotenv()
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASS")

def send_leave_request_email(request_id, employee, employee_number, department, leave_category,
                             leave_start, leave_start_time, leave_end, leave_end_time, reason):
    dept_head = DEPARTMENT_HEADS.get(department)
    recipients = [dept_head]

    approve_link = f"http://localhost:5000/approve/{request_id}"
    reject_link = f"http://localhost:5000/reject/{request_id}"

    subject = f"Leave Request from {employee}"

    body = f"""
    Dear {department} Department Head,

    A new leave request has been submitted.

    📌 Employee Name: {employee}
    🆔 Employee Number: {employee_number}
    🏢 Department: {department}
    🗂️ Leave Category: {leave_category}
    📅 Leave Period: From {leave_start} {leave_start_time} to {leave_end} {leave_end_time}
    📝 Reason: {reason}

    ➕ Approve: {approve_link}
    ➖ Reject: {reject_link}

    Regards,  
    Leave Request System
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("mail.vintageteas.lk", 465) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(msg["From"], recipients, msg.as_string())


def notify_hr(employee, department, leave_start, leave_start_time, leave_end, leave_end_time, approved):
    if not approved:
        return  # Notify HR only on approval

    subject = f"Leave Approved: {employee}"

    body = f"""
    Dear HR Team,

    The following leave request has been approved by the department head:

    📌 Employee Name: {employee}
    🏢 Department: {department}
    📅 Leave Period: From {leave_start} {leave_start_time} to {leave_end} {leave_end_time}

    Please update your records accordingly.

    Regards,  
    Leave Request System
    """

    recipients = [HR_MANAGER_EMAIL, HR_ASSISTANT_EMAIL]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("mail.vintageteas.lk", 465) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(msg["From"], recipients, msg.as_string())
