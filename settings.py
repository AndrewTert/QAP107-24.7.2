import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_pass')
valid_email_second_account = os.getenv('valid_email_second_account')