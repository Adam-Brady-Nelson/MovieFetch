# Torrent Movie Fetch Discord Bot

Uses an external movie API to download a movie based on an IMDb ID.
THIS PROGRAM ALONE DOES NOT ALLOW PIRACY, IT NEEDS VARIOUS OTHER DATA SOURCES

## Getting Started

### Dependencies

* python.py, requests, python-qbittorrent, asyncio, python-dotenv
* This was ran using Windows 10 and 11, but I cannot foresee any issue with other systems

### Installing

* Script can be placed and ran in anywhere

### Executing program

* How to run the program
* Create a .env file named ".env"

  ```
  TOKEN = '' #(Discord token)
  TRACKERS = '' #(e.g. &trudp://tracker.one:1234/announce&trudp://tracker.two:4321/announce) Note: Separated by &tr
  API_URL = '' #(Cannot be provided due to piracy laws and potential Github takedowns)
  SAVEDIR = '' #e.g. C:\ThisFolder
  USER = '' #(This is the WebUI username for QBittorrent)
  PASSWORD = '' #(This is the WebUI password for QBittorrent)
  ```

## Help

The inputted IMDB info needs to be a full link including https:// at this moment

## Authors

## Version History
