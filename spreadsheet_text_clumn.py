s = ''
for i in range(1000):
    s += '=IMPORTRANGE("シートID", "フォームの回答 1!B'+ str(i+2) + '")\n'

with open("./spreadsheet_text_clumn.txt", mode='w') as f:
    f.write(s)