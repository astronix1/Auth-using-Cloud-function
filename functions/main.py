from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore, auth
import smtplib
from email.mime.text import MIMEText
import random

initialize_app()

SENDER_EMAIL = "-----" 
APP_PASSWORD = "----" 


@https_fn.on_call()
def send_email_otp(req: https_fn.CallableRequest) -> dict:
    recipient_email = req.data.get("email")
    if not recipient_email:
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT, message="Email required")

    otp = str(random.randint(100000, 999999))

    db = firestore.client()
    db.collection("otp_codes").document(recipient_email).set({
        "otp": otp,
        "createdAt": firestore.SERVER_TIMESTAMP
    })

    print(f"Attempting to send email to {recipient_email}...")
    
    try:
        msg = MIMEText(f"Your login code is: {otp}")
        msg['Subject'] = "Your Login Code"
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email


        print("Connecting to smtp.gmail.com...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        
        print("Logging in...")
        server.login(SENDER_EMAIL, APP_PASSWORD)
        
        print("Sending mail...")
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        
        print("SUCCESS: Email sent!")
        return {"success": True}
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"!!! AUTH ERROR: Google rejected the password {e}")
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INTERNAL, message="Auth Failed: Check Terminal")
        
    except Exception as e:
        print(f"!!! CRASH: {type(e).__name__}: {e}")
        raise https_fn.HttpsError(code=https_fn.FunctionsErrorCode.INTERNAL, message=f"Server Error: {str(e)}")

@https_fn.on_call()
def verify_email_otp(req: https_fn.CallableRequest) -> dict:
    email = req.data.get("email")
    code = req.data.get("code")

    db = firestore.client()
    doc_ref = db.collection("otp_codes").document(email)
    doc = doc_ref.get()

    if not doc.exists:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.NOT_FOUND,
            message="No OTP found"
        )

    data = doc.to_dict()
    if data.get("otp") != code:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
            message="Incorrect OTP"
        )

    try:
        user = auth.get_user_by_email(email)
        uid = user.uid
    except:
        user = auth.create_user(email=email)
        uid = user.uid

    custom_token = auth.create_custom_token(uid)

    if isinstance(custom_token, bytes):
        custom_token = custom_token.decode("utf-8")

    doc_ref.delete()

    return {"token": custom_token}
