from smtplib import SMTP
import datetime

SERVER = "localhost"
smtp = SMTP(SERVER, 26)
smtp.set_debuglevel(0)
smtp.connect()

from_addr = "marcellahastings@gmail.com" #input from form
to_addr = "marcellahastings@gmail.com"    #andrea

subj = "New Commission"
date = datetime.datetime.now()

message_text = "Dear Marcella,\nThis is a new message\n\nBye\n"
message = """\
    From: %s\
    Subject: %s\
    Date: %s\n\
    %s
    """ % (from_addr, subj, date, message_text)

smtp.sendmail(from_addr, to_addr, message)
smtp.quit()

