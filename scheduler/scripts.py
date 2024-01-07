import logging
import cProfile, pstats, io

import fire

from scheduler.logging_utils import get_default_logger
from scheduler.solver import Solver
from scheduler.input_parser import InputParser, InputGenerator
from scheduler.methods import METHODS

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

def run_algo_impl(algo_name: str, file_tag: int):
    """
    Run algorithm on input data
    algo_name - algorithm name
    file_tag - tag of input files
    """
    if algo_name not in METHODS:
        logger.critical("Unknown algorithm: " + algo_name)
        return []

    ina = InputParser.by_tag(file_tag, False)
    met = METHODS[algo_name](ina)
    sol = Solver(ina, met)
    out = sol.run()
    with open(ina.get_out_filename(), 'w') as f:
        print(out, file=f)
    return out

def run_algo():
    fire.Fire(run_algo_impl)

def gen_data_impl(prob_step, prob_queues, num_samples, read_tag, write_tag):
    """
    Generates input data and writes it to the file 
    prob_step, prob_queues, num_samples - see InputGenerator.generate_data
    write_tag - see InputGenerator.write_by_tag
    read_tag - file tags from which the change_times and work_times tables will be obtained
    """
    ina = InputParser.by_tag(read_tag, False)
    gen = InputGenerator(ina.change_times, ina.work_times)
    gen.generate_data(prob_step, list(prob_queues), num_samples)
    gen.write_by_tag(write_tag)
    logger.info("Data generated in the file tag " + str(write_tag))

def gen_data():
    fire.Fire(gen_data_impl)

def profiler():
    prof = cProfile.Profile()
    prof.enable()
    prof.runcall(run_algo)
    prof.disable()

    stream = io.StringIO()
    pstats.Stats(prof, stream=stream).sort_stats(
         pstats.SortKey.TIME, pstats.SortKey.CUMULATIVE
    ).print_stats(10)
    print(stream.getvalue())

if __name__ == '__main__':
    fire.Fire(run_algo_impl)
