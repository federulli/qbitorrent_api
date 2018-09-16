import requests

HOST = 'http://127.0.0.1:8080'


def get_torrents(status='all'):
    """
    :param status: all, downloading, completed,
        paused, active, inactive
    :return:
    """
    r = requests.get(
        '{}/api/v2/torrents/info?filter={}'.format(HOST, status)
    )
    r.raise_for_status()
    return r.json()


def post_torrent(magnet, download_path):
    r = requests.post(
            '{}/command/download'.format(HOST),
            data=dict(
                urls=magnet,
                savepath=download_path
            )
    )
    r.raise_for_status()
