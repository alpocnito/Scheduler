import logging

from scheduler.common import get_default_logger
from scheduler.solver import Solver
from scheduler.input_pasrser import InputParser

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':

    ina = InputParser.by_num(1)
    sol = Solver(ina)

    sol.run()
