"""DCN Lab 2: a Flask web server that returns the current UTC time."""

from datetime import datetime, timezone

from flask import Flask, Response

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "Hello world! Visit /time for the current UTC time.\n"


@app.get("/time")
def current_time():
    now = datetime.now(timezone.utc).isoformat(timespec="microseconds")
    return Response(now + "\n", mimetype="text/plain", headers={"Cache-Control": "no-store"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
