from scheduler.events import *
from scheduler.input_pasrser import *
from scheduler.common import get_default_logger

logger = get_default_logger(__name__)
logger.setLevel(logging.INFO)

class Solver:
    change_times_: list[list]
    work_times_  : list
    events_      : Events
    busy_        : bool
    last_queue_  : int

    # The number of items in each queue
    queues_: list

    def __init__(self, ip: InputParser):
        self.arrivals_ = ip.arrivals
        self.change_times_ = ip.change_times
        self.work_times_ = ip.work_times
        self.busy_ = False
        self.last_queue_ = 0
        self.events_ = Events()
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
        if event.type == EVENT_ARRIVE:
            if self.busy_:
                self.queues_[event.qnumber] += 1
                return
            else:
                time_change = self.change_times_[self.last_queue_][event.qnumber]
                time_work = self.work_times_[event.qnumber]

                if time_change != 0:
                    self.events_.change_type_st(curtime, event.qnumber)
                    self.events_.change_type_en(curtime + time_change, event.qnumber)
                self.events_.load(curtime + time_change, event.qnumber)
                self.events_.unload(curtime + time_change + time_work, event.qnumber)
                self.busy_ = True
                return

        elif event.type == EVENT_CHANGE_TYPE_ST:
            self.busy_ = True
            return

        elif event.type == EVENT_CHANGE_TYPE_EN:
            self.busy_ = False
            return

        elif event.type == EVENT_LOAD:
            self.busy_ = True
            self.last_queue_ = event.qnumber
            return

        elif event.type == EVENT_UNLOAD:
            self.busy_ = False
            qnum = -1
            for i, queue in enumerate(self.queues_):
                if queue != 0:
                    qnum = i
                    break
            if qnum == -1:
                return

            self.queues_[qnum] -= 1
            time_change = self.change_times_[self.last_queue_][qnum]
            time_work = self.work_times_[qnum]

            if time_change != 0:
                self.events_.change_type_st(curtime, qnum)
                self.events_.change_type_en(curtime + time_change, qnum)
            self.events_.load(curtime + time_change, qnum)
            self.events_.unload(curtime + time_change + time_work, qnum)
            self.busy_ = True
            return
        else:
            assert 0, "Unknwown event_type = " + event.type