from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask_migrate import Migrate
from collections import Counter
from extensions import db
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Import models
    from models import Tweet

    # Routes
    @app.route('/')
    def index():
        search_query = request.args.get('search', '').strip()

        # Query tweets
        if search_query:
            tweets = Tweet.query.filter(
                (Tweet.hashtag.ilike(f'%{search_query}%')) |
                (Tweet.author_id.ilike(f'%{search_query}%'))
            ).order_by(Tweet.created_time.desc()).all()
        else:
            tweets = Tweet.query.order_by(Tweet.created_time.desc()).all()

        # Sentiment counts for bar chart
        positive = sum(1 for tweet in tweets if tweet.sentiment == 'Positive')
        neutral = sum(1 for tweet in tweets if tweet.sentiment == 'Neutral')
        negative = sum(1 for tweet in tweets if tweet.sentiment == 'Negative')

        sentiment_data = {
            'positive': positive,
            'neutral': neutral,
            'negative': negative
        }

        # Hashtag frequency data for horizontal bar chart
        hashtags = [tweet.hashtag for tweet in tweets if tweet.hashtag]
        hashtag_counter = Counter(hashtags)
        sorted_hashtags = sorted(hashtag_counter.items(), key=lambda x: x[1], reverse=True)
        hashtag_labels = [item[0] for item in sorted_hashtags]
        hashtag_counts = [item[1] for item in sorted_hashtags]

        # Serialize tweets for JavaScript use
        serialized_tweets = [{
            'id': tweet.id,
            'author_id': tweet.author_id,
            'hashtag': tweet.hashtag,
            'text': tweet.text,
            'created_time': tweet.created_time.strftime('%Y-%m-%d %H:%M'),
            'likes': tweet.likes,
            'retweets': tweet.retweets,
            'replies': tweet.replies,
            'quotes': tweet.quotes,
            'sentiment': tweet.sentiment,
            'media_urls': tweet.media_urls
        } for tweet in tweets]

        return render_template(
            'index.html',
            tweets=tweets,
            sentiment_data=sentiment_data,
            hashtag_labels=hashtag_labels,
            hashtag_counts=hashtag_counts,
            serialized_tweets=serialized_tweets,
            time_labels=[],  # Added to prevent JSON error
            time_counts=[]   # Added to prevent JSON error
        )

    return app

# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
