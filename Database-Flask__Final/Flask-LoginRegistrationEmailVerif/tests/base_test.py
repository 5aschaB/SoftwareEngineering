import os
import datetime

from flask_testing import TestCase

from src import app, db
from src.accounts.models import UserAccountTable


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        unconfirmed_user = UserAccountTable(email="unconfirmeduser@gmail.com", password="unconfirmeduser", tokenGenerationTime=datetime.datetime.now(),
                                            emailVerificationStatus=False, emailVerifiedTime=None, roleType="mgr", is_admin=False)
        db.session.add(unconfirmed_user)
        confirmed_user = UserAccountTable(email="confirmeduser@gmail.com", password="confirmeduser", tokenGenerationTime=datetime.datetime.now(),
                                            emailVerificationStatus=True, emailVerifiedTime=datetime.datetime.now(), roleType="mgr", is_admin=False)
        db.session.add(confirmed_user)
        
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        testdb_path = os.path.join("src", "testdb.sqlite")
        os.remove(testdb_path)
