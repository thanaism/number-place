import csv
# import os
# import sys
import pytest
# sys.path.insert(0, os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '..')))


@pytest.mark.parametrize('row_count', [
    10**1,
    10**2,
    10**3,
    10**4,
    10**5,
    10**6
])
def test_make_csv(row_count):
    with open('data/1000000_MONSTERS_ATTACK.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for i in range(row_count):
            row = [str(i) + '-' + str(j) for j in range(10)]
            writer.writerow(row)


@pytest.mark.parametrize('writeline', [
    [[11, 12, 13, 14], [21, 22, 23, 24], [31, 32, 33, 34]],
    [[11, 12, 13, 14], [21, 22, 23, 24], [31, 32, 33, 34]],
    [[11, 12, 13, 14], [21, 22, 23, 24], [31, 32, 33, 34]]
])
def test_use_writerows(writeline):
    with open('data/sample.csv', 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        # csv.QUOTE_NONNUMERIC
        writer.writerows(writeline)
    with open('data/sample.csv') as f:
        print(f.read())


if __name__ == '__main__':
    parameter = '-sv'
    pytest.main([parameter, __file__])
