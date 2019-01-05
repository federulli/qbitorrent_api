import requests

HOST = 'http://127.0.0.1:8080'


def get_torrents():
    """
    :param status: all, downloading, completed,
        paused, active, inactive
    :return:
    """
    r = requests.get(
        '{}/query/torrents'.format(HOST)
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


def delete_completed_torrent():
    torrents = get_torrents()
    hashes = "|".join(
        torrent["hash"]
        for torrent in torrents if torrent['state'] in ["uploading", "stalledUP", "queuedUP"]
    )
    r = requests.post("{}/command/delete".format(HOST), data=dict(hashes=hashes))
    r.raise_for_status()
