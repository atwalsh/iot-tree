import requests
import os

particle_base_url = 'https://api.particle.io/v1/devices'


def toggle_tree(request):
    key = request.headers.get('HEADER_KEY')
    if key is None or key != os.environ['HEADER_KEY']:
        return 'Unauthorized', 401
    status = request.json['status']
    toggle_status = None
    if status == 1:
        toggle_status = "1"
    elif status == 0:
        toggle_status = "0"
    else:
        return 'Bad Request', 400
    device_id = os.environ['PARTICLE_DEVICE_ID']
    func_name = os.environ['PARTICLE_DEVICE_FUNCTION']
    access_token = os.environ['PARTICLE_ACCESS_TOKEN']
    r = requests.post(
        url=f'{particle_base_url}/{device_id}/{func_name}',
        data={'access_token': access_token, 'args': toggle_status}
    )
    if r.status_code != 200:
        return 'ERROR', 500
    return 'OK', 200
