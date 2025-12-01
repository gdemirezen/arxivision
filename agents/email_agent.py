from tools.email_tool import send_email

class EmailAgent:
    def send_report(self, to_email: str, content: str):
        print(f"EmailAgent: Sending report to {to_email}...")
        subject = "Weekly Academic Research Update"
        success = send_email(to_email, subject, content)
        if success:
            print("EmailAgent: Report sent successfully.")
        else:
            print("EmailAgent: Failed to send report.")
