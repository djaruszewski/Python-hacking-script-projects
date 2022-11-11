from pwn import *
import sys

# it might be more convienent to pass data on the command line,
# here we verify correct # of arguments and make obvious how to use the script
if len(sys.argv) != 2:
    print("Invalid arguments!")
    print(f">> {sys.argv[0]} <sha256sum>")
    exit()

wanted_hash = sys.argv[1]
password_file = "rockyou.txt"
attempts = 0

with log.progress(f"Attempting to hack: {wanted_hash}!\n") as p:
    # specify what we are attempting to crack
    with open(password_file, "r", encoding='latin-1') as password_list:
    #open file and specify encoding bc of the encoding of some of the passwords
        for password in password_list:
            password = password.strip("\n").encode('latin-1')
            password_hash = sha256sumhex(password)
            # use sha256sumhex() because we want in hex format bc 
            # that's the comparison we're making by encoding
            p.status(f"[{attempts}] {password.decode('latin-1')} == {password_hash}")
            if password_hash == wanted_hash:
                p.success(f"Password hash found after {attempts} attempts!, {password.decode('latin-1')} hashes to {password_hash}")
                exit()
            attempts += 1
        p.failure("Password hash not found!")
