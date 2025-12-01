import smtplib
import os
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to: str, subject: str, body: str):
    """
    Sends an email using SMTP credentials from environment variables.
    Falls back to mock email if credentials are not set.
    Converts Markdown body to HTML for better formatting.
    """
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT")
    smtp_email = os.environ.get("SMTP_EMAIL")
    smtp_password = os.environ.get("SMTP_PASSWORD")

    # Convert Markdown to HTML
    html_body = markdown.markdown(body)

    if not all([smtp_server, smtp_port, smtp_email, smtp_password]):
        print("Warning: SMTP credentials not found in environment variables. Sending mock email.")
        print(f"--- MOCK EMAIL SENT ---")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Body (HTML Preview):\n{html_body[:500]}...")
        print(f"-----------------------")
        return True

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_email
        msg['To'] = to
        msg['Subject'] = subject

        # Attach both plain text and HTML versions
        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(html_body, 'html')

        msg.attach(part1)
        msg.attach(part2)

        # Connect to server
        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        server.login(smtp_email, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_email, to, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
