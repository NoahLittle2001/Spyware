import smtplib
import ssl
import sys



def phis_mail(email_from, email_to,pswd):
    # Setup port number and server name
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    subject = "Trend Micro Update"
    message = """Dear user, \n\nTrendMicro needs an updated immediatelly to secure your computer from viruses. Click here: http://127.0.0.1:5500/Download%20Site/download.html"""
    # content of message
    email_message = f"Subject: {subject}\n\n{message}"  

    # Create context
    simple_email_context = ssl.create_default_context()
    try:
        # Connect to the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from, pswd)
        print("Connected to server :-)")

        # Send the actual email
        print(f"Sending email to - {email_to}")
        TIE_server.sendmail(email_from, email_to, email_message)
        print(f"Email successfully sent to - {email_to}")

    # If there's an error, print it out
    except Exception as e:
        print(e)

    # Close the port
    finally:
        TIE_server.quit()

if __name__ == "__main__":
    # sender = sys.argv[1]
    # receiver = sys.argv[2]
    # app = sys.argv[3]
    sender = ""
    receiver = ""
    app = ""
    phis_mail(sender, receiver, app)