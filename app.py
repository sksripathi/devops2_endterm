import logging

from flask import Flask, render_template
import analysis

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)


def initialize_dashboard_data() -> None:
    """Load dashboard data once at startup so terminal logs show the dataset workflow."""
    print("[TERMINAL] Initializing dashboard data...", flush=True)
    analysis.build_dashboard_data()
    print("[TERMINAL] Dashboard data initialized", flush=True)


@app.route("/")
def index():
    """Render the analytics dashboard homepage."""
    logger.info("Starting Flask request for /")
    logger.info("Using analysis module: %s", analysis.__file__)
    print("[TERMINAL] Loading dashboard data...", flush=True)
    dashboard_data = analysis.build_dashboard_data()
    logger.info("Dashboard ready")
    print("[TERMINAL] Dashboard ready", flush=True)
    return render_template("index.html", dashboard_data=dashboard_data)


if __name__ == "__main__":
    initialize_dashboard_data()
    print("[TERMINAL] Starting Flask server on http://127.0.0.1:5000", flush=True)
    app.run(host="127.0.0.1", port=5000)
