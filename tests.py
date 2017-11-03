import unittest

from party import app
from model import db, example_data, connect_to_db
# from flask import Flask, session


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", 
                      result.data)

    def test_no_rsvp_yet(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the
        # party details

        result = self.client.get('/')
        self.assertNotIn("123 Magic Unicorn Way", result.data)
        self.assertIn('Please RSVP', result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)

        self.assertIn("123 Magic Unicorn Way", result.data)
        self.assertNotIn('Please RSVP', result.data)

#class where we are logged in by default
class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def rsvp(self):

        #add us to the session so as we go through tests, we're logged in
        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # #add us to the session so as we go through tests, we're logged in
        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess['RSVP'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        
        #calls the rsvp method - and could do this if you have only one class
        #with tests in it
        self.rsvp()
        result = self.client.get('/games')
        self.assertIn('Assasinate people', result.data)


if __name__ == "__main__":
    unittest.main()
