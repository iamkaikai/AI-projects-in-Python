import random

def test():
    s = set()
    total = 0
    def recursive(n, depth=0):
        nonlocal total
        if n in s or total > 100 or depth > 100:
            print(s)
            print(total)
            return
        s.add(n)
        total += n
        recursive(random.randint(1, 10), depth+1)
    recursive(1)

test()
