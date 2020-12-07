import random
import string


def _get_random_value(t=None):
    case_map = {
        "int":  random.randint(-2 ** 63, 2 ** 63 - 1),
        "float":  random.uniform(-2 ** 63, 2 ** 63 - 1),
        "str":  ''.join(random.sample(string.ascii_letters + string.digits, random.randint(0, 32))),
        "array":  [''.join(random.sample(string.ascii_letters + string.digits, random.randint(0, 32))) for _ in range(random.randint(0, 32))],
        "map":  {''.join(random.sample(string.ascii_letters + string.digits, random.randint(0, 32))): ''.join(random.sample(string.ascii_letters + string.digits, random.randint(0, 32))) for _ in
                        range(random.randint(0, 64))},
        "bool":  random.choice([True, False])
    }
    type_arr = ["str", "int", "map", "array", "float", "bool"]
    if t:
        ret = case_map.get(t)
    else:
        ret = case_map.get(random.choice(type_arr))
    return ret


if __name__ == '__main__':
    print(_get_random_value())