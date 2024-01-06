import logging

from events import Event, Events
from input_pasrser import InputParser
from common import get_default_logger
from methods import MBase

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

class Solver:
    change_times_: list[list]
    work_times_  : list
    events_      : Events
    busy_        : bool
    last_queue_  : int
    method_      : MBase

    # The number of items in each queue
    queues_: list

    def __init__(self, ip: InputParser, met: MBase):
        self.arrivals_ = ip.arrivals
        self.change_times_ = ip.change_times
        self.work_times_ = ip.work_times
        self.busy_ = False
        self.last_queue_ = 0
        self.events_ = Events()
        self.method_ = met
        for ar in self.arrivals_:
            self.events_.arrive(ar[0], ar[1])
        self.queues_ = [0] * len(self.work_times_)

    def run(self):
        while self.events_.size() != 0:
            ev = self.events_.get()
            self.solve_(ev)
        logger.warning("============ history ============")
        logger.warning("time : event   queue num   queues")
        logger.warning("")
        logger.warning(self.events_.history())
        logger.warning("=================================")

    def solve_(self, event: Event):
        curtime = event.timestamp
        if event.type == Event.ARRIVE:
            self.queues_[event.qnumber] += 1
            if self.busy_:
                return
            
            qnum = self.method_.decide(self.queues_, self.last_queue_)
            self.start_task_(qnum, curtime)
            self.busy_ = True
            return

        elif event.type == Event.LOAD_CH:
            self.busy_ = True
            self.last_queue_ = event.qnumber
            return
    
        elif event.type == Event.LOAD:
            self.busy_ = True
            self.last_queue_ = event.qnumber
            return

        elif event.type == Event.UNLOAD:
            self.busy_ = False
            self.queues_[event.qnumber] -= 1
            if max(self.queues_) == 0:
                return

            qnum = self.method_.decide(self.queues_, self.last_queue_)
            self.start_task_(qnum, curtime)
            self.busy_ = True
            return
        else:
            assert 0, "Unknwown event_type = " + event.type

    def start_task_(self, qnum: int, curtime: int):
        time_change = self.change_times_[self.last_queue_][qnum]
        time_work = self.work_times_[qnum]

        if self.last_queue_ != qnum:
            self.events_.load_ch(curtime, qnum)
        else:
            self.events_.load(curtime, qnum)
        
        self.events_.unload(curtime + time_change + time_work, qnum)
