import logging

from scheduler.common import get_default_logger
from scheduler.solver import Solver
from scheduler.input_parser import InputParser, InputGenerator
from scheduler.methods import MDumb, MBrainLike

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':

    ina = InputParser.by_tag(1)

    gen = InputGenerator(ina.change_times, ina.work_times)
    gen.generate_data(0.5, [0.1, 0.9], 10000)
    gen.write_by_tag(2)
    #met = MBrainLike(ina)
    #sol = Solver(ina, met)
    #sol.run()
