from pwn import *
import sys

if len(sys.argv) != 2:
    print("Invalid arguments!")
    print(f">> {sys.argv[0]} <sha256sum>")
    exit()

wanted_hash = sys.argv[1]
password_file = "rockyou.txt"
attempts = 0

with log.progress(f"Attempting to hack: {wanted_hash}!\n") as p:
    with open(password_file, "r", encoding='latin-1') as password_list:
        for password in password_list:
            password = password.strip("\n").encode('latin-1')
            password_hash = sha256sumhex(password)
            p.status(f"[{attempts}] {password.decode('latin-1')} == {password_hash}")
            if password_hash == wanted_hash:
                p.success(f"Password hash found after {attempts} attempts!, {password.decode('latin-1')} hashes to {password_hash}")
                exit()
            attempts += 1
        p.failure("Password hash not found!")
