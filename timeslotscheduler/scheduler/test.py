import random
import string

LIST_SIZE = 7
MAX_SECTION = 5


def generate_random_string():
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(10))

    return random_string


def get_lists():
    lists = [
        [
            sorted([random.randint(1, 1400), random.randint(1, 1400)])
            for _ in range(random.randint(1, MAX_SECTION))
        ]
        for _ in range(LIST_SIZE)
    ]

    ret = {}
    for slots in lists:
        ret[generate_random_string()] = slots

    return ret
