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


def get_list1():
    lists = {
        "cs486": [[[690, 770], [510, 590]], [2, 4]],
        "cs451": [[[780, 860]], [2, 4]],
        "cs370": [[[960, 1040], [600, 680], [870, 950]], [1, 3]],
        "sci206": [[[1050, 1130]], [1, 3]],
        "china202r": [[[870, 950]], [1, 3]],
    }
    return lists


list = [
    "cs486",
    "cs451",
    "cs370",
    "sci206",
    "china202r",
]
