import logging

from flask import Flask, render_template
import analysis

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    """Render the analytics dashboard homepage."""
    logger.info("Starting Flask request for /")
    logger.info("Using analysis module: %s", analysis.__file__)
    dashboard_data = analysis.build_dashboard_data()
    logger.info("Dashboard ready")
    return render_template("index.html", dashboard_data=dashboard_data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
