numbers=[]

for i in range(10):
    number=int(input(f'введите элементы {i+1}:'))
    numbers.append(number)

sr=sum(numbers)/len(numbers)

for i in range( len(numbers)):
    if numbers[i]>sr:
        numbers[i]=1
print('Среднее арифметическое:', sr)
print('Измененный массив:', numbers)
