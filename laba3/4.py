n=list(map(int((input('введите эдементы массива через пробел:').split()))))
max_l=max(n)
min_l=min(n)
max_idx=n.index(max_l)
min_idx=n.index(min_l)
n[max_idx],n[min_idx]=n[min_idx],n[max_idx]
priint('Массив после замены:',n)
