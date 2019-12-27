import requests
import os
from flask import jsonify

particle_base_url = "https://api.particle.io/v1/devices"

# Particle API request variables
device_id = os.environ["PARTICLE_DEVICE_ID"]
func_name = os.environ["PARTICLE_DEVICE_FUNCTION"]
variable_name = os.environ["PARTICLE_VARIABLE_NAME"]
access_token = os.environ["PARTICLE_ACCESS_TOKEN"]


def toggle_tree(request):
    """
    Interact with the Particle board connected to the relay switch. 
    This method is called by the GCP Cloud Function.
    """
    # Check the header for key
    key = request.headers.get("HEADER_KEY")
    if key is None or key != os.environ["HEADER_KEY"]:
        return "Unauthorized", 401

    # Handle the request
    if request.method == "GET":
        return _handle_get(request)
    elif request.method == "POST":
        return _handle_post(request)
    else:
        return "Bad Request", 400


def _handle_get(request):
    """Return the current status of the tree."""
    r = requests.get(
        url=f"{particle_base_url}/{device_id}/{variable_name}",
        params={"access_token": access_token},
    )
    if r.status_code != 200:
        return "ERROR", 500
    return jsonify({"status": r.json()["result"]})


def _handle_post(request):
    """Change the status of the tree."""
    # Get the on/off value from request body
    status = request.json.get("status") if request.json else None
    if status not in (0, 1):
        return "Bad Request", 400

    # Make request to Particle API
    r = requests.post(
        url=f"{particle_base_url}/{device_id}/{func_name}",
        data={"access_token": access_token, "args": str(status)},
    )

    # Return some message and HTTP status code
    if r.status_code != 200:
        return "ERROR", 500
    return "OK", 200
