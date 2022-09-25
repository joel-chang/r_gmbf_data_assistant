from title_check import (
    check_body_fat,
    check_age,
    check_height,
    check_sex,
    check_weight
)

def test_body_fat():
    tests = {
        '1%'    :'empty',  # no one has 1% body fat, prevents 11%
        '18%'   :'18',
        '1 %'   :'empty',
        '01%'   :'01',  # it's okay
        '1'     :'empty',
        'bf18 '  :'18',
        'bf: 18 ':'18',
        '18bf'  :'empty',  # in case of F18bf25%
        '18.99%':'18'
    }

    for _input, _output in tests.items():
        actual_output = check_body_fat(_input)
        print(_input)
        print(_output)
        assert isinstance(actual_output, str), f'{_input}: expected string, got {type(actual_output)}'
        assert actual_output == _output, f'{_input}: expected {_output}, got {actual_output}'
