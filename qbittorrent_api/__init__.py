import os
import requests

s = requests.Session()


def get_host():
    return f'http://{os.environ["QBITTORRENT_HOST"]}:8080'


def login():
    username = os.environ.get("QBITTORRENT_USERNAME")
    password = os.environ.get("QBITTORRENT_PASSWORD")
    if username and password:
        r = s.post(
            f'{get_host()}/login',
            data=dict(
                username=username,
                password=password
            )
        )
        r.raise_for_status()


def get_torrents():
    login()
    r = s.get(
        f'{get_host()}/query/torrents'
    )
    r.raise_for_status()
    return r.json()


def post_torrent(magnet, download_path):
    login()
    r = s.post(
        f'{get_host()}/command/download',
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
        for torrent in torrents if torrent['state'] in ["uploading", "stalledUP", "queuedUP", 'forcedUP']
    )
    r = s.post(f"{get_host()}/command/delete", data=dict(hashes=hashes))
    r.raise_for_status()


def delete_all_torrents():
    login()
    torrents = get_torrents()
    hashes = "|".join(
        torrent["hash"]
        for torrent in torrents
    )
    r = s.post(f"{get_host()}/command/delete", data=dict(hashes=hashes))
    r.raise_for_status()
