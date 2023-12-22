import csv
import os

class InputAnalyzer:
    """
    Read tables in python lists

    arrivals = list[timestamp, queue number]
    changeTimes = matrix NxN with changes costs
    workTimes = list with N elements, work time for each queue
    """
    arrivals   : list[int, int]
    changeTimes: list[list]
    workTimes  : list

    def __init__(self, arrivals_fn: str, changeTimes_fn: str, workTimes_fn: str):
        """
        _fn means filenames of tables
        """
        self.arrivals = []
        with open(arrivals_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                self.arrivals.append([int(elem) for elem in row])

        self.changeTimes = []
        with open(changeTimes_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                self.changeTimes.append([int(elem) for elem in row])

        self.workTimes = []
        with open(workTimes_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                self.workTimes.append([int(elem) for elem in row])

    @staticmethod
    def by_num(num: int):
        """
        Simplifies version of __init__
        """
        base_dir = "scheduler/data/in/"
        return InputAnalyzer(
            base_dir + "arrivals_" + str(num) + ".csv",
            base_dir + "changeTimes_" + str(num) + ".csv",
            base_dir + "workTimes_" + str(num) + ".csv",
        )




if __name__ == '__main__':
    ina = InputAnalyzer.by_num(1)
    print(ina.arrivals)
    print(ina.changeTimes)
    print(ina.workTimes)
