# Problem 8: Alice sent the flag to Bob in an email. Bob's IMAP server is 192.168.14.24. Unfortunately for Bob, he didn't pick a very good password. In fact, his password is about the worst password that he might have chosen for his password. Log in to Bob's email using his password and retrieve the flag. Hint: The Subject line of the email is "FLAG".

import imaplib

mail = imaplib.IMAP4('192.168.14.24')
mail.login("bob", "password")
mail.select("inbox")
_, list = mail.search(None, "ALL")
list = list[0].split(' ')
flag = ""
for email in list:
    _, body = mail.fetch(email, '(RFC822)')
    if 'FLAG' in body[0][1]:
        print "found flag in " + email
        for line in body[0][1].split('\n'):
            if line.startswith('FLAG'):
                _, flag = line.split(' ')
    else:
        print "flag is not in " + email
print "Found flag: " + flag
