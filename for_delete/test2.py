def print_products(*args):
    l = [i for i in args if type(i) in (str,) and i.isalpha()]
    if len(l) == 0:
        print('Нет продуктов')
    else:
        for i in range(len(l)):
            print(f"{i+1}) {l[i]}")

print_products('Бананы', [1, 2], ('Соль',), 'Яблоки', '', 'Макароны', 5, True)