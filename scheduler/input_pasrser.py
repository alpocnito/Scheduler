import csv


class InputParser:
    """
    Read tables in python lists

    arrivals = list[timestamp, queue number]
    change_times = matrix NxN with changes costs
    work_times = list with N elements, work time for each queue
    """
    arrivals   : list[int, int]
    change_times: list[list]
    work_times  : list

    def __init__(self, arrivals_fn: str, change_times_fn: str, work_times_fn: str):
        """
        _fn means filenames of tables
        """
        self.arrivals = []
        with open(arrivals_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                self.arrivals.append([int(elem) for elem in row])

        self.change_times = []
        with open(change_times_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                self.change_times.append([int(elem) for elem in row])

        self.work_times = []
        with open(work_times_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                self.work_times = [int(elem) for elem in row]

    @staticmethod
    def by_num(num: int):
        """
        Simplifies version of __init__
        """
        base_dir = "/home/ron/dev/test/Scheduler/scheduler/data/in/"
        return InputParser(
            base_dir + "arrivals_" + str(num) + ".csv",
            base_dir + "change_times_" + str(num) + ".csv",
            base_dir + "work_times_" + str(num) + ".csv",
        )
