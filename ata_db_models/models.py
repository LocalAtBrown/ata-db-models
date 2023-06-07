from datetime import datetime
from enum import Enum
from typing import Optional, Union
from uuid import UUID

from pydantic import HttpUrl
from sqlmodel import JSON, Column, Field, SQLModel, String


class StrEnum(str, Enum):
    """
    StrEnum class. Replace with built-in version after upgrading to Python 3.10.
    """

    def __str__(self) -> str:
        return f"{self.value}"


class RefrMedium(StrEnum):
    email = "email"
    internal = "internal"
    paid = "paid"
    search = "search"
    social = "social"
    unknown = "unknown"


class Group(StrEnum):
    A = "A"
    B = "B"
    C = "C"


class SiteName(StrEnum):
    AFRO_LA = "afro-la"
    DALLAS_FREE_PRESS = "dallas-free-press"
    OPEN_VALLEJO = "open-vallejo"
    THE_19TH = "the-19th"


class Event(SQLModel, table=True):
    # Site name
    site_name: SiteName = Field(primary_key=True)

    # Browser viewport height
    br_viewheight: Optional[float]

    # Browser viewport width
    br_viewwidth: Optional[float]

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

    # URL of the page
    # TODO: Backfill this field for events before June 7, 2023
    page_url: HttpUrl = Field(sa_column=Column(String))

    # Fragment of page URL, e.g., #section1 in https://dallasfreepress.com/event-directory/#section1
    # TODO: Backfill this field for events before June 1, 2023
    page_urlfragment: Optional[str]

    # Host of page, e.g., dallasfreepress.com in https://dallasfreepress.com/event-directory/
    # TODO: Backfill this field for events before June 7, 2023, then remove the Optional in the type hint
    page_urlhost: Optional[str]

    # Path to page, e.g., /event-directory/ in https://dallasfreepress.com/event-directory/
    page_urlpath: str

    # Querystring of page, e.g., ?utm_source=google&utm_medium=cpc&utm_campaign=brand
    # TODO: Backfill this field for events before June 1, 2023
    page_urlquery: Optional[str]

    # URL of the referrer
    page_referrer: HttpUrl = Field(sa_column=Column(String))

    # Maximum page y-offset seen in the last ping period. Depends on event_name == "page_ping"
    pp_yoffset_max: Optional[float] = None

    # Type of referer. Can be "social", "search", "internal", "unknown", "email"
    # (read: https://docs.snowplow.io/docs/enriching-your-data/available-enrichments/referrer-parser-enrichment/)
    refr_medium: Optional[RefrMedium] = None

    # Name of referer if recognised, e.g., "Google" or "Bing"
    refr_source: Optional[str] = None

    # URL host of referrer
    refr_urlhost: Optional[str]

    # URL fragment of referrer
    # TODO: Backfill this field for events before June 1, 2023
    refr_urlfragment: Optional[str]

    # URL path of referrer
    refr_urlpath: Optional[str]

    # URL querystring of referrer
    # TODO: Backfill this field for events before June 1, 2023
    refr_urlquery: Optional[str]

    # Data/attributes of HTML form and all its inputs in JSON format. Only present if event_name == "submit_form"
    # (read: https://github.com/snowplow/iglu-central/blob/master/schemas/com.snowplowanalytics.snowplow/submit_form/jsonschema/1-0-0)
    unstruct_event_com_snowplowanalytics_snowplow_submit_form_1: Optional[Union[list, dict]] = Field(sa_column=Column(JSON))  # type: ignore

    # Raw useragent
    useragent: str


class Prescription(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True)
    site_name: str = Field(primary_key=True)
    prescribe: bool
    last_updated: datetime
    # TODO will add this once we have models to work with!
    # model_id: UUID = Field(foreign_key="model.id")


class UserGroup(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True)
    site_name: str = Field(primary_key=True)
    group: Group
    last_updated: datetime = Field(default_factory=datetime.utcnow)
