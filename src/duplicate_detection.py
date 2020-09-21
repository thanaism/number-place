a = 'saldkfjaskjfwioaowignaoknvlakajsfjlaskjflkjsldfkjlkj'
b = 'saldkfjaskjfwioaowignaoknvljkajsfjlaskjflkjsldfkjlkj'

for index, value in enumerate(zip(a, b)):
    # if i != j:
    #     print(False)
    # print(index, value)
    if value[0] != value[1]:
        print(f'{index}: \'{value[0]}\' & \'{value[1]}\' are different.')
