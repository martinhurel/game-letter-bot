import csv
dico = []
with open("liste_francais.txt") as f:
    txt = csv.reader(f, delimiter='\n', encoding='utf-8')
    for line in txt:
        word = line[0]
        dico.append(word)

print(dico)