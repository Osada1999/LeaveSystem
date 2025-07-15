# main.py
from leave_mailer import send_leave_request_email

# Example leave request
employee_name = "Lahiru Perera"
department = "IT"
leave_date = "2025-07-20"
reason = "Medical appointment"

send_leave_request_email(employee_name, department, leave_date, reason)
