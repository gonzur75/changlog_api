from sqlalchemy.orm import Session

import app.factories
from app import models
from app.db import engine


def init_data():
    with Session(engine) as session:
        app.factories.UserFactory.__session__ = session
        app.factories.ProductFactory.__session__ = session
        app.factories.UpdateFactory.__session__ = session
        app.factories.UpdatePointFactory.__session__ = session

        user = session.query(models.User).filter(models.User.username == "user").first()
        if not user:
            user = app.factories.UserFactory.create_sync(username="user")

        product = app.factories.ProductFactory.create_sync(name="Changelog", owner=user)

        updates = app.factories.UpdateFactory.create_batch_sync(
            size=100, product=product
        )

        for update in updates:
            app.factories.UpdatePointFactory.create_batch_sync(size=12, update=update)

        session.commit()


init_data()
