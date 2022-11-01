# Put the data into a list
# Match block by block

import csv
from lib2to3.pytree import convert

def GetData():
    data1, data2 = [], []

    with open('data1.csv', encoding="utf8") as f1, open('data2.csv',
                                                        encoding="utf8") as f2:
        csv_reader = csv.reader(f1)
        for line_no, line in enumerate(csv_reader, 1):
            if line_no != 1:
                data1.append(line)

        csv_reader = csv.reader(f2)
        for line_no, line in enumerate(csv_reader, 1):
            if line_no != 1:
                data2.append(line)

    return data1, data2
            
# Test muna natin without the approximation algo 

def MatchWithoutAppx(d1, d2) -> list:
    '''
        Constraints:
            - If one of the data in each block doesn't match, return False
            - else return True
    '''
    TruthList = []
    for i in range(0, len(d1)):
        for k in range(0, len(d1[0])):
            if d1[i][k] == d2[i][k]:
                TruthList.append('True')
            else:
                TruthList.append('False')

    return TruthList



def main():
    d1, d2 = GetData()
    print(MatchWithoutAppx(d1, d2))


if __name__ == '__main__':
    main()
    