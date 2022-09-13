from data_population import DataPopulation

possible = DataPopulation()

class TitleChecker:
    def __init__(self, _title):
        self.title = _title
        if self.title.count('/') > 2:
            self.title = self.title.replace('/', ' ')
        self.title_tok = self.title.split()
        self.check_body_fat()
        self.check_age()
        self.check_sex()
        self.check_fm_age()
        self.check_height()
        self.check_weight()
        self.is_valid = self.is_useful()

    def check_fm_age(self):
        for fmage in possible.fmage:
            if fmage in self.title:
                self.age = ''.join(filter(str.isdigit, fmage))
                self.sex = fmage.replace(self.age, '')

    def check_body_fat(self):
        self.body_fat = "empty"
        for bf in possible.bfs:
            if bf in self.title:
                self.body_fat = ''.join(filter(str.isdigit, bf))
    
    def check_age(self):
        self.age = "empty"
        for age in possible.ages:
            if age in self.title:
                self.age = ''.join(filter(str.isdigit, age))

    def check_sex(self):
        self.sex = "empty"
        for sex_word in possible.sex_word:
            if sex_word in self.title:
                self.sex = sex_word
        for tok in self.title_tok:
            for sex in possible.sex:
                if sex == tok:
                    self.sex = tok[0].upper()

    def check_height(self):
        self.height = "empty"
        for height in possible.heights:
            if height in self.title:
                self.height = height
    
    def check_weight(self):
        self.weight = "empty"
        for weight in possible.weights:
            if weight in self.title:
                self.weight = weight

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

