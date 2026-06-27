from flask import Flask, render_template
from analysis import build_dashboard_data

app = Flask(__name__)


@app.route("/")
def index():
    """Render the analytics dashboard homepage."""
    dashboard_data = build_dashboard_data()
    return render_template("index.html", dashboard_data=dashboard_data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
