from scheduler.solver import Solver
from scheduler.input_pasrser import InputParser

if __name__ == '__main__':
    ina = InputParser.by_num(1)
    sol = Solver(ina)

    sol.run()
