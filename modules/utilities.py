def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")


def show_test(body):
    in_tag = False
    result = []
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            result.append(c)
    return ''.join(result)


def load(url):
    body = url.request()
    show(body)
