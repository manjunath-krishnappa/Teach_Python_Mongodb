import random
import uuid
import string
import datetime


def random_number(num1, num2):
    return random.randint(num1, num2)


def random_string_lowercase(size=6, chars=string.ascii_lowercase):
    return "".join(random.choice(chars) for _ in range(size))


def random_digits(size=6, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def datetime_now():
    # current_datetime = datetime.datetime.now()        # "2021-06-25T10:44:17.818587"
    # current_datetime = str(datetime.datetime.now())   # "2021-06-25T10:43:42.223015"
    current_datetime = str(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )  # "2021-06-25T10:45:03"
    return current_datetime


def get_uuid():
    return str(uuid.uuid4())
