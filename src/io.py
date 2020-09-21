import csv
writeline = [[11, 12, 13, 14], [21, 22, 23, 24], [31, 32, 33, 34]]
with open('data/sample.csv', 'w') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    # csv.QUOTE_NONNUMERIC
    writer.writerows(writeline)

with open('data/sample.csv') as f:
    print(f.read())
