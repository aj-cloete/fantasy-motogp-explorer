from dataclasses import dataclass, field


@dataclass(kw_only=True)
class EventStats:
    event_num: int
    points: float
    highest_position: int
    fastest_lap: int
    race_time: str
    race_time_float: float


@dataclass(kw_only=True)
class Stats:
    podiums: int
    num_riders: int
    avg_grid_pos: float
    avg_finishing_pos: float
    total_fantasy_points: float
    fantasy_pos: float
    total_gp_points: float
    gp_pos: int
    total_points: float
    prices: list[int]
    events: list[EventStats]
    _prices: list[int] = field(init=False, repr=False)
    _events: list[EventStats] = field(init=False, repr=False)

    @property
    def prices(self):
        return self._prices

    @prices.setter
    def prices(self, prices: dict):
        ret = []
        i = 1
        while True:
            price = prices.get(str(i))
            if not price:
                break
            ret.append(price)
            i += 1
        self._prices = ret

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, events: dict):
        ret = []
        i = 1
        while True:
            event_stats = events.get(str(i))
            if not event_stats:
                break
            ret.append(EventStats(event_num=i, **event_stats))
            i += 1
        self._events = ret
