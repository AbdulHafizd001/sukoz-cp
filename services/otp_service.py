import random

otp_store = {}  # Simpan OTP sementara

def send_otp(email):
    otp = random.randint(100000, 999999)
    otp_store[email] = otp
    # Implement email sending logic
    print(f"OTP for {email}: {otp}")  # Debug
    return otp

def verify_otp(email, otp):
    return otp_store.get(email) == otp
