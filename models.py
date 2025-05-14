from run import db

class Tweet(db.Model):
    id = db.Column(db.String, primary_key=True)
    author_id = db.Column(db.String)
    hashtag = db.Column(db.String)
    text = db.Column(db.Text)
    created_time = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    retweets = db.Column(db.Integer)
    replies = db.Column(db.Integer)
    quotes = db.Column(db.Integer)
    sentiment = db.Column(db.String)
    media_urls = db.Column(db.Text, nullable=True)


def __repr__(self):
    return f"{self.text} ({self.sentiment})"
