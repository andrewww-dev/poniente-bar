from http.server import BaseHTTPRequestHandler
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# CONFIGURATION (Loaded from Vercel Environment Variables)
SENDER_EMAIL = os.environ.get("sharyi.andriy@gmail.com")     # Your bot email (e.g., bookingbot@gmail.com)
SENDER_PASSWORD = os.environ.get("AnAr20112013!!")   # The App Password for that gmail
RECIPIENT_EMAIL = os.environ.get("sharyi.andriy@gmail.com")   # The Restaurant Owner's Email

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Read the data sent from the website
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        # 2. Extract info
        name = data.get('name', 'Unknown')
        date = data.get('date')
        time = data.get('time')
        guests = data.get('guests')
        notes = data.get('notes', 'None')

        # 3. Create the Email content
        subject = f"🔔 New Booking: {name} ({date} @ {time})"
        
        body = f"""
        NEW RESERVATION REQUEST
        -----------------------
        👤 Name:   {name}
        👥 Guests: {guests}
        📅 Date:   {date}
        ⏰ Time:   {time}
        📝 Notes:  {notes}
        -----------------------
        Please reply to this email or call the client to confirm.
        """

        # 4. Send Email via Gmail SMTP
        try:
            msg = MIMEMultipart()
            msg['From'] = f"Booking Bot <{SENDER_EMAIL}>"
            msg['To'] = RECIPIENT_EMAIL
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Connect to Gmail Server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
            server.quit()

            # 5. Success Response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

        except Exception as e:
            # Error Response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
