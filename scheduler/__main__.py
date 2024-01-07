from scheduler.input_parser import InputParser, InputGenerator
from scheduler.methods import State, MBrainLike

if __name__ == '__main__':

    st1 = State([0, 63], 1)
    st2 = State([0, 85], 1)

    print(st1)
    print(st2)

    print(State.distance(st1, st2))

