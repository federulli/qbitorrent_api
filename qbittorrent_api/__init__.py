import os
import requests

HOST = f'http://{os.environ["QBITTORRENT_HOST"]}:8080'
USERNAME = os.environ.get("QBITTORRENT_USERNAME")
PASSWORD = os.environ.get("QBITTORRENT_PASSWORD")

s = requests.Session()


def login():
    if USERNAME and PASSWORD:
        r = s.post(
            f'{HOST}/login',
            data=dict(
                username=USERNAME,
                password=PASSWORD
            )
        )
        r.raise_for_status()


def get_torrents():
    login()
    r = s.get(
        '{}/query/torrents'.format(HOST)
    )
    r.raise_for_status()
    return r.json()


def post_torrent(magnet, download_path):
    login()
    r = s.post(
        '{}/command/download'.format(HOST),
        data=dict(
            urls=magnet,
            savepath=download_path
        )
    )
    r.raise_for_status()


def delete_completed_torrent():
    login()
    torrents = get_torrents()
    hashes = "|".join(
        torrent["hash"]
        for torrent in torrents if torrent['state'] in ["uploading", "stalledUP", "queuedUP"]
    )
    r = s.post("{}/command/delete".format(HOST), data=dict(hashes=hashes))
    r.raise_for_status()
