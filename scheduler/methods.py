import logging
import random

from abc import ABC, abstractmethod

from scheduler.input_parser import InputParser
from scheduler.logging_utils import get_default_logger

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

class MBase(ABC):

    @abstractmethod
    def load(self, queues, last_queue):
        """
        We have NOT empty queues and new task arrived
        """
        pass

    @abstractmethod
    def unload(self, queues):
        """
        Queue states after unloading
        """
        pass

class MRandom(MBase):
    """
    On each iteration select random queue and load task from it
    """
    change_times_: list[list]
    work_times_  : list
    def __init__(self, ip: InputParser):
        self.change_times_ = ip.change_times
        self.work_times_ = ip.work_times

    def load(self, queues, last_queue):
        assert max(queues) != 0

        # get not empty queues
        numbered_queues = list(enumerate(queues))
        numbered_queues = list(filter(lambda elem: elem[1] != 0, numbered_queues))

        # get random queue
        random.shuffle(numbered_queues)
        return numbered_queues[0][0]

    def unload(self, queues):
        """
        Queue states after unloading
        """
        pass

class MSmart(MBase):
    """
    On each iteration continue to load previous queue
    If queue is empty, selecting queue with minimum change time
    """
    change_times_: list[list]
    work_times_  : list
    def __init__(self, ip: InputParser):
        self.change_times_ = ip.change_times
        self.work_times_ = ip.work_times

    def load(self, queues, last_queue):
        assert max(queues) != 0

        if queues[last_queue] != 0:
            return last_queue

        # Selecting minimum change time
        numbered_ch_times = list(enumerate(self.change_times_[last_queue]))
        numbered_ch_times.sort(key=lambda elem: elem[1])

        while queues[numbered_ch_times[0][0]] == 0:
            del numbered_ch_times[0]

        return numbered_ch_times[0][0]

    def unload(self, queues):
        """
        Queue states after unloading
        """
        pass

class State:
    """
    One state and operations on it
    """
    # Has a length equal to the number of queues
    # Shows the distribution of elements in queues
    # sum(elems_proportion) must be equal to 1
    elems_proportion_: list

    # Last queue processed
    last_queue_: int

    # The total number of elements if all queues
    num_elements_: int

    def __init__(self, queues, last_queue):
        self.num_elements_ = len(queues)
        self.elems_proportion_ = [elems / len(queues) for elems in queues]
        self.last_queue_ = last_queue

    def __eq__(self, rhs) -> bool:
        return self.elems_proportion_ == rhs.elems_proportion_ and \
               self.last_queue_ == rhs.last_queue_ and \
               self.num_elements_ == rhs.num_elements_

    @staticmethod
    def distance(st1, st2) -> float:
        """
        Distance between two States 
        """
        if st1.last_queue_ != st2.last_queue_:
            return -1

        ALPHA = 1.0
        BETA  = 1.0
        GAMMA = 0.01

        dist_elems_proportion = ALPHA * sum(
            abs(el1 - el2) ** BETA for el1, el2 in zip(st1.elems_proportion_, st2.elems_proportion_)
        )
        dist_total_elems = GAMMA * abs(st1.num_elements_ - st2.num_elements_)

        return dist_elems_proportion + dist_total_elems

    @property
    def num_elements(self) -> int:
        return self.num_elements_

class Remember:
    """
    Contains States, Actions and Results
    """

    # current_res = new_res * RESULTS_UPDATE_RATE + (1 - RESULTS_UPDATE_RATE) * old_res
    RESULTS_UPDATE_RATE = 0.2

    # Memory creation time
    timestamp_: int

    state_before_: State
    state_after_: State

    # Selected queue number
    action_: int
    # Result of action
    result_: int

    def __init__(self, timestamp, state_before, state_after, action):
        self.state_before_ = state_before
        self.state_after_ = state_after
        self.action_ = action
        self.timestamp_ = timestamp
        self.result_ = state_before.num_elements - state_after.num_elements

    def add_new_result(self, new_res: int, timestamp: int):
        self.result_ = new_res * Remember.RESULTS_UPDATE_RATE + (1 - Remember.RESULTS_UPDATE_RATE) * self.result_
        self.timestamp_ = timestamp

    def __eq__(self, rhs) -> bool:
        return self.timestamp_ == rhs.timestamp and \
               self.state_before_ == rhs.state_before_ and \
               self.state_after_ == rhs.state_after_ and \
               self.action_ == rhs.action_ and \
               self.result_ == rhs.result_

    @property
    def state_before(self) -> int:
        return self.state_before_

    @property
    def state_after(self) -> int:
        return self.state_after_

    @property
    def action(self) -> int:
        return self.action_

    @property
    def result(self) -> int:
        return self.result_

    @property
    def timestamp(self) -> int:
        return self.timestamp_

class Memory:
    """
    Contains Remembers
    """
    # if distance(state1, state2) < EQUAL_THRESHOLD then state1 == state2
    EQUAL_THRESHOLD = 0.5
    # if distance(state1, state2) < SIMILAR_THRESHOLD then state1 is similar to the state2
    SIMILAR_THRESHOLD = 1.0
    REMEMBER_LIFETIME = 1000

    memory_: list[Remember]
    queues_num_: int

    def __init__(self, queues_num: int):
        self.memory_ = []
        self.queues_num_ = queues_num

    def __len__(self):
        return len(self.memory_)

    def add_remember(self, new_rem: Remember):
        memory = self.get_sorted_memory(new_rem.state_before)

        for i, rem in enumerate(memory):
            distance_states_before = State.distance(new_rem.state_before, rem.state_before)

            if distance_states_before <= Memory.EQUAL_THRESHOLD and new_rem.action == rem.action:
                self.memory_[i].add_new_result(rem.result, rem.timestamp)
                return
            if distance_states_before > Memory.EQUAL_THRESHOLD:
                break
        self.memory_.append(new_rem)

    def find_alike(self, state_before: State) -> int:
        """
        Returns the number of similar states_before
        """
        ans = 0
        for rem in self.memory_:
            dist = State.distance(rem.state_before_, state_before)
            if dist == -1:
                continue
            ans += 1
        return ans

    def get_sorted_memory(self, base_state_before: State):

        mem_with_distance = []
        for rem in self.memory_:
            dist = State.distance(rem.state_before, base_state_before)
            if dist == -1:
                continue
            mem_with_distance.append([dist, rem])

        mem_with_distance.sort(key=lambda elem: elem[0])
        memory = [elem[1] for elem in mem_with_distance]

        return memory

    def update_res(self, old_rem: Remember, new_rem: Remember):
        for i, rem in enumerate(self.memory_):
            if rem == old_rem:
                self.memory_[i].add_new_result(new_rem.result, new_rem.timestamp)
                return
        assert 0

    def renew(self, cur_time: int):
        for rem in self.memory_:
            if cur_time - rem.timestamp_ > Memory.REMEMBER_LIFETIME:
                self.memory_.remove(rem)

    def get_action(self, state_before: State) -> Remember:
        memory = self.get_sorted_memory(state_before)
        assert len(memory) != 0

        similar_memory = []
        similar_memory.append(memory[0])

        for i in range(1, len(memory)):
            if State.distance(memory[i].state_before, state_before) <= Memory.SIMILAR_THRESHOLD:
                similar_memory.append(memory[i])
            else:
                break

        similar_memory.sort(key=lambda rem: -rem.result)
        number = min(int(random.expovariate(1)), len(similar_memory) - 1)

        return similar_memory[number]

class MBrainLike(MBase):
    change_times_: list[list]
    work_times_  : list
    num_queues_  : int
    memory_      : Memory
    memory_size_ : int
    timestamp_   : int

    created_new_remember_: bool
    last_state_before_   : State
    last_action_         : int
    last_rem_            : Remember

    # Probability of creating a new Remember
    CREATE_PROB = 0.2

    def __init__(self, ip: InputParser):
        self.change_times_ = ip.change_times
        self.work_times_ = ip.work_times
        self.num_queues_ = len(self.work_times_)
        self.memory_ = Memory(self.num_queues_)
        self.memory_size_ = 10 ** (self.num_queues_)
        self.timestamp_ = 0

    def random_action(self) -> int:
        action = random.randrange(0, self.num_queues_)
        self.created_new_remember_ = True
        self.last_action_ = action
        return action

    def load(self, queues, last_queue):
        assert max(queues) != 0

        state_before = State(queues, last_queue)
        self.last_state_before_ = state_before

        # Absolutely new Remember
        if self.memory_.find_alike(state_before) == 0:
            return self.random_action()

        # We tend to create new Remembers if our memory is not full
        if len(self.memory_) != self.memory_size_:
            if random.random() <= MBrainLike.CREATE_PROB:
                return self.random_action()

        # Select an existing Remember
        rem = self.memory_.get_action(state_before)
        self.created_new_remember_ = False
        self.last_rem_ = rem
        self.last_action_ = rem.action
        return rem.action

    def unload(self, queues):
        state_after = State(queues, self.last_action_)
        rem = Remember(self.timestamp_, self.last_state_before_, state_after, self.last_action_)

        if self.created_new_remember_:
            self.memory_.add_remember(rem)
        else:
            self.memory_.update_res(self.last_rem_, rem)

        self.memory_.renew(self.timestamp_)
        self.timestamp_ += 1

METHODS = {
    "MRandom" : MRandom,
    "MSmart" : MSmart,
    "MBrainLike": MBrainLike
}
