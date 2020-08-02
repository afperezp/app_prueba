from .. import db
import datetime

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    points = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.String, db.ForeignKey('user.public_id'), nullable=False)
    # likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}','{self.created}')"