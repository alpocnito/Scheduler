import logging

from common import get_default_logger
from solver import Solver
from input_pasrser import InputParser, InputGenerator
from methods import MDumb, MBrainLike

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':

    ina = InputParser.by_num(1)
    
    gen = InputGenerator(ina.change_times, ina.work_times)
    gen.generate_data(0.5, [0.1, 0.9], 10000)
    #met = MBrainLike(ina)
    #sol = Solver(ina, met)
    #sol.run()
