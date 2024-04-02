from dataclasses import dataclass, field


@dataclass
class RiderEventStats:
    grid_position: int
    q1_position: int
    q2_position: int
    sprint_position: int
    final_position: int
    q1_points: float
    q2_points: float
    sprint_points: float
    final_points: float
    qualifying_vs_final_position: int
    qualifying_vs_final_position_points: float
    event_num: int
    points: float
    fastest_lap: int
    race_time: str
    race_time_float: float


@dataclass
class RiderStats:
    wpr_history: dict
    avg_points: float
    podium: int
    last_event: float
    last_3_events: float
    last_5_events: float
    season_points: float
    starts: int
    avg_qualifying_pos: float
    is_prev_season: int
    cost_dynamic: int
    total_points: float
    avg_grid_pos: float
    avg_finishing_pos: float
    prices: list[int]
    events: list[RiderEventStats]
    _prices: list[int] = field(init=False, repr=False)
    _events: list[RiderEventStats] = field(init=False, repr=False)

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
            ret.append(RiderEventStats(event_num=i, **event_stats))
            i += 1
        self._events = ret


@dataclass
class _Rider:
    first_name: str
    last_name: str
    cost: int
    country: str
    number: int
    status: str
    id: int
    constructor_id: int
    squad_id: int
    stats: RiderStats
    _stats: RiderStats = field(init=False, repr=False)
    team_id: int = field(init=False)
    short_name: str = field(init=False)

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, stats: dict):
        self._stats = RiderStats(**stats)


class Rider(_Rider):
    @property
    def team_id(self):
        return self.squad_id

    @property
    def short_name(self):
        return f"{self.first_name[0]} {self.last_name[:3]}".upper()
