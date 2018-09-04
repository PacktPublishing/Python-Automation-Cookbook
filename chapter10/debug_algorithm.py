def valid(candidate):
    if candidate <= 1:
        return False

    lower = candidate - 1
    while lower > 1:
        if candidate / lower == candidate // lower:
            return False
        lower -= 1

    return True


assert valid(3)
assert not valid(15)
assert not valid(18)
assert not valid(50)
assert valid(53)
