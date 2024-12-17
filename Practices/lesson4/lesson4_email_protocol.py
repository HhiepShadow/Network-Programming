import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
# dùng mật khẩu ứng dụng của email
# cách bật: https://support.google.com/accounts/answer/185833?hl=vi
 
def send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, body):
    # Tạo đối tượng MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
 
    # Thêm nội dung email
    msg.attach(MIMEText(body, 'plain'))
 
    # Kết nối đến máy chủ SMTP và gửi email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
 
if __name__ == "__main__":
 
    # Cấu hình thông tin email
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Cổng SMTP cho TLS
 
    # Nhập thông tin từ người dùng
    smtp_user = input("Enter your email: ")
    smtp_password = input("Enter your email password: ")
    to_email = input("Enter recipient email: ")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
 
    # Gửi email
    send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, body)