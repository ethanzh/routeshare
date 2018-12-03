import textract
text = textract.process('hi.pdf', encoding='ascii')
text = text.decode("utf-8") 
lines = text.split("\n")

for i in range(len(lines)):
    current_line = lines[i]
    if (len(current_line) > 0 and current_line[0] == " "):
        code = current_line[1:7]
        day = current_line[7:]
        # take second line, split time and building
        next_line = lines[i + 1]
        # sometimes next line only has one char
        data = next_line.split(" ")
        if len(data) > 4:
            # times are index 0, 2, building is 3
            times = (data[0], data[2])
            building = data[3]
            print(code, day, times, building)
        # the line after is the professor's name, so go ahead by 2 more (3 total)
        next_line = lines[i + 3]
        if (len(next_line) == 1):
            next_day = [next_line]
            next_line = lines[i + 4]
            data = next_line.split(" ")
            try:
                if len(data) > 4:
                    times = (data[0], data[2])
                    building = data[3]
                    print(" " * 6, day, times, building)
            except IndexError:
                print(data)
