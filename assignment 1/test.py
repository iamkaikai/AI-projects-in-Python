x = (3,3,1)
y = (1,0,0)

r = tuple(a - b for a, b in zip(x, y))

print(r)