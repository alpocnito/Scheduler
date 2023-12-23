import csv
import logging

from scheduler.common import get_default_logger

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

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
        logger.info('==== arrivals ====')
        logger.info('time - queue num')
        logger.info("")
        with open(arrivals_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                logger.info("{0:4} - {1:<2}".format(int(row[0]), int(row[1])))
                self.arrivals.append([int(row[0]), int(row[1])])
        logger.info('==================\n')

        self.change_times = []
        logger.info('==== change_times ====')
        with open(change_times_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                cur_row = [int(elem) for elem in row]
                logger.info(cur_row)
                self.change_times.append(cur_row)
        logger.info('======================\n')

        logger.info('==== work_times ====')
        self.work_times = []
        with open(work_times_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                cur_row = [int(elem) for elem in row]
                logger.info(cur_row)
                self.work_times = cur_row
        logger.info('=====================\n')

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
