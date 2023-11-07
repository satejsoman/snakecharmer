from pathlib import Path
from getpass import getuser()
from email.mime.text import MIMEText
from socket import gethostname
from subprocess import Popen, PIPE
from dateutil.relativedelta import relativedelta

# a version of pathlib's mkdir that returns a path object
def mkdir(p: Path | str, *args, **kwargs):
    p = Path(p)
    kwargs = {'parents': True, "exist_ok": True} | kwargs
    p.mkdir(*args, **kwargs)
    return p

# send an email, assuming *nix and sendmail installed
def email(subject, body = "", recipient = None, sender = None):
    if sender is None:
        sender = f"{getuser()}@{gethostname()}"
    if recipient is None:
        recipient = sender
    msg = MIMEText(body)
    msg["To"] = recipient
    msg["From"] = sender
    msg["Subject"] = subject

    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin = PIPE, universal_newlines = True)
    p.communicate(msg.as_string())

# human readable time deltas
attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
def time_difference(*args, **kwargs):
    sep = kwargs.pop('sep', ' ')
    delta = relativedelta(*args, **kwargs)
    components = [f"{(getattr(delta, attr)} {attr if getattr(delta, attr) > 1 else attr[:-1]}" for attr in attrs if getattr(delta, attr)]
    return sep.join(components)
