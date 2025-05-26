import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import time
from flask import Flask, request
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import base64

# Initialize Flask app
app = Flask(__name__)

# Email configuration (will be set via Vercel environment variables)
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = "sales@automataxpro.site"

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

def generate_proposal_with_gemini(data):
    print("Generating proposal with Gemini...")
    process_name = data.get("processName", "Unknown Process")
    weekly_hours = data.get("weeklyHours", "N/A")
    employees_involved = data.get("employeesInvolved", "N/A")
    main_steps = data.get("mainSteps", "Not specified")
    tools_used = data.get("toolsUsed", "Not specified")

    # Create a prompt for Gemini
    prompt = f"""
    You are an expert in automation solutions. Generate a professional automation proposal for a client based on the following details:

    - Process Name: {process_name}
    - Weekly Hours Spent on Process: {weekly_hours}
    - Number of Employees Involved: {employees_involved}
    - Main Steps of the Process: {main_steps}
    - Tools Currently Used: {tools_used}

    The proposal should include:
    - A title ("AutomataX Automation Proposal")
    - A summary of the current process
    - A proposed automation solution with estimated time savings (assume 70% of weekly hours can be saved)
    - Benefits of the solution (e.g., efficiency gain of 40-60%)
    - Next steps for the client to proceed with AutomataX
    - A closing statement thanking the client

    Format the proposal as plain text with clear section headings.
    """

    try:
        response = model.generate_content(prompt)
        proposal = response.text.strip()
        print("Proposal generated successfully with Gemini")
        return proposal
    except Exception as e:
        print(f"Failed to generate proposal with Gemini: {str(e)}")
        # Fallback to manual proposal generation if Gemini fails
        weekly_hours_int = int(weekly_hours) if weekly_hours.isdigit() else 0
        time_savings = weekly_hours_int * 0.7 if weekly_hours_int else "N/A"
        return f"""
AutomataX Automation Proposal
=============================

Current Process Summary
-----------------------
Process Name: {process_name}
Weekly Hours: {weekly_hours}
Employees Involved: {employees_involved}
Main Steps: {main_steps}
Tools Used: {tools_used}

Proposed Automation Solution
----------------------------
- Automate repetitive tasks to save {time_savings} hours weekly.
- Integrate tools like {tools_used} for seamless operation.
- Expected efficiency gain: 40-60%.

Next Steps
----------
- Schedule a consultation with AutomataX to discuss implementation.
- Contact us at sales@automataxpro.site for more details.

Thank you for choosing AutomataX!
"""

def create_pdf(proposal_text):
    print("Creating PDF...")
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Set up the PDF
    c.setFont("Helvetica", 12)
    y = height - 50  # Start 50 units from the top

    # Split the proposal text into lines and write to PDF
    lines = proposal_text.split("\n")
    for line in lines:
        if y < 50:  # If we're near the bottom, start a new page
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50
        c.drawString(50, y, line)
        y -= 15  # Move down for the next line

    c.showPage()
    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    print("PDF created successfully")
    return pdf_data

def send_email(to_email, subject, body, pdf_data=None):
    print(f"Attempting to send email to {to_email}")
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Error: EMAIL_ADDRESS or EMAIL_PASSWORD not set in environment variables")
        return False

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach PDF if provided
    if pdf_data:
        pdf_part = MIMEApplication(pdf_data, _subtype="pdf")
        pdf_part.add_header("Content-Disposition", "attachment", filename="AutomataX_Proposal.pdf")
        msg.attach(pdf_part)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
                print("Connecting to SMTP server...")
                server.starttls()
                print("Starting TLS...")
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                print("Logged in to SMTP server")
                server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
                print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Email sending failed to {to_email} (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return False

@app.route("/api/generate-proposal", methods=["POST"])
def generate_proposal_endpoint():
    print("Function invoked")
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    try:
        print("Checking HTTP method...")
        if request.method != "POST":
            print("Method not allowed")
            return (
                json.dumps({"status": "error", "message": "Method not allowed"}),
                405,
                headers
            )

        print("Parsing request body...")
        if not request.data:
            print("Request body is empty")
            return (
                json.dumps({"status": "error", "message": "Request body is empty"}),
                400,
                headers
            )

        try:
            data = request.get_json()
            print(f"Request body parsed: {data}")
        except Exception as e:
            print(f"JSON decode error: {str(e)}")
            return (
                json.dumps({"status": "error", "message": "Invalid JSON in request body"}),
                400,
                headers
            )

        print("Validating required fields...")
        required_fields = ["processName", "weeklyHours", "employeesInvolved", "mainSteps", "toolsUsed", "email"]
        for field in required_fields:
            if field not in data or not data[field]:
                print(f"Missing field: {field}")
                return (
                    json.dumps({"status": "error", "message": f"Missing required field: {field}"}),
                    400,
                    headers
                )

        # Generate the proposal using Gemini
        proposal_text = generate_proposal_with_gemini(data)

        # Generate PDF
        pdf_data = create_pdf(proposal_text)

        # Send proposal to the user's email with PDF attachment
        user_email = data["email"]
        subject = "Your AutomataX Automation Proposal"
        print(f"Sending proposal email to {user_email}")
        if not send_email(user_email, subject, proposal_text, pdf_data):
            print("Failed to send proposal email")
            return (
                json.dumps({"status": "error", "message": "Failed to send proposal to your email"}),
                500,
                headers
            )

        # Send notification to sales team (plain text only)
        sales_subject = f"New Proposal Generated for {user_email}"
        sales_body = f"A new proposal has been generated:\n\n{proposal_text}"
        print(f"Sending notification email to {TO_EMAIL}")
        if not send_email(TO_EMAIL, sales_subject, sales_body):
            print("Failed to notify sales team, but user email was sent")

        print("Request processed successfully")
        return (
            json.dumps({"status": "success", "message": "Proposal generated and sent successfully"}),
            200,
            headers
        )

    except Exception as e:
        print(f"Server error: {str(e)}")
        return (
            json.dumps({"status": "error", "message": f"Server error: {str(e)}"}),
            500,
            headers
        )

if __name__ == "__main__":
    app.run()