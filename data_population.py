# regex would probably be better for this
# first percentages

class DataPopulation:
    def __init__(self):
        self.bfs = []
        self.ages = []
        self.sex = []
        self.sex_word = []
        self.heights = []
        self.weights = []
        self.fmage = []

        # this seems like a common format as well
        for i in range(18, 70):
            self.fmage.append(f"{i}M")
            self.fmage.append(f"{i}F")
            self.fmage.append(f"M{i}")
            self.fmage.append(f"F{i}")

        # create possible body fat
        for i in range(4, 10):  # why? because if it's stupid but it works, then it's stupid but it works
            self.bfs.append(f" {i}%")  # it fixes dealing with single digit percentages
            self.bfs.append(f" {i} %")
            self.bfs.append(f" {i}ish")  # e.g. won't think that 18% is both 18% and 8%
        for i in range(10, 40):
            self.bfs.append(f"{i}%")
            self.bfs.append(f"{i} %")
            self.bfs.append(f"{i}ish")

        # for age
        for i in range(16, 40):
            self.ages.append(f"{i} years old")
            self.ages.append(f"{i}y")
            self.ages.append(f"{i}Y")
            self.ages.append(f"Age: {i}")
            self.ages.append(f"Age:{i}")
            self.ages.append(f"age: {i}")
            self.ages.append(f"age:{i}")
            self.ages.append(f"{i} y/o")
            self.ages.append(f"{i}y/o")
            self.ages.append(f"{i} Y/O")
            self.ages.append(f"{i} yo")
            self.ages.append(f"{i}yo")

        # for sex
        self.sex = ['f', 'F', 'm', 'M', '[M]', '[F]', '(F)', '(M)']
        self.sex_word = ['male', 'Male', 'female', 'Female']

        # retard units
        for i in range(4, 8):
            self.heights.append(f"{i}'")
            self.heights.append(f"{i}’")  # damn you tildes
            self.heights.append(f"{i}”")  # just ”murica things
            self.heights.append(f"{i}ft")
            self.heights.append(f"{i} ft")
            for j in range(0, 13):
                self.heights.append(f"{i}'{j}")
                self.heights.append(f"{i}’{j}")
                self.heights.append(f"{i}’ {j}")
                self.heights.append(f"{i}”{j}")
                self.heights.append(f"{i}” {j}")
                self.heights.append(f"{i}' {j}")
                self.heights.append(f"{i}ft{j}")
                self.heights.append(f"{i} ft {j}")
                self.heights.append(f"{i}ft{j}in")
                self.heights.append(f"{i}ft {j}in")
                self.heights.append(f"{i}ft. {j}in")
                self.heights.append(f"{i}ft {j}in.")
                self.heights.append(f"{i}ft. {j}in.")
                self.heights.append(f"{i} Foot {j}")
                self.heights.append(f"{i} foot {j}")

        # metric
        for i in range(100, 220):
            self.heights.append(f"{i}cm")
            self.heights.append(f"{i} cm")
            self.heights.append(f"{i}CM")
            self.heights.append(f"{i} CM")
            self.heights.append(f"{i/100}m")
            self.heights.append(f"{i/100} m")
            self.heights.append(f"{i/100}M")
            self.heights.append(f"{i/100} M")
            self.heights.append(f"{i} inches")

        # for weight
        for i in range(50, 300):
            self.weights.append(f"{i}lb")
            self.weights.append(f"{i} lb")
            self.weights.append(f"{i}lbs")
            self.weights.append(f"{i} lbs")
            self.weights.append(f"{i} LBS")
            self.weights.append(f"{i}LBS")
            self.weights.append(f"{i} pounds")

        for i in range(50, 250):
            self.weights.append(f"{i}kg")
            self.weights.append(f"{i} kg")
            self.weights.append(f"{i}KG")
            self.weights.append(f"{i} KG")
            self.weights.append(f"{i} kilo")

        for i in range(500, 2500):
            self.weights.append(f"{format(i/10, '.1f')}kg")
            self.weights.append(f"{format(i/10, '.1f')} kg")
            self.weights.append(f"{format(i/10, '.1f')}KG")
            self.weights.append(f"{format(i/10, '.1f')} KG")
            self.weights.append(f"{format(i/10, '.1f')} kilo")
