import ds_messenger

def test_case1():
    y = ds_messenger.DirectMessenger()
    y.username = 'Milky'
    y.password = 'John'
    x = y.send('Die', 'Milky')
    assert x == True

def test_case2():
    y = ds_messenger.DirectMessenger()
    y.username = 'Milky'
    y.password = 'John'
    x = y.retrieve_all()
    assert type(x) == list

def test_case3():
    y = ds_messenger.DirectMessenger()
    y.username = 'Milky'
    y.password = 'John'
    x = y.retrieve_new()
    assert type(x) == list



if __name__ == "__main__":
    test_case1()
    test_case2()
    test_case3()
