import json
import logging
from functools import cached_property
import os

import pandas as pd
import requests
from pandas._libs.tslibs.parsing import DateParseError

from data_models.constructors import Constructor
from data_models.riders import Rider
from data_models.teams import Team
from data_models.weekends import Weekend
from urls import (
    riders_url as _riders,
    squads_url as _squads,
    constructors_url as _constructors,
    events_url as _events
)
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class Base:
    def __init__(
            self,
            url: str,
            name: str,
            base_class: type,
    ):
        self._url = url
        self._name = name
        self._base_class = base_class

    @cached_property
    def _log(self):
        return logging.getLogger(":".join([__name__, self._name]))

    @cached_property
    def website_json(self):
        datestr = datetime.strftime(datetime.now(), "%Y%m%d")
        directory = os.path.join(os.path.dirname(__file__), "data", self._name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, f"{datestr}.json")
        try:
            with open(filename, "r") as f:
                data = json.loads(f.read())
            self._log.info(f"Using {self._name+' '}data from disk: {filename}")
        except FileNotFoundError as e:
            self._log.info(f"Getting {self._name+' '}stats from website")
            data = requests.get(self._url).json()
            with open(filename, "w") as f:
                f.write(json.dumps(data))
        return data

    @cached_property
    def raw_info(self):
        return [self._base_class(**datum) for datum in self.website_json]

    @cached_property
    def _info(self):
        df = pd.DataFrame(self.raw_info).set_index("id")
        for col in df:
            if str(df[col].dtype) != "object":
                continue
            try:
                df[col] = pd.to_datetime(df[col], utc=True)
            except (DateParseError, TypeError):
                pass
        return df


class BaseStats(Base):

    @property
    def info(self):
        return self._info.drop(columns=["stats", "_stats"])

    @property
    def _stats(self):
        df = pd.json_normalize(self._info.stats)
        df.index = self._info.index
        return df

    @property
    def stats(self):
        return self._stats.drop(columns=["prices", "_prices", "events", "_events"])

    @property
    def history(self):
        df = pd.json_normalize(self._stats.events)
        df.index = self._info.index
        dfs = []
        for event_id in df:
            df_event = pd.json_normalize(df[event_id])
            df_event["event_id"] = event_id+1
            df_event.index = self._info.index
            dfs.append(df_event)
        df_events = pd.concat(dfs)
        return df_events.sort_index()

    @property
    def complete_info(self):
        return self.info.join(self.stats)

    @property
    def all_data(self):
        return self.info.merge(
            self.stats,
            how="left",
            left_index=True,
            right_index=True
        ).merge(
            self.history,
            how="left",
            left_index=True,
            right_index=True)


class RiderStats(BaseStats):
    def __init__(
            self,
            url: str = _riders,
            name: str = "rider",
            base_class: type = Rider
    ):
        super().__init__(url=url, name=name, base_class=base_class)

    @property
    def basic_info(self):
        return super().info.drop(columns=["squad_id", "constructor_id", "team_id"])


class ConstructorStats(BaseStats):
    def __init__(
            self,
            url: str = _constructors,
            name: str = "constructor",
            base_class: type = Constructor
    ):
        super().__init__(url=url, name=name, base_class=base_class)


class TeamStats(BaseStats):
    def __init__(
            self,
            url: str = _squads,
            name: str = "team",
            base_class: type = Team
    ):
        super().__init__(url=url, name=name, base_class=base_class)

    @property
    def info(self):
        return super().info.drop(columns="_is_wildcard")

    @property
    def basic_info(self):
        return self.info.drop(columns="is_wildcard")


class Weekends(Base):
    def __init__(
            self,
            url: str = _events,
            name: str = "weekend",
            base_class: type = Weekend
    ):
        super().__init__(url=url, name=name, base_class=base_class)

    @property
    def info(self):
        df = self._info.drop(columns=["_start", "_end", "_races", "races", "weather"])
        df = df.rename(columns={"position": "number"})
        weather = pd.json_normalize(self._info.weather)
        weather.index = df.index
        return pd.concat([df, weather], axis=1)

    @property
    def events(self):
        events = pd.json_normalize(self._info.races)
        events.index = self._info.index
        dfs = []
        for event_order in events:
            event = pd.json_normalize(events[event_order])
            event["weekend_event"] = event_order+1
            event.index = events.index
            dfs.append(event)
        ret = pd.concat(dfs).drop(columns=["_start", "_end"])
        return ret.rename(columns={"id": "event_id"}).sort_values("event_id")

    @property
    def all_data(self):
        return self.info.join(self.events, rsuffix="_of_event")


# @st.cache_resource
class FantasyStats:
    @cached_property
    def riders(self):
        return RiderStats()

    @cached_property
    def constructors(self):
        return ConstructorStats()

    @cached_property
    def teams(self):
        return TeamStats()

    @cached_property
    def weekends(self):
        return Weekends()
