from . import db


class Application(db.Model):
    __tablename__ = "applications"

    pk = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users._id"), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.String(50), nullable=False)
    answer_date = db.Column(db.String(50), nullable=False, default='')
    approved = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="applications", lazy=True)

    @property
    def json(self):
        return {
            "pk": self.pk,
            "_id": self._id,
            "user_id": self.user_id,
            "value": self.value,
            "request_date": self.request_date,
            "answer_date": self.answer_date,
            "approved": self.approved,
            "is_admin": self.is_admin
        }

    # id check
    @classmethod
    def get(cls, application_id: int):
        application = cls.query.filter(cls._id == application_id).first()
        return application


class User(db.Model):
    __tablename__ = "users"

    pk = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.BINARY(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False)
    nickname = db.Column(db.String(250), nullable=False)
    debt = db.Column(db.Integer, nullable=False, default=0)

    applications = db.relationship("Application", back_populates="user", lazy=True)

    @property
    def json(self):
        return {
            "pk": self.pk,
            "_id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "nickname": self.nickname,
            "debt": self.debt
        }

    # id check
    @classmethod
    def get(cls, user_id: int):
        user = cls.query.filter(cls._id == user_id).first()
        return user
