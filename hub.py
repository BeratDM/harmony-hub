from flask import Flask, request, abort
import hmac
import hashlib
import subprocess
import os

app = Flask(__name__)

NIKO_GITHUB_WEBHOOK_SECRET = os.getenv("NIKO_GITHUB_WEBHOOK_SECRET", "")
NIKO_MANUAL_SECRET = os.getenv("NIKO_MANUAL_SECRET", "")


@app.route("/")
def index():
    return "harmony"


@app.route("/niko-deploy", methods=["POST"])
def niko_deploy():
    # Check if this is GitHub webhook
    sig = request.headers.get("X-Hub-Signature-256")
    if sig:
        body = request.data
        expected_sig = (
            "sha256="
            + hmac.new(
                NIKO_GITHUB_WEBHOOK_SECRET.encode(), body, hashlib.sha256
            ).hexdigest()
        )
        if not hmac.compare_digest(sig, expected_sig):
            abort(403, description="Invalid signature or token")
    else:
        # Manual trigger check
        token = request.headers.get("X-Manual-Token")
        if token != MANUAL_SECRET:
            abort(403, description="Invalid signature or token")

    print("deploying niko-discord-bot")
    # Run deployment script
    subprocess.Popen(["/home/bx/bxProjects/niko-discord-bot/util/deploy.sh"])
    return "Deployment started\n", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
