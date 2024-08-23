from deluge_client import DelugeClient

client = DelugeClient('127.0.0.1', 8112, 'deluge')

def add_torrent(torrent_file):
    with open(torrent_file, 'rb') as f:
        torrent_data = f.read()
        client.add_torrent(torrent_data)
        print('Torrent added')

add_torrent('/path/to/torrent/file.torrent')
