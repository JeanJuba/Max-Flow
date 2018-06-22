def changer(list = []):
    list[:] = [x * 10 for x in list]
    print('List inside method: ', list)

a = [x * 2 for x in [1,2,3,4]]
print('List before method: ', a)
changer(a)
print('List after method: ', a)
