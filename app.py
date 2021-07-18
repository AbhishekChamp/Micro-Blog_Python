import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient("MONGODB_URI", 27017)
    app.db = client.microblog

    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_title = request.form.get("title")
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert({"title": entry_title, "content": entry_content, "date": formatted_date})
          
        entries_with_date = [
            (
                entry["title"],
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template('home.html', entries = entries_with_date)
    
    return app
