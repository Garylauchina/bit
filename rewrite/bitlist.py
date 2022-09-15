def dec(f):
    def make_list(*args,**kwargs):
        list1 = [f(*args,**kwargs)]
        return list1
    return make_list


@dec
def double(x):
    return x * 2


@dec
def key(x,y):
    return x,x*y


print(double(3))
print(key(3,6))
