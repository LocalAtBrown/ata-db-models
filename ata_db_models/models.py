from datetime import datetime
from enum import Enum
from typing import Optional, Union
from uuid import UUID

from pydantic import HttpUrl
from sqlmodel import JSON, Column, Field, SQLModel, String


class RefrMedium(str, Enum):
    email = "email"
    internal = "internal"
    paid = "paid"
    search = "search"
    social = "social"
    unknown = "unknown"


class Event(SQLModel, table=True):
    # TODO make enum
    site_name: str = Field(primary_key=True)
    # Timestamp making allowance for inaccurate device clock
    derived_tstamp: datetime
    # The page's height in pixels
    doc_height: float
    # Number of the current user session, e.g. first session is 1, next session is 2, etc. Dependent on domain_userid
    domain_sessionidx: int
    # User ID set by Snowplow using 1st party cookie
    domain_userid: UUID
    # Screen height in pixels. Almost 1-to-1 relationship with domain_userid (there are exceptions)
    dvce_screenheight: float
    # Screen width in pixels. Almost 1-to-1 relationship with domain_userid (there are exceptions)
    dvce_screenwidth: float
    # ID of event. This would be the primary key within the site DataFrame,
    # and part of the [site_name, event_id] composite key in the database table
    event_id: UUID = Field(primary_key=True)
    # Name of event. Can be "page_view", "page_ping", "focus_form", "change_form", "submit_form"
    # TODO make enum
    event_name: str
    # [STR, CATEGORICAL if needed] Path to page, e.g., /event-directory/ in https://dallasfreepress.com/event-directory/
    page_urlpath: str
    # URL of the referrer
    page_referrer: HttpUrl = Field(sa_column=Column(String))
    # Maximum page y-offset seen in the last ping period. Depends on event_name == "page_ping"
    pp_yoffset_max: Optional[float] = None
    # Type of referer. Can be "social", "search", "internal", "unknown", "email"
    # (read: https://docs.snowplow.io/docs/enriching-your-data/available-enrichments/referrer-parser-enrichment/)
    refr_medium: Optional[RefrMedium] = None
    # Name of referer if recognised, e.g., "Google" or "Bing"
    refr_source: Optional[str] = None
    # Data/attributes of HTML form and all its inputs in JSON format. Only present if event_name == "submit_form"
    # (read: https://github.com/snowplow/iglu-central/blob/master/schemas/com.snowplowanalytics.snowplow/submit_form/jsonschema/1-0-0)
    unstruct_event_com_snowplowanalytics_snowplow_submit_form_1: Optional[Union[list, dict]] = Field(sa_column=Column(JSON))  # type: ignore
    # Raw useragent
    useragent: str
    br_viewheight: Optional[float]
    br_viewwidth: Optional[float]
    refr_urlhost: Optional[str]
    refr_urlpath: Optional[str]


class Prescription(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True)
    site_name: str = Field(primary_key=True)
    prescribe: bool
    last_updated: datetime
    # TODO will add this once we have models to work with!
    # model_id: UUID = Field(foreign_key="model.id")
