import smtplib


class NotificationManager:
    def send_notification(self, user, text):

        with smtplib.SMTP("smtp.office365.com",587) as connection:
            connection.starttls()
            connection.login(user="my_email",password="password")
            connection.sendmail(
                from_addr="my_email",
                to_addrs=user,
                msg=f"Subject: Low price flight ALERT\n\n{text}"
            )
