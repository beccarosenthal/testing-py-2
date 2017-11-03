from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Game(db.Model):
    """Board game."""

    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100))


def connect_to_db(app, db_uri="postgresql:///games"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""
    
    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate games
    Game.query.delete()

    CAH_DESC = 'Assasinate people and pretend it\'s equally fun for all participants.'
    FIBBAGE_DESC = 'Lie to your friends and hope they remain your friends'

    cards_against_humans = Game(name='cards_against_humans',
                                description=CAH_DESC)
    fibbage = Game(name='fibbbage',
                   description=FIBBAGE_DESC)

    db.session.add_all([cards_against_humans, fibbage])
    db.session.commit()


if __name__ == '__main__':
    from party import app

    connect_to_db(app, 'postgresql:///games')
    print "Connected to DB."
 