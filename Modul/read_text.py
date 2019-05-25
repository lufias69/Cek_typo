def read_text(alamat):
    lineList = list()
    with open(alamat, encoding = "ISO-8859-1") as f:
        for line in f:
            lineList.append(line.rstrip('\n'))
    return lineList