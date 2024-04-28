import json
import logging
import os
from datetime import datetime
from functools import cached_property

import pandas as pd
import requests
from data_models.constructors import Constructor
from data_models.riders import Rider
from data_models.teams import Team
from data_models.weekends import Weekend
from urls import constructors_url as _constructors
from urls import events_url as _events
from urls import riders_url as _riders
from urls import squads_url as _squads

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
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
        except FileNotFoundError:
            self._log.info(f"Getting {self._name+' '}stats from website")
            data = requests.get(self._url).json()
            with open(filename, "w") as f:
                f.write(json.dumps(data))
        return data

    @cached_property
    def raw_info(self):
        return [self._base_class.from_dict(datum) for datum in self.website_json]

    @cached_property
    def _info(self):
        df = pd.DataFrame(self.raw_info).set_index("id")
        for col in df:
            if str(df[col].dtype) != "object":
                continue
            try:
                df[col] = pd.to_datetime(df[col], utc=True, format="%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
        return df


class BaseStats(Base):

    @property
    def info(self):
        ret = self._info.drop(columns=["stats", "_stats", "_cost_millions"]).rename(
            errors="ignore",
            columns={
                "first_name": "Name",
                "name": "Name",
                "last_name": "Surname",
                "country": "From",
                "number": "#",
                "status": "Status",
                "cost": "Cost $M",
                "rider": "Rider",
                "num_riders": "Riders",
            },
        )
        return ret

    @property
    def _stats(self):
        df = pd.json_normalize(self._info.stats)
        df.index = self._info.index
        return df

    @property
    def stats(self):
        identifier = "Rider" if "Rider" in self.info.columns else "Name"
        ret = (
            self.info[[identifier, "Cost $M"]]
            .join(self._stats)
            .drop(columns=["prices", "_prices", "events", "_events"], errors="ignore")
        )
        ret.columns = [col.replace("_", " ").title().replace("Gp", "GP") for col in ret.columns]
        return (
            ret.drop(columns=["Total Fantasy Points"], errors="ignore")
            .rename(errors="ignore", columns={"Total Points": "Total Fantasy Points"})
            .sort_values("Total Fantasy Points", ascending=False)
        )

    @property
    def history(self):
        df = pd.json_normalize(self._stats.events)
        df.index = self._info.index
        dfs = []
        for event_id in df:
            df_event = pd.json_normalize(df[event_id])
            df_event.index = self._info.index
            dfs.append(df_event)
        df_events = pd.concat(dfs).sort_values("event_num")
        identifier = "Rider" if "Rider" in self.info.columns else "Name"
        df_events.insert(0, identifier, self.info[identifier])
        df_events.columns = [x.replace("_", " ").title() for x in df_events.columns]
        return df_events

    @property
    def complete_info(self):
        complete = self.info.join(self.stats.drop(columns=["Rider", "Name", "Num riders"], errors="ignore"))
        return complete

    @property
    def all_data(self):
        all_data = (
            self.info.merge(self.stats, how="left", left_index=True, right_index=True).merge(
                self.history, how="left", left_index=True, right_index=True
            )
        ).sort_values("Event Num")
        return all_data


class RiderStats(BaseStats):
    def __init__(self, url: str = _riders, name: str = "rider", base_class: type = Rider):
        super().__init__(url=url, name=name, base_class=base_class)

    @property
    def basic_info(self):
        basic_data = (
            super().info.sort_values("Cost $M", ascending=False).drop(columns=["squad_id", "constructor_id", "team_id"])
        )
        basic_data.columns = [x.replace("_", " ").title() for x in basic_data.columns]
        return basic_data[["Rider"] + [col for col in basic_data.columns if col != "Rider"]]


class ConstructorStats(BaseStats):
    def __init__(self, url: str = _constructors, name: str = "constructor", base_class: type = Constructor):
        super().__init__(url=url, name=name, base_class=base_class)


class TeamStats(BaseStats):
    def __init__(self, url: str = _squads, name: str = "team", base_class: type = Team):
        super().__init__(url=url, name=name, base_class=base_class)

    @property
    def info(self):
        return super().info.drop(columns="_is_wildcard")

    @property
    def basic_info(self):
        basic_data = self.info.sort_values("Cost $M", ascending=False).rename(
            columns={"num_riders": "Riders", "cost": "Cost ($M)", "is_wildcard": "wildcard"}
        )
        basic_data.columns = [x.replace("_", " ").title() for x in basic_data.columns]
        return basic_data


class Weekends(Base):
    def __init__(self, url: str = _events, name: str = "weekend", base_class: type = Weekend):
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
            event["weekend_event"] = event_order + 1
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

    @cached_property
    def rider_full_data(self):
        constructor = self.constructors.info.rename(columns={"name": "constructor"})
        team = self.teams.info.rename(columns={"name": "team"})
        full_data = self.riders.all_data.merge(
            constructor.constructor, left_on="constructor_id", right_index=True
        ).merge(team.team, left_on="team_id", right_index=True)
        ret = full_data.drop(columns=["constructor_id", "squad_id", "team_id"])
        return ret
