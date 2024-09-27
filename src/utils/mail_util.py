from flask_mail import Message
from src import mail  # Import đối tượng mail đã được cấu hình trong app chính
import random

SENDER_EMAIL = "duynguyenn1711@gmail.com"


# Hàm gửi email OTP
def send_otp_email(recipient, otp):
    msg = Message(
        subject="OTP for Password Reset",
        sender=SENDER_EMAIL,  # Chỉ định người gửi
        recipients=[recipient],
    )
    msg.body = f"Your OTP is: {otp}. It is valid for 5 minutes."
    mail.send(msg)


def generate_otp():
    return "".join(random.choices("0123456789", k=6))
