from datetime import datetime

import pytest
from sqlmodel import Session, create_engine, select

from src.helpers import Partner
from src.models import Event, SQLModel

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")


@pytest.mark.order(4)
def test_create_tables():
    # if it runs and no errors pop up, congrats, the tables were made without error
    SQLModel.metadata.create_all(engine)


@pytest.mark.order(5)
def test_insert_data():
    fake_event = Event(
        site_name=Partner.afro_la,
        derived_tstamp=datetime.now(),
        doc_height=1,
        domain_sessionidx=1,
        domain_userid="fake-domain-id",
        dvce_screenheight=400,
        dvce_screenwidth=400,
        event_id="fake-event-id",
        event_name="page_ping",
        network_userid="fake-network-id",
        page_urlpath="/path/to/fake/article",
        page_referrer="https://www.fake.com",
        pp_yoffset_max=1,
        refr_medium="unknown",
        useragent="fake-user-agent",
    )
    session = Session(engine)
    session.add(fake_event)

    session.commit()

    statement = select(Event)
    results = session.exec(statement)
    db_event = results.first()
    assert fake_event == db_event
