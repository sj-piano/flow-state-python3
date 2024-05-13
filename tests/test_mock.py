from flow_state.dog import Dog


def test_dog_bark():
    dog = Dog('Winston')
    assert dog.respond('Winston') == 'Woof'
