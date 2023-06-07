from datetime import datetime
from uuid import uuid4

import pytest
from sqlmodel import Session, create_engine, select

from ata_db_models.models import Event, Prescription, SiteName, SQLModel

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")


@pytest.mark.order(4)
def test_create_tables():
    # if it runs and no errors pop up, congrats, the tables were made without error
    SQLModel.metadata.create_all(engine)


@pytest.mark.order(5)
def test_insert_event_data() -> None:
    fake_event = Event(
        site_name=SiteName.AFRO_LA,
        derived_tstamp=datetime.now(),
        doc_height=1,
        domain_sessionidx=1,
        domain_userid=uuid4(),
        dvce_screenheight=400,
        dvce_screenwidth=400,
        event_id=uuid4(),
        event_name="page_ping",
        network_userid=uuid4(),
        page_url="https://www.fake.com/path/to/fake/article",
        page_urlhost="www.fake.com",
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


@pytest.mark.order(6)
def test_insert_prescription_data() -> None:
    fake_prescription = Prescription(
        user_id=uuid4(), site_name=SiteName.AFRO_LA, prescribe=True, last_updated=datetime.now()
    )

    session = Session(engine)
    session.add(fake_prescription)

    session.commit()

    statement = select(Prescription)
    results = session.exec(statement)
    db_prescription = results.first()
    assert fake_prescription == db_prescription
