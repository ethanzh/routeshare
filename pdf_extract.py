import textract
text = textract.process('test.pdf', encoding='ascii')
text = text.decode("utf-8") 
lines = text.split("\n")

for i in range(len(lines)):
    current_line = lines[i]
    if (len(current_line) > 0 and current_line[0] == " "):
        code = current_line[1:7]
        day = current_line[7:]
        print(day)

#for i in lines:
    #print(i)
