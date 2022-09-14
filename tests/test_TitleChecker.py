from title_check import TitleChecker


def get_oneline_info(cur):
    res = f'TITLE_{cur.title.strip()}_BF_{cur.body_fat}_AGE_{cur.age}_SEX_{cur.sex}_HEIGHT_{cur.height}_WEIGHT_{cur.weight}_'
    return res

def test_data_pop():
    file = open("tests/test_log.txt", "r")

    lines = file.readlines()
    file.close()

    new = ''
    for line in lines:
        cur = TitleChecker(line)
        new+=f'{get_oneline_info(cur)}\n'


    with open('tests/test_output.txt', 'w') as f:
        f.write(new)

    expected = open("tests/test_expected_result.txt", 'r')
    actual = open("tests/test_output.txt", "r")


    expected_lines = expected.readlines()
    actual_lines = actual.readlines()

    assert len(expected_lines) == len(actual_lines), 'line number is different!'

    i = 0
    for actual_line, expected_line in zip(actual_lines, expected_lines):
        i += 1
        assert actual_line == expected_line, f'Diff at line {i}'

    print('No errors in title parsing.')