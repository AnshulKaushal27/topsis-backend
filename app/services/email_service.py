from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
import os


def send_email_with_attachment(to_email, subject, body, attachment_path):
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

        message = Mail(
            from_email="parralexpie@gmail.com",  # sender (does not need to exist)
            to_emails=to_email,
            subject=subject,
            plain_text_content=body,
        )

        # Attach CSV
        with open(attachment_path, "rb") as f:
            encoded_file = base64.b64encode(f.read()).decode()

        attachment = Attachment(
            FileContent(encoded_file),
            FileName(os.path.basename(attachment_path)),
            FileType("text/csv"),
            Disposition("attachment"),
        )

        message.attachment = attachment

        response = sg.send(message)

        print("✅ SendGrid email sent:", response.status_code)

    except Exception as e:
        print("❌ SendGrid email error:", str(e))
