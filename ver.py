def play(change):
    import random
    g = ['auto', 'horse', 'horse']
    x = random.randint(0, 2)
    if x == 1:
        g[2] = 0
    else:
        g[1] = 0
    if g[x] == 'auto':
        if change:
            return False
        else:
            return True
    else:
        if change:
            return True
        else:
            return False

# Проверка
lis = []
for i in range(100000000):
    lis.append(play(False))
print(sum(lis)/len(lis))


