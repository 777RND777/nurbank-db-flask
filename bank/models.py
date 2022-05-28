from . import db


class Application(db.Model):
    __tablename__ = "applications"

    pk = db.Column(db.Integer, primary_key=True)
    id_ = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id_"), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.String(50), nullable=False)
    answer_date = db.Column(db.String(50), nullable=False, default='')
    approved = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="applications", lazy=True)

    # id check
    @classmethod
    def get(cls, application_id: int) -> 'Application':
        application = cls.query.filter(cls.id_ == application_id).first()
        return application


class User(db.Model):
    __tablename__ = "users"

    pk = db.Column(db.Integer, primary_key=True)
    id_ = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.BINARY(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False)
    nickname = db.Column(db.String(250), nullable=False)
    debt = db.Column(db.Integer, nullable=False, default=0)

    applications = db.relationship("Application", back_populates="user", lazy=True)

    # id check
    @classmethod
    def get(cls, user_id: int) -> 'User':
        user = cls.query.filter(cls.id_ == user_id).first()
        return user
