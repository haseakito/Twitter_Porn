from apps.app import db
from datetime import datetime

class URLs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False),
    url = db.Column(db.String(200), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name