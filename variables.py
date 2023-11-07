import os
from config import *

# bot name
bot_name = BOT_NAME
bot_username = BOT_USERNAME

# message for /start command
welcome_message = '''Welcome to @lmbachel_bot

Send me a link from spotify and I'll download it for you.

It can be a track link like:
https://open.spotify.com/track/734dz1YaFITwawPpM25fSt

Or an album link like:
https://open.spotify.com/album/0Lg1uZvI312TPqxNWShFXL

Or a playlist link like:
https://open.spotify.com/playlist/37i9dQZF1DWX4UlFW6EJPs


NOTE: I might not answer right away but I always answer😉❤️


©️ Creator: @wissemgrari'''

# message for /info command
info_message = '''This bot's whole open source is available in github.'''


deezer_link_message = '''This bot is created to download from spotify but you sent a deezer link.
Send the link of your track/album/playlist from spotify'''

soundcloud_link_message = '''This bot is created to download from spotify but you sent a soundcloud link.
Send the link of your track/album/playlist from spotify'''

youtube_link_message = '''This bot is created to download from spotify but you sent a youtube link.
Send the link of your track/album/playlist from spotify'''

end_message = '''end.

Rabi m3a zawali'''



wrong_link_message = '''This is not a correct spotify link.

You should send a track link like:
https://open.spotify.com/track/734dz1YaFITwawPpM25fSt

Or an album link like:
https://open.spotify.com/album/0Lg1uZvI312TPqxNWShFXL

Or a playlist link like:
https://open.spotify.com/playlist/37i9dQZF1DWX4UlFW6EJPs'''

# download directory
directory = "./output/"

# csv files path
db_csv_path = "./csv_files/db.csv"
users_csv_path = "./csv_files/users.csv"

# env variables
bot_api = BOT_API
database_channel = MUSIC_DATABASE_ID

# spotify regex patterns
spotify_shortened_link_pattern = r'https:\/\/spotify\.link\/[A-Za-z0-9]+'
spotify_track_link_pattern = r'https:\/\/open\.spotify\.com\/(intl-[a-zA-Z]{2}\/)?track\/[a-zA-Z0-9]+'
spotify_album_link_pattern = r'https:\/\/open\.spotify\.com\/(intl-[a-zA-Z]{2}\/)?album\/[a-zA-Z0-9]+'
spotify_playlist_link_pattern = r'https:\/\/open\.spotify\.com\/(intl-[a-zA-Z]{2}\/)?playlist\/[a-zA-Z0-9]+'
spotify_correct_link_pattern = spotify_track_link_pattern + "|" + spotify_album_link_pattern + "|" + spotify_playlist_link_pattern + "|" + spotify_shortened_link_pattern
#spotify_track_id_pattern = r"spotify\.com\/track\/(\w+)(?:\?.*)?$"
#spotify_album_id_pattern = r"spotify\.com\/album\/(\w+)(?:\?.*)?$"
#spotify_playlist_id_pattern = r"spotify\.com\/playlist\/(\w+)(?:\?.*)?$"
deezer_link_pattern = r'https?:\/\/(?:www\.)?deezer\.com\/(?:\w{2}\/)?(?:\w+\/)?(?:track|album|artist|playlist)\/\d+'
soundcloud_link_pattern = r"(?:https?://)?(?:www\.)?soundcloud\.com/([a-zA-Z0-9-_]+)/([a-zA-Z0-9-_]+)"
youtube_link_pattern = r"(?:(?:https?:)?//)?(?:www\.)?(?:(?:youtube\.com/(?:watch\?.*v=|embed/|v/)|youtu.be/))([\w-]{11})"

# log chanel
log_bot_url = "https://api.telegram.org/bot" + bot_api + "/"
log_channel_id = LOG_CHANNEL_ID

# specify to use warp or not
warp_mode = False

# spotify
spotify_client_id = SPOTIFY_CLIENT_ID
spotify_client_secret = SPOTIFY_CLIENT_SECRET

# database csv columns
db_time_column = 0
db_sp_track_column = 1
db_tl_audio_column = 2

# users csv columns
ucsv_user_id_column = 0
ucsv_last_time_column = 1

# data and time format in csv files
datetime_format = "%Y/%m/%d-%H:%M:%S"

# necessary time in seconds for user to wait between 2 requests
user_request_wait = 30

unsuccessful_process_message = '''Sorry, my process wasn't sucessful :('''
