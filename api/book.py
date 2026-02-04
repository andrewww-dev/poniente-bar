from http.server import BaseHTTPRequestHandler
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# LOAD SECRETS
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASS")
RECIPIENT_EMAIL = os.environ.get("OWNER_EMAIL")

class handler(BaseHTTPRequestHandler):
    # 1. HANDLE BROWSER VISITS (GET Request)
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Server is running! Python is working.".encode('utf-8'))

    # 2. HANDLE FORM SUBMISSIONS (POST Request)
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Data Extraction
            name = data.get('name', 'Unknown')
            date = data.get('date')
            time = data.get('time')
            guests = data.get('guests')
            notes = data.get('notes', 'None')

            # Email Content
            subject = f"🔔 New Booking: {name}"
            body = f"Name: {name}\nGuests: {guests}\nDate: {date} @ {time}\nNotes: {notes}"

            # Sending Email
            msg = MIMEMultipart()
            msg['From'] = f"Booking Bot <{SENDER_EMAIL}>"
            msg['To'] = RECIPIENT_EMAIL
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
            server.quit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
