from flask import Flask, render_template, request
from pull_apod import fetch_apod
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    '''Render Home Page '''
    data = fetch_apod()
    return render_template("home.html", apod=data)

@app.route("/history", methods=["GET"])
def history():
    ''' History Page get API data and push to HTML page '''
    date = request.args.get("date")
    data = None
    if date:
        try:
            data = fetch_apod(date)
        except Exception as e:
            data = {"error": str(e)}
    today = datetime.today().strftime('%Y-%m-%d')  # today's date
    return render_template("history.html", apod=data, today=today) # Return picture, and information

if __name__ == "__main__":
    app.run(debug=True)
