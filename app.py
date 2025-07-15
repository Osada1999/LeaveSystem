from flask import Flask, render_template, request
from leave_mailer import send_leave_request_email, notify_hr
import uuid

app = Flask(__name__)
pending_requests = {}  # Simulates a database

@app.route("/", methods=["GET", "POST"])
def leave_form():
    if request.method == "POST":
        employee = request.form["employee"]
        employee_number = request.form["employee_number"]
        department = request.form["department"]
        leave_category = request.form["leave_category"]
        leave_start = request.form["leave_start"]
        leave_start_time = request.form["leave_start_time"]
        leave_end = request.form["leave_end"]
        leave_end_time = request.form["leave_end_time"]
        reason = request.form["reason"]
        request_id = str(uuid.uuid4())

        # Save request in memory
        pending_requests[request_id] = {
            "employee": employee,
            "employee_number": employee_number,
            "department": department,
            "leave_category": leave_category,
            "leave_start": leave_start,
            "leave_start_time": leave_start_time,
            "leave_end": leave_end,
            "leave_end_time": leave_end_time,
            "reason": reason
        }

        send_leave_request_email(
            request_id, employee, employee_number, department, leave_category,
            leave_start, leave_start_time, leave_end, leave_end_time, reason
        )
        return "Leave request submitted."

    return render_template("leave_form.html")

@app.route("/approve/<request_id>")
def approve(request_id):
    data = pending_requests.pop(request_id, None)
    if data:
        notify_hr(
            employee=data["employee"],
            department=data["department"],
            leave_start=data["leave_start"],
            leave_start_time=data["leave_start_time"],
            leave_end=data["leave_end"],
            leave_end_time=data["leave_end_time"],
            approved=True
        )
        return render_template("approval_result.html", result="approved")
    return "Invalid request ID"

@app.route("/reject/<request_id>")
def reject(request_id):
    data = pending_requests.pop(request_id, None)
    if data:
        notify_hr(
            employee=data["employee"],
            department=data["department"],
            leave_start=data["leave_start"],
            leave_start_time=data["leave_start_time"],
            leave_end=data["leave_end"],
            leave_end_time=data["leave_end_time"],
            approved=False
        )
        return render_template("approval_result.html", result="rejected")
    return "Invalid request ID"

if __name__ == "__main__":
    app.run(debug=True)
