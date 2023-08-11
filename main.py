"""
This program will take your
"""
import json
from dataclasses import dataclass
from typing import List

from ytmusicapi import YTMusic
from openpyxl import Workbook


@dataclass
class Song:
    title: str
    artists: List


def main():
    """ Main method where the magic happens. """
    try:
        print("Authorizing...")
        ytmusic = YTMusic("oauth.json")
    except json.decoder.JSONDecodeError:
        print("Error reading oauth.json file. Run 'ytmusicapi oauth' from the command line to generate.")
        return

    print("Getting liked songs...")
    song_query_result = ytmusic.get_liked_songs(2000)

    song_list = []
    for track in song_query_result['tracks']:
        artist_list = []
        for artists in track['artists']:
            artist_list.append(artists['name'])
        song = Song(title=track['title'], artists=artist_list)
        song_list.append(song)

    sorted_song_list = sorted(song_list, key=lambda x: x.artists[0].lower() + x.title)
    # print(songs)
    # print(json.dumps(songs, indent=4))
    print("Writing out spreadsheet...")

    workbook = Workbook()
    work_sheet = workbook.active
    work_sheet.append(['Title', 'Artist 1', 'Artist 2', 'Artist 3'])

    for song in sorted_song_list:
        row = [song.title]
        for artist in song.artists:
            row.append(artist)

        work_sheet.append(row)

    workbook.save("liked_songs.xlsx")
    print("Finished. Results in liked_songs.xlsx")


main()
