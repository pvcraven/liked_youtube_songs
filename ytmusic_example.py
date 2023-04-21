import json
from ytmusicapi import YTMusic

from openpyxl import Workbook


def main():

    try:
        print("Authorizing...")
        ytmusic = YTMusic("oauth.json")
    except json.decoder.JSONDecodeError:
        print("Error reading oauth.json file. Run 'ytmusicapi oauth' from the command line to generate.")
        return

    print("Getting liked songs...")
    songs = ytmusic.get_liked_songs(2000)

    # print(songs)
    # print(json.dumps(songs, indent=4))
    print("Writing out spreadsheet...")

    workbook = Workbook()
    work_sheet = workbook.active

    for track in songs['tracks']:
        row = []
        title = track['title']
        row.append(title)
        for artists in track['artists']:
            artist = artists['name']
            row.append(artist)

        work_sheet.append(row)

    workbook.save("liked_songs.xlsx")
    print("Finished. Results in liked_songs.xlsx")


main()
