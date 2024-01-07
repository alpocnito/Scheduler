from scheduler.events import Event, Events
from scheduler.input_parser import InputParser
from scheduler.methods import MBase

class Solver:
    change_times_: list[list]
    work_times_  : list
    events_      : Events
    busy_        : bool

    # number of the last queue being in processed
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
        self.events_.arrives(self.arrivals_)
        self.queues_ = [0] * len(self.work_times_)

    def run(self) -> str:
        while self.events_.size() != 0:
            ev = self.events_.get()
            self.solve_(ev)
        out  = "time : event   queue num   queues\n"
        out += self.events_.history()
        print(self.events_.stats())
        self.method_.end()
        return self.events_.queues_distrib()

    def solve_(self, event: Event):
        curtime = event.timestamp
        if event.type == Event.ARRIVE:
            self.queues_[event.qnumber] += 1
            if self.busy_:
                return

            qnum = self.method_.load(self.queues_, self.last_queue_)
            self.start_task_(qnum, curtime)
            self.busy_ = True
            return

        if event.type == Event.LOAD_CH:
            self.busy_ = True
            self.last_queue_ = event.qnumber
            return

        if event.type == Event.LOAD:
            self.busy_ = True
            self.last_queue_ = event.qnumber
            return

        if event.type == Event.UNLOAD:
            self.busy_ = False
            self.queues_[event.qnumber] -= 1
            self.method_.unload(self.queues_)
            if max(self.queues_) == 0:
                return

            qnum = self.method_.load(self.queues_, self.last_queue_)
            self.start_task_(qnum, curtime)
            self.busy_ = True
            return

        assert 0, "Unknwown event_type = " + event.type

    def start_task_(self, qnum: int, curtime: int):
        time_change = self.change_times_[self.last_queue_][qnum]
        time_work = self.work_times_[qnum]

        if self.last_queue_ != qnum:
            self.events_.load_ch(curtime, qnum)
        else:
            self.events_.load(curtime, qnum)

        self.events_.unload(curtime + time_change + time_work, qnum)
