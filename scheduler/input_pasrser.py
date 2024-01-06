import csv
import logging

from common import get_default_logger
from random import choices

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

class InputParser:
    """
    Read tables in python lists

    arrivals = list[timestamp, queue number]
    change_times = matrix NxN with changes costs
    work_times = list with N elements, work time for each queue
    """
    arrivals_   : list[int, int]
    change_times_: list[list]
    work_times_  : list

    def __init__(self, arrivals_fn: str, change_times_fn: str, work_times_fn: str):
        """
        _fn means filenames of tables
        """
        self.arrivals_ = []
        logger.info('==== arrivals ====')
        logger.info('time - queue num')
        logger.info("")

        with open(arrivals_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                logger.info("{0:4} - {1:<2}".format(int(row[0]), int(row[1])))
                self.arrivals_.append([int(row[0]), int(row[1])])
        logger.info('==================\n')

        self.change_times_ = []
        logger.info('==== change_times ====')
        with open(change_times_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                cur_row = [int(elem) for elem in row]
                logger.info(cur_row)
                self.change_times_.append(cur_row)
        logger.info('======================\n')

        logger.info('==== work_times ====')
        self.work_times_ = []
        with open(work_times_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                cur_row = [int(elem) for elem in row]
                logger.info(cur_row)
                self.work_times_ = cur_row
        logger.info('=====================\n')

    @staticmethod
    def by_num(num: int):
        """
        Simplifies version of __init__
        """
        base_dir = "scheduler/data/in/"
        return InputParser(
            base_dir + "arrivals_" + str(num) + ".csv",
            base_dir + "change_times_" + str(num) + ".csv",
            base_dir + "work_times_" + str(num) + ".csv",
        )

    @property
    def arrivals(self):
        return self.arrivals_

    @property
    def change_times(self):
        return self.change_times_
    
    @property
    def work_times(self):
        return self.work_times_

class InputGenerator:
    arrivals_     : list[int, int]
    change_times_ : list[list]
    work_times_   : list

    def __init__(self, change_times, work_times):
        self.change_times_ = change_times
        self.work_times_ = work_times

    def generate_data(self, prob_step, prob_queues, num_samples):
        """
        prob_step - probability that a request will be generated 
            in one timestamp. For example, prob_step = 0.5 means that
            on avarage one request will be generated per two timesteps
        prob_queues - list with probabilities. prob_queues[i] contains the
            probability that a request will be arrived in the i queue.
            sum(prob_queues) must be == 1
        """
        num_queues = len(prob_queues)
        queues = choices(list(range(num_queues)), prob_queues, k=num_samples)
        times = choices([0, 1], [1-prob_step, prob_step], k=int(num_samples / prob_step))
        
        timestamps = [i for i, time in enumerate(times) if time != 0]
        queues = queues[:len(timestamps)]

        self.arrivals_ = list(map(list, zip(timestamps, queues)))
        print(len(self.arrivals_))
        print(sum(queues))

    def write(self, arrivals_fn: str, change_times_fn: str, work_times_fn: str):
        """
        _fn means filenames of tables
        """
        self.arrivals_ = []
        logger.info('==== arrivals ====')
        logger.info('time - queue num')
        logger.info("")

        with open(arrivals_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                logger.info("{0:4} - {1:<2}".format(int(row[0]), int(row[1])))
                self.arrivals_.append([int(row[0]), int(row[1])])
        logger.info('==================\n')

        self.change_times_ = []
        logger.info('==== change_times ====')
        with open(change_times_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                cur_row = [int(elem) for elem in row]
                logger.info(cur_row)
                self.change_times_.append(cur_row)
        logger.info('======================\n')

        logger.info('==== work_times ====')
        self.work_times_ = []
        with open(work_times_fn, newline='\n') as file:
            table = csv.reader(file, delimiter=',', quotechar='"')
            for row in table:
                cur_row = [int(elem) for elem in row]
                logger.info(cur_row)
                self.work_times_ = cur_row
        logger.info('=====================\n')
