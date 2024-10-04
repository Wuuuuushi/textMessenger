from Profile import Profile

def test_case1():
    p = Profile()
    p.add_message('Hi')
    assert p.messages == ['Hi']


def test_case2():
    p = Profile()
    p.add_my_messages('My sent message')
    assert p.my_messages == ['My sent message']


