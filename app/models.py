from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.username)


class ConferenceModel(db.Model):
    __tablename__ = 'conference'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)
    teams = db.relationship('TeamModel', backref='conference', lazy='dynamic')

    def __repr__(self):
        return '<Conference %r>' % (self.name)


class TeamModel(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    players = db.relationship('PlayerModel', backref='team', lazy='dynamic')

    def __repr__(self):
        return '<Team %r>' % (self.name)

class PlayerModel(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(4), index=True)
    name = db.Column(db.String(75), index=True)
    number = db.Column(db.String(3))
    position = db.Column(db.String(4))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    academic_class = db.Column(db.String(2))
    hometown = db.Column(db.String(40))
    status = db.Column(db.SmallInteger)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<player %r>' % (self.name)