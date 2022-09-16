from title_check import TitleChecker

def test_body_fat():
    samples = []
    for i in range(4, 10):  # why? because if it's stupid but it works, then it's stupid but it works
        samples.append(f" {i}%")  # it fixes dealing with single digit percentages
        samples.append(f" {i} %")
    for i in range(10, 40):
        samples.append(f"{i}%")
        samples.append(f"{i} %")
    
    for sample in samples:
        cur_test = TitleChecker(sample)
        assert cur_test.body_fat != 'empty'