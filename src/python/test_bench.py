from trivium import Trivium


def pytest_funcarg__input_data(request):
    """Key or IV input is here"""
    data = 0x0
    return data


def test_input_transformation(input_data):
    datatest = Trivium(0xFFF, 0x00)
    result = datatest._setLength(input_data)
    assert result == 00000000000000000000000000000000000000000000000000000000000000000000000000000000
