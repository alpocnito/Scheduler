import csv
import logging
import subprocess

from random import choices

from scheduler.logging_utils import get_default_logger

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

IN_DIR = "/data/in/"
OUT_DIR = "/data/out/"

class InputParser:
    """
    Read tables in python lists

    arrivals = list[timestamp, queue tag]
    change_times = matrix NxN with changes costs
    work_times = list with N elements, work time for each queue
    """

    arrivals_fn_     : str
    change_times_fn_ : str
    work_times_fn_   : str
    arrivals_        : list[int, int]
    change_times_    : list[list]
    work_times_      : list

    def __init__(self, arrivals_fn: str, change_times_fn: str, work_times_fn: str, logs_on=True):
        """
        arrivals_fn - filename for arrivals table
        change_times_fn - filename for change_times table
        work_times_fn - filename for work_times table
        """
        if not logs_on:
            logging.disable(logging.FATAL)

        self.arrivals_fn_ = arrivals_fn
        self.change_times_fn_ = change_times_fn
        self.work_times_fn_ = work_times_fn

        logger.info('==== arrivals ====')
        logger.info('time - queue num')
        logger.info("")

        self.arrivals_ = []
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
        logging.disable(logging.NOTSET)

    @staticmethod
    def by_tag(tag: int, logs_on=True):
        """
        Simplifies version of __init__, where
        arrivals_fn = arrivals_<tag>.csv
        change_times_fn =change_times_<tag>.csv
        work_times_fn = work_times_<tag>.csv
        """
        base_dir = InputParser.get_project_dir() + IN_DIR
        return InputParser(
            base_dir + "arrivals_" + str(tag) + ".csv",
            base_dir + "change_times_" + str(tag) + ".csv",
            base_dir + "work_times_" + str(tag) + ".csv",
            logs_on
        )

    @staticmethod
    def get_project_dir():
        return subprocess.getoutput("pwd")

    @property
    def arrivals(self):
        return self.arrivals_

    @property
    def change_times(self):
        return self.change_times_

    @property
    def work_times(self):
        return self.work_times_

    def get_out_filename(self):
        filename = self.arrivals_fn_[self.arrivals_fn_.rfind('/'):]
        return InputParser.get_project_dir() + OUT_DIR + filename

class InputGenerator:
    """
    Generates a large amount of the input data based on distribution
    """
    arrivals_     : list[int, int]
    change_times_ : list[list]
    work_times_   : list

    def __init__(self, change_times, work_times):
        self.change_times_ = change_times
        self.work_times_ = work_times

    def generate_data(self, prob_step, prob_queues, num_samples):
        """
        prob_step - the probability that a request will be generated 
            at a single timestamp. For example, prob_step = 0.5 means that
            on avarage one request will be generated in two time steps
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
        #print(len(self.arrivals_))
        #print(sum(queues))

    def write(self, arrivals_fn: str, change_times_fn: str, work_times_fn: str):
        """
        Writes generated input data to files

        arrivals_fn - filename for arrivals table
        change_times_fn - filename for change_times table
        work_times_fn - filename for work_times table
        """
        with open(arrivals_fn, 'w+', newline='\n') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            for row in self.arrivals_:
                writer.writerow(row)

        with open(change_times_fn, 'w+', newline='\n') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            for row in self.change_times_:
                writer.writerow(row)

        with open(work_times_fn, 'w+', newline='\n') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            writer.writerow(self.work_times_)

    def write_by_tag(self, tag: int):
        """
        Simplifies version of write, where
        arrivals_fn = arrivals_<tag>.csv
        change_times_fn =change_times_<tag>.csv
        work_times_fn = work_times_<tag>.csv
        """
        cur_dir = subprocess.getoutput("pwd")
        base_dir = cur_dir + OUT_DIR
        self.write(
            base_dir + "arrivals_" + str(tag) + ".csv",
            base_dir + "change_times_" + str(tag) + ".csv",
            base_dir + "work_times_" + str(tag) + ".csv",
        )
