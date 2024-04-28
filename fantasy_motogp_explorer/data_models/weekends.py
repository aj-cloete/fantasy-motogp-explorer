import inspect
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    id: int
    type: str
    status: str
    is_race2: int
    start: datetime
    end: datetime
    _start: datetime = field(init=False, repr=False)
    _end: datetime = field(init=False, repr=False)

    @classmethod
    def from_dict(cls, env):
        default_env = {k: None for k in inspect.signature(cls).parameters}
        default_env.update(env)
        return cls(**{k: v for k, v in default_env.items() if k in inspect.signature(cls).parameters})

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = datetime.fromisoformat(start)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = datetime.fromisoformat(end)


@dataclass
class Weekend:
    id: int
    name: str
    circuit: str
    displayed_name: str
    short_name: str
    position: int
    status: str
    start: datetime
    end: datetime
    races: list[Event]
    weather: dict = field(default_factory=dict)
    _start: datetime = field(init=False, repr=False)
    _end: datetime = field(init=False, repr=False)
    _races: list[Event] = field(init=False, repr=False)

    @classmethod
    def from_dict(cls, env):
        default_env = {k: None for k in inspect.signature(cls).parameters}
        default_env.update(env)
        return cls(**{k: v for k, v in default_env.items() if k in inspect.signature(cls).parameters})

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = datetime.fromisoformat(start)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = datetime.fromisoformat(end)

    @property
    def races(self):
        return self._races

    @races.setter
    def races(self, races):
        self._races = [Event(**race) for race in races]
