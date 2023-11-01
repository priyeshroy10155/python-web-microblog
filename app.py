from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            date_time=datetime.datetime.today().strftime("%d-%m-%y")
            
            app.db.entries.insert_one({"content": entry_content, "date": date_time})

        entry_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%d-%m-%y").strftime("%b %d")
                
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entry_with_date)
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
    
