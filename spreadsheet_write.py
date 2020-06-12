s = ''
for i in range(1000):
    s += '=IMPORTRANGE("1g2Y4c2JnCA7IPKyUiSNASSKwfs9LlxsiRStKxoPImFU", "Form Responses 1!B'+ str(i+2) + '")\n'

with open("./spreadsheet_write.txt", mode='w') as f:
    f.write(s)