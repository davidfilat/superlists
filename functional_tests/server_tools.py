import re
from subprocess import call, getoutput


def reset_database():
    call("heroku run 'python manage.py flush --no-input'", shell=True)


def create_session_on_server(email):
    output = getoutput(f"heroku run 'python manage.py create_session {email}'")
    key_search = re.search(r"([a-z|0-9]){32}", output)
    return key_search.group(0)
