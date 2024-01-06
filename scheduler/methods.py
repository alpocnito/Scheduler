from abc import ABC, abstractmethod
from input_pasrser import InputParser

class MBase(ABC):

    @abstractmethod
    def decide(self, queues, last_queue):
        """
        We have a free resource
        """
        pass

class MDumb(MBase):
    
    change_times_: list[list]
    work_times_  : list
    def __init__(self, ip: InputParser):
        self.change_times_ = ip.change_times
        self.work_times_ = ip.work_times
    
    def decide(self, queues, last_queue):
        """
        We have empty queues and new task arrived
        """
        print(queues)
        assert max(queues) != 0
        for i, queue in enumerate(queues):
            if queue != 0:
                return i


class MBrainLike(MBase):
    
    change_times_: list[list]
    work_times_  : list
    def __init__(self, ip: InputParser):
        self.change_times_ = ip.change_times
        self.work_times_ = ip.work_times
    
    def decide(self, queues, last_queue):
        """
        We have empty queues and new task arrived
        """
        print(queues)
        assert max(queues) != 0
        for i, queue in enumerate(queues):
            if queue != 0:
                return i
