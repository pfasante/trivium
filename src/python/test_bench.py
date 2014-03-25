from trivium import Trivium


def pytest_funcarg__input_data(request):
    """Key or IV input is here"""
    data = 0x0
    return data


def test_input_transformation(input_data):
    datatest = Trivium("X", "X")
    result = datatest._setlength(input_data)
    assert result == 00000000000000000000000000000000000000000000000000000000000000000000000000000000
