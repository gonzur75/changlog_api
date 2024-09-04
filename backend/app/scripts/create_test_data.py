from sqlalchemy.orm import Session

import app.factories
from app import models
from app.db import engine


def init_data():
    with Session(engine) as session:
        app.factories.UserPolyFactory.__session__ = session
        app.factories.ProductPolyFactory.__session__ = session
        app.factories.UpdatePolyFactory.__session__ = session
        app.factories.UpdatePointPolyFactory.__session__ = session

        user = session.query(models.User).filter(models.User.username == "user").first()
        if not user:
            user = app.factories.UserPolyFactory.create_sync(username="user")

        product = app.factories.ProductPolyFactory.create_sync(
            name="Changelog", owner=user
        )

        updates = app.factories.UpdatePolyFactory.create_batch_sync(
            size=100, product=product
        )

        for update in updates:
            app.factories.UpdatePointPolyFactory.create_batch_sync(
                size=12, update=update
            )

        session.commit()


init_data()
