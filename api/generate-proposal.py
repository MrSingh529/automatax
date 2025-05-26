import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Email configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = "sales@automataxpro.site"

def generate_proposal(data):
    process_name = data.get('processName', 'Unknown Process')
    weekly_hours = data.get('weeklyHours', 'N/A')
    employees_involved = data.get('employeesInvolved', 'N/A')
    main_steps = data.get('mainSteps', 'Not specified')
    tools_used = data.get('toolsUsed', 'Not specified')

    proposal = f"""
AutomataX Automation Proposal
=============================

Process Name: {process_name}
Weekly Hours: {weekly_hours}
Employees Involved: {employees_involved}
Main Steps: {main_steps}
Tools Used: {tools_used}

Proposed Automation Solution:
- Automate repetitive tasks to save {int(weekly_hours) * 0.7 if weekly_hours.isdigit() else 'N/A'} hours weekly.
- Integrate tools like {tools_used} for seamless operation.
- Expected efficiency gain: 40-60%.

Next Steps:
- Schedule a consultation with AutomataX to discuss implementation.
- Contact us at sales@automataxpro.site for more details.

Thank you for choosing AutomataX!
"""
    return proposal

def send_email(to_email, subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Error: EMAIL_ADDRESS or EMAIL_PASSWORD not set in environment variables")
        return False

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Email sending failed to {to_email}: {str(e)}")
        return False

def main(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    try:
        # Check the request method
        if event.get("httpMethod") != "POST":
            return {
                "statusCode": 405,
                "headers": headers,
                "body": json.dumps({"status": "error", "message": "Method not allowed"})
            }

        # Parse the request body
        body = event.get("body")
        if not body:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"status": "error", "message": "Request body is empty"})
            }

        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"status": "error", "message": "Invalid JSON in request body"})
            }

        # Validate required fields
        required_fields = ['processName', 'weeklyHours', 'employeesInvolved', 'mainSteps', 'toolsUsed', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"status": "error", "message": f"Missing required field: {field}"})
                }

        # Generate the proposal
        proposal_text = generate_proposal(data)

        # Send proposal to the user's email
        user_email = data['email']
        subject = "Your AutomataX Automation Proposal"
        if not send_email(user_email, subject, proposal_text):
            return {
                "statusCode": 500,
                "headers": headers,
                "body": json.dumps({"status": "error", "message": "Failed to send proposal to your email"})
            }

        # Send notification to sales team
        sales_subject = f"New Proposal Generated for {user_email}"
        sales_body = f"A new proposal has been generated:\n\n{proposal_text}"
        if not send_email(TO_EMAIL, sales_subject, sales_body):
            print("Failed to notify sales team, but user email was sent.")

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"status": "success", "message": "Proposal generated and sent successfully"})
        }

    except Exception as e:
        print(f"Server error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"status": "error", "message": f"Server error: {str(e)}"})
        }