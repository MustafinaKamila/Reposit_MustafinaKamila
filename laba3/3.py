s=input('введите текст')
words=s.split()
result=[ ]
for word in words:
    clean_word=word.strip('.,!/?:;''"()-')
    if not clean_word:
        continue
    if clean_word.lower().startswith('а') and clean_word.lower()/endwith('я'):
        result.append(clean_word)
print(result)