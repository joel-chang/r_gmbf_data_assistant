from curses import flash
import re


# all of these could have more than one match, and i choose either the first or the last
# could refactor these again, but i don't want to for now
def check_body_fat(_str):
    # remember single digits
    # 18% 18bf bf:18 bf: 18 body fat: 18 bf18 %18 18ish "18 %"
    int_perc = re.compile(r'[^.^,]\d{1,2}[.,]?\d?\d?\s??%').findall(_str)
    perc_int = re.compile(r'%\d{1,2}').findall(_str)
    int_bf = re.compile(r'^[.,]\d{1,2}[.,]?\d?\d?\s??bf',flags=re.IGNORECASE).findall(_str)
    bf_int = re.compile(r'bf:??\s??\d{1,2}\D',flags=re.IGNORECASE).findall(_str)

    matches = int_bf + bf_int + int_perc + perc_int

    if len(matches) == 0: 
        # print(f"WARNING: {_str} doesn't have body fat.")
        return 'empty'
    new_bf = re.split('[.]|,', matches[0])[0][:]
    return ''.join(filter(str.isdigit, new_bf))

def check_age(_str):
    # more than 18 if possible
    # 32Y 32y F32 32F 32years "32 years old" age:32 age: 32 Age: 32 Age:32 "32 y" "32 Y"
    xx_y = re.compile(r'\d\d\s??y', flags=re.IGNORECASE).findall(_str)
    age_xx = re.compile(r'age:\s??\d\d', flags=re.IGNORECASE).findall(_str)
    xx_s = re.compile(r'\d\d\s??[fm]', flags=re.IGNORECASE).findall(_str)
    s_xx = re.compile(r'[mf]\d\d').findall(_str)

    matches = xx_y + age_xx + xx_s + s_xx
    if len(matches) == 0:
        # print(f"WARNING: {_str} doesn't contain age.")
        return 'empty'
    
    return ''.join(filter(str.isdigit, matches[-1]))


def check_sex(_str):
    # F M 32f f32 m32 M32 32m
    mat1 = re.compile(r'(\[[mf]\])', flags=re.IGNORECASE).findall(_str)
    mat2 = re.compile(r'(\([mf]\))', flags=re.IGNORECASE).findall(_str)
    mat3 = re.compile(r'(\s[mf]\s)', flags=re.IGNORECASE).findall(_str)
    mat4 = re.compile(r'(\d\d[fm])', flags=re.IGNORECASE).findall(_str)
    mat5 = re.compile(r'([fm]\d\d)', flags=re.IGNORECASE).findall(_str)
    mat6 = re.compile(r'female', flags=re.IGNORECASE).findall(_str)
    mat7 = re.compile(r'^f^emale', flags=re.IGNORECASE).findall(_str)

    matches = mat1 + mat2 + mat3 + mat4 + mat5 + mat6 + mat7
    if len(matches) == 0:
        # print(f"WARNING: {self.title} doesn't contain sex.")
        return 'empty'
    return ''.join(filter(str.isalpha, matches[-1]))

def check_height(_str):
    # [4-8]'|`|"
    # [0-13]'|`|"
    # [4-8]ft [0-11]in

    # imperial
    int_FTortilde_int_ = re.compile(r"([4-8]\s??['’”]\s??1?[0-9]?)", flags=re.IGNORECASE).findall(_str)
    int_fft = re.compile(r"([4-8]\s??ft.??\d\d??)").findall(_str)
    int_foot = re.compile(r"[4-8]\s?foot\s?[0-9]|1[0-1]").findall(_str)

    # metric
    cm = re.compile(r'[1-2][0-9][0-9]\s??cm', flags=re.IGNORECASE).findall(_str)
    m = re.compile(r'[1-2].[0-9][0-9]??\s?m', flags=re.IGNORECASE).findall(_str)

    matches = int_FTortilde_int_ + int_foot + m + cm + int_fft
    if len(matches) == 0:
        # print(f"WARNING: {self.title} doesn't contain height.")
        return 'empty'
    return matches[0].replace(' ', '')

def check_weight(_str):
    # imperial
    pounds = re.compile(r'\d\d\d??\s?pounds?', flags=re.IGNORECASE).findall(_str)
    lbs = re.compile(r'\d\d\d??\s??lbs??', flags=re.IGNORECASE).findall(_str)
    kilos = re.compile(r'\d\d\d??\s??k', flags=re.IGNORECASE).findall(_str)

    matches = pounds + kilos + lbs
    if len(matches) == 0:
        # print(f"WARNING: {self.title} doesn't contain weight.")
        return 'empty'
    # print(matches[0])
    return matches[0].replace(' ', '')

class TitleChecker:
    def __init__(self, _title):
        self.title = _title
        if self.title.count('/') > 2:
            self.title = self.title.replace('/', ' ')
        self.title_tok = self.title.split()
        self.body_fat = check_body_fat(self.title)
        self.age = check_age(self.title)
        self.sex = check_sex(self.title)
        self.height = check_height(self.title)
        self.weight = check_weight(self.title)
        self.is_valid = self.is_useful()

    def is_useful(self):
        points = 5
        points -= 1 if self.body_fat == 'empty' else 0
        points -= 1 if self.age == 'empty' else 0
        points -= 1 if self.sex == 'empty' else 0
        points -= 1 if self.height == 'empty' else 0
        points -= 1 if self.weight == 'empty' else 0
        return True if points else False

    def print_info(self):
        print(f"Title: {self.title}")
        print(f"Body Fat: {self.body_fat}")
        print(f"Age: {self.age}")
        print(f"Sex: {self.sex}")
        print(f"Height: {self.height}")
        print(f"Weight: {self.weight}")

    def get_info(self):
        res = ''
        res += f"   Title: {self.title}\n"
        res += f"   Body Fat: {self.body_fat}\n"
        res += f"   Age: {self.age}\n"
        res += f"   Sex: {self.sex}\n"
        res += f"   Height: {self.height}\n"
        res += f"   Weight: {self.weight}\n"
        return res
