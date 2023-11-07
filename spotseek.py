#!/usr/bin/python3
import telebot
from telebot import types
import os
import re
from functions import download, file_list, clear_files
from variables import welcome_message, info_message, deezer_link_message, soundcloud_link_message, youtube_link_message, end_message, wrong_link_message, directory, bot_api, database_channel, spotify_shortened_link_pattern, spotify_track_link_pattern, spotify_album_link_pattern, spotify_playlist_link_pattern, spotify_correct_link_pattern, deezer_link_pattern, soundcloud_link_pattern, youtube_link_pattern, db_csv_path, users_csv_path, db_time_column, db_sp_track_column, db_tl_audio_column, ucsv_user_id_column, ucsv_last_time_column, user_request_wait, bot_name, bot_username, unsuccessful_process_message
from log import log, log_channel_id
from csv_functions import csv_read, db_csv_append, get_row_list_csv_search, get_row_index_csv_search, csv_sort, allow_user
from spotify import get_redirect_link, get_link_type, get_track_ids, get_valid_spotify_links
from mp3 import change_cover_image, get_track_duration, get_artist_name_from_track, get_track_title
import threading # to use lock
import time # for sleep

# initialize and get ready
bot = telebot.TeleBot(bot_api)
clear_files(directory)

# Create a mutex lock
lock = threading.Lock()

@bot.message_handler(commands = ['start'])
def start_message(message):
    bot.send_message(message.chat.id, welcome_message, disable_web_page_preview=True)
    log(bot_name + " log:\n/start command sent from user: " + str(message.chat.id))

@bot.message_handler(commands = ['info'])
def start_message(message):
    bot.send_message(message.chat.id, info_message, parse_mode="Markdown", disable_web_page_preview=True)
    log(bot_name + " log:\n/info command sent from user: " + str(message.chat.id))

@bot.message_handler(regexp = deezer_link_pattern)
def deezer_link_handler(message):
    bot.send_message(message.chat.id, deezer_link_message, parse_mode="Markdown", disable_web_page_preview=True)
    log(bot_name + " log:\ndeezer link sent from user: " + str(message.chat.id))

@bot.message_handler(regexp = soundcloud_link_pattern)
def soundcloud_link_handler(message):
    bot.send_message(message.chat.id, soundcloud_link_message, parse_mode="Markdown", disable_web_page_preview=True)
    log(bot_name + " log:\nsoundcloud link sent from user: " + str(message.chat.id))

@bot.message_handler(regexp = youtube_link_pattern)
def youtube_link_handler(message):
    bot.send_message(message.chat.id, youtube_link_message, parse_mode="Markdown", disable_web_page_preview=True)
    log(bot_name + " log:\nyoutube link sent from user: " + str(message.chat.id))

@bot.message_handler(regexp = spotify_correct_link_pattern)
def handle_correct_spotify_link(message):
    temp_message1 = bot.send_message(message.chat.id, "Ok, wait for me to process...")
    log(bot_name + " log:\ncorrect link pattern from user: " + str(message.chat.id) + " with contents of:\n" + message.text)
    try:
        # make it one user at a time
        with lock:
            if allow_user(message.chat.id):
                log(bot_name + " log:\nuser " + str(message.chat.id) + " is allowed to use the bot.")
                try:
                    bot.delete_message(message.chat.id, temp_message1.message_id)
                except:
                    pass
                temp_message2 = bot.send_message(message.chat.id, "Start downloading...\nIt can be very fast or very slow, be patient.")
                clear_files(directory)
                valid_spotify_links_in_user_text = get_valid_spotify_links(message.text)

                # if user sends multiple links combined with normal text we only extract and analyze first one so the bot won't be spammed
                first_link = valid_spotify_links_in_user_text[0]

                # if the link is shortened convert "spotify.link" to "open.spotify.com"
                if get_link_type(first_link) == "shortened":
                    log(bot_name + " log:\nshortened link sent from user: " + str(message.chat.id))
                    first_link = get_redirect_link(first_link)
                    if first_link is None or first_link.strip() == "":
                        log(bot_name + " log:\nerror in handling short link") # TO-DO: doesn't run, fix later
                        return

                
                matches = get_track_ids(first_link)
                if len(matches) > 1000:
                    bot.send_message(message.chat.id, "Bot can't download playlists more than 1000 tracks at the moment. This feature will be added later.")
                    log(bot_name + " log:\nPlaylist more than 1000 tracks from user: " + str(message.chat.id))
                    return
                if matches:
                    at_least_one_track_downloaded = False
                    # download every link:
                    for track_id in matches:
                        time.sleep(0.5) # wait a little to alleviate telegram bot limit
                        # (https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this)
                        link = "https://open.spotify.com/track/" + track_id 
                        existed_row = get_row_list_csv_search(db_csv_path, db_sp_track_column, track_id)
                        if existed_row:
                            telegram_audio_id = existed_row[db_tl_audio_column]
                            bot.send_audio(message.chat.id, telegram_audio_id, caption=bot_username)
                            at_least_one_track_downloaded = True
                        else:
                            download(link)
                            # upload to telegram and delete from hard drive:
                            for file in file_list(directory): # we send every possible file in directory to bypass searching for file name
                                change_cover_image(file, "cover.jpg")
                                audio = open(directory + file, 'rb')
                                # check file size because of telegram 50MB limit
                                file_size = os.fstat(audio.fileno()).st_size
                                if file_size > 50_000_000:
                                    too_large_file_error = "Sorry, size of \"{f}\" is more than 50MB and can't be sent".format(f = file)
                                    bot.send_message(message.chat.id, too_large_file_error)
                                else:
                                    # get track metadata to be shown in telegram
                                    track_duration = get_track_duration(directory + file)
                                    track_artist = get_artist_name_from_track(directory + file)
                                    track_title = get_track_title(directory + file)
                                    thumb_image = open(directory + "cover_low.jpg", 'rb')
                                    # first send to database_channel:
                                    audio_message = bot.send_audio(database_channel, \
                                            audio, thumb=thumb_image, \
                                            caption=bot_username, \
                                            duration=track_duration, \
                                            performer=track_artist, \
                                            title=track_title)
                                    # add file to database
                                    db_csv_append(db_csv_path, track_id, audio_message.audio.file_id)
                                    # second send to user:
                                    bot.send_audio(message.chat.id, audio_message.audio.file_id, caption=bot_username)
                                    at_least_one_track_downloaded = True
                                # remove files from drive
                                clear_files(directory)
                    # finish message for user
                    try:
                        bot.delete_message(message.chat.id, temp_message2.message_id)
                    except:
                        pass
                    if at_least_one_track_downloaded:
                        bot.send_message(message.chat.id, end_message, parse_mode="Markdown", disable_web_page_preview=True)
                    else:
                        bot.send_message(message.chat.id, unsuccessful_process_message, parse_mode="Markdown")
                else:
                    log(bot_name + " log:\nNo matches found. \
                                     this line should not happen in normal behavior\
                                     becuase it is already checked with regex, if happens is a bug.")
                    bot.send_message(message.chat.id, unsuccessful_process_message, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "you should wait " + str(user_request_wait) + " seconds between requests")
                log(bot_name + " log:\n⏰user " + str(message.chat.id) + " isn't allowed to use the bot")
    except Exception as e:
        log(bot_name + " log:\nAn error occurred: " + str(e))
        bot.send_message(message.chat.id, unsuccessful_process_message, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def all_other_forms_of_messages(message):
    bot.reply_to(message, wrong_link_message, disable_web_page_preview=True)
    log(bot_name + " log:\n❌wrong link pattern from user: " + str(message.chat.id) + " with contents of:\n" + message.text)

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()
