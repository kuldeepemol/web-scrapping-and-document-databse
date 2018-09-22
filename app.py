from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Use pymongo to set up mongo connection
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

app = Flask(__name__)

@app.route("/")
def index():
    all_mars_details = collection.find_one()

    return render_template('index.html', details=all_mars_details)


@app.route("/scrape")
def scraper():

    collection.drop()
    mars_details = scrape_mars.scrape()
    collection.insert_one(mars_details)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)