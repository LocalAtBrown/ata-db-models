from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import HttpUrl
from sqlmodel import Column, Field, SQLModel, String


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
    # User ID set by Snowplow using 3rd party cookie
    network_userid: UUID
    # [STR, CATEGORICAL if needed] Path to page, e.g., /event-directory/ in https://dallasfreepress.com/event-directory/
    # TODO make regex validation
    page_urlpath: str
    # URL of the referrer
    page_referrer: HttpUrl = Field(sa_column=Column(String))
    # Maximum page y-offset seen in the last ping period. Depends on event_name == "page_ping"
    # TODO might be optional/nullable
    pp_yoffset_max: Optional[float] = None
    # Type of referer. Can be "social", "search", "internal", "unknown", "email"
    # (read: https://docs.snowplow.io/docs/enriching-your-data/available-enrichments/referrer-parser-enrichment/)
    # TODO consider making this an enum
    refr_medium: str
    # Name of referer if recognised, e.g., "Google" or "Bing"
    refr_source: Optional[str] = None
    # Data/attributes of HTML input and its form in JSON format. Only present if event_name == "change_form"
    # (read: https://github.com/snowplow/iglu-central/blob/master/schemas/com.snowplowanalytics.snowplow/change_form/jsonschema/1-0-0)
    # TODO probably optional and json
    unstruct_event_com_snowplowanalytics_snowplow_change_form_1: Optional[str] = None
    # Data/attributes of HTML input and its form in JSON format. Only present if event_name == "focus_form"
    # (read: https://github.com/snowplow/iglu-central/blob/master/schemas/com.snowplowanalytics.snowplow/focus_form/jsonschema/1-0-0)
    # TODO probably optional and json
    unstruct_event_com_snowplowanalytics_snowplow_focus_form_1: Optional[str] = None
    # Data/attributes of HTML form and all its inputs in JSON format. Only present if event_name == "submit_form"
    # (read: https://github.com/snowplow/iglu-central/blob/master/schemas/com.snowplowanalytics.snowplow/submit_form/jsonschema/1-0-0)
    # TODO probably optional and json
    unstruct_event_com_snowplowanalytics_snowplow_submit_form_1: Optional[str] = None
    # Raw useragent
    useragent: str
