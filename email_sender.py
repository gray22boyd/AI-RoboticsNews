import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
from typing import List, Optional
from config import (
    EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, 
    SMTP_SERVER, SMTP_PORT, EMAIL_SUBJECT
)

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.sender_email = EMAIL_SENDER
        self.password = EMAIL_PASSWORD
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        
    def send_digest(self, html_content: str, subject: str = None) -> bool:
        """Send the daily digest email"""
        if not subject:
            subject = EMAIL_SUBJECT
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = EMAIL_RECIPIENT
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.password)
                text = message.as_string()
                server.sendmail(self.sender_email, EMAIL_RECIPIENT, text)
            
            logger.info(f"Email sent successfully to {EMAIL_RECIPIENT}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_error_notification(self, error_message: str) -> bool:
        """Send error notification email"""
        subject = "AI News Monitor - Error Notification"
        
        html_content = f"""
        <html>
        <body>
            <h2>⚠️ AI News Monitor Error</h2>
            <p>An error occurred while generating the daily digest:</p>
            <pre>{error_message}</pre>
            <p>Please check the system logs for more details.</p>
        </body>
        </html>
        """
        
        return self.send_digest(html_content, subject)

if __name__ == "__main__":
    sender = EmailSender()
    test_html = "<html><body><h1>Test Email</h1><p>This is a test.</p></body></html>"
    success = sender.send_digest(test_html, "Test Subject")
    print(f"Email sent: {success}") 