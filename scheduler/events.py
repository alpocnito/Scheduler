EVENT_ARRIVE = "arrive"
EVENT_LOAD = "load"
EVENT_UNLOAD = "unload"
EVENT_CHANGE_TYPE_ST = "ch_type_st"
EVENT_CHANGE_TYPE_EN = "ch_type_en"

class Event:
    timestamp_: int

    # On of the EVENT_ types
    type_: str

    # The number of the queue associated with the event
    qnumber_: int

    def __init__(self, timestamp, ttype, qnumber):
        self.timestamp_ = timestamp
        self.type_ = ttype
        self.qnumber_ = qnumber

    def __repr__(self) -> str:
        return "{0:4} : {1:10} {2:1}".format(
            self.timestamp_, self.type_, self.qnumber_
        )

    def type_gt_(self, other):
        if self.type_ == EVENT_CHANGE_TYPE_EN:
            return False
        if other.type == EVENT_CHANGE_TYPE_EN:
            return True
        if self.type_ == EVENT_UNLOAD:
            return False
        if other.type == EVENT_UNLOAD:
            return True
        if self.type_ == EVENT_CHANGE_TYPE_ST:
            return False
        if other.type == EVENT_CHANGE_TYPE_ST:
            return True
        if self.type_ == EVENT_ARRIVE:
            return False
        return True

    def __gt__(self, other) -> bool:
        if self.timestamp_ == other.timestamp_:
            return self.type_gt_(other)
        return self.timestamp_ > other.timestamp_

    def __eq__(self, other) -> bool:
        return self.timestamp_ == other.timestamp_

    def __lt__(self, other) -> bool:
        if self.timestamp_ == other.timestamp_:
            return not self.type_gt_(other)
        return self.timestamp_ < other.timestamp_

    def __le__(self, other) -> bool:
        return  self < other or self == other

    def __ge__(self, other) -> bool:
        return  self > other or self == other

    @property
    def qnumber(self) -> int:
        return self.qnumber_

    @property
    def type(self) -> int:
        return self.type_

    @property
    def timestamp(self) -> int:
        return self.timestamp_


class Events:
    events_ = []
    del_events_ = []

    def __repr__(self) -> str:
        str_evs = [str(ev) for ev in self.events_]
        return "\n".join(str_evs)

    def add(self, event: Event):

        if len(self.events_) == 0:
            self.events_ = [event]
            return

        for i, ev in enumerate(self.events_):
            if event < ev:
                self.events_.insert(i, event)
                return
        self.events_.append(event)

    def size(self) -> int:
        return len(self.events_)

    def get(self) -> Event:
        ev = self.events_[0]
        self.del_events_.append(ev)
        self.events_.remove(ev)
        return ev

    def arrive(self, timestamp, number):
        new_ev = Event(timestamp, EVENT_ARRIVE, number)
        self.add(new_ev)

    def change_type_st(self, timestamp, qnumber):
        new_ev = Event(timestamp, EVENT_CHANGE_TYPE_ST, qnumber)
        self.add(new_ev)

    def change_type_en(self, timestamp, qnumber):
        new_ev = Event(timestamp, EVENT_CHANGE_TYPE_EN, qnumber)
        self.add(new_ev)

    def load(self, timestamp, qnumber):
        new_ev = Event(timestamp, EVENT_LOAD, qnumber)
        self.add(new_ev)

    def unload(self, timestamp, qnumber):
        new_ev = Event(timestamp, EVENT_UNLOAD, qnumber)
        self.add(new_ev)

    def history(self) -> str:

        str_evs = []

        self.del_events_.sort()
        queues_num = max(self.del_events_, key = lambda ev: ev.qnumber).qnumber
        cur_queues = [0] * (queues_num + 1)
        for ev in self.del_events_:
            if ev.type == EVENT_ARRIVE:
                cur_queues[ev.qnumber] += 1
            elif ev.type == EVENT_LOAD:
                cur_queues[ev.qnumber] -= 1
            str_evs.append(str(ev) + "        " + str(cur_queues))
        return "\n".join(str_evs)
