import json
import requests
from datetime import datetime
import re
import ssl
import smtplib

from email.message import EmailMessage
import eyed3
from tinytag import TinyTag


def json_loader(key) -> list:
    with open('Json/messages.json', 'r') as r:
        json_data = json.load(r)

    return json_data[key]


def json_parser(key: str, value) -> None:
    NEW_DATA_KEY = key #Write Key Here
    NEW_DATA_VALUE = value #Write Value Here
    # When changing the holidays please make sure that you spell the key as holidays and copy the value as plain text (don't include links)

    with open('Json/messages.json', 'r') as r:
        data = json.load(r)

    data[str(NEW_DATA_KEY)] = NEW_DATA_VALUE

    with open('Json/messages.json', 'w') as w:
        json.dump(data, w)

    print('SuccessFully Updated:', NEW_DATA_KEY)

def contains_link(message: str):
    url_expression = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    result: list = re.findall(url_expression, message.lower())
    if result == []:
        return False
    else:
        return True
    
def send_email(subject: str, body: str, from_: str, to_: str, password: str) -> None:
    # Setting Variables
    em = EmailMessage()
    em['From'] = from_
    em['To'] = to_
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    # Login and send Email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(from_, password)
        smtp.sendmail(from_, to_, em.as_string())

def update_holidays(log, processed: str, full_name: str, user_name: str) -> None:
    if contains_link(processed):
        json_parser('holidays', processed.split('/')[-1])
    else:
        json_parser('holidays', processed)
        log("UpdateHolidays Command", 'Updated Holidays Message', f'Updated to https://t.me/habtemaryam26/{processed.split("/")[-1]}', log_level="INFO")
        log("UpdateHolidays Command", f'Sent Message to{full_name}({user_name})', 'For Private Chat', log_level="INFO")

async def send_comment(update, context, comment, full_name, user_name):
    await context.bot.send_message(5282771696, comment)
    
    send_email('Comment From telegram bot',
        f'''Message From: {full_name}({user_name})
        date: {datetime.now().strftime("%d-%m-%Y, %H:%M:%S")}
        Comment: {comment}''',
        'habtemaryam26bot@gmail.com',
        'bitaniagezahegn3@gmail.com',
        'lhdxigvfqzwrmqpy')


def change_meta_data(artist: str,
                    album: str, 
                    album_artist: list, 
                    title: str, 
                    track_num: int = None,  
                    genre: str = 'Mezmur', 
                    date = datetime.now().strftime('%Y'),
                    art: str = None
                    ) -> None:
    
    FILE_NAME = 'Audio/audio_file.mp3'
    
    audiofile = eyed3.load(FILE_NAME, )
    eyed3.log.setLevel("ERROR")

    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.album_artist = ', '.join(album_artist)
    audiofile.tag.title = title
    audiofile.tag.track_num = track_num
    audiofile.tag.genre = genre
    audiofile.tag.recording_date = date
    try:
        with open(art, "rb") as cover_art:
            audiofile.tag.images.set(3, cover_art.read(), "image/jpeg")
    except:
        pass
    audiofile.tag.save()

def show_meta_data(get_img: bool=False) -> list:
    
    FILE_NAME = 'Audio/audio_file.mp3'
    
    tag = TinyTag.get(FILE_NAME, image=get_img, ignore_errors=True)
    result: list = [
    str(tag.album),         # album as string
    str(tag.albumartist),   # album artist as string
    str(tag.artist),        # artist name as string
    str(tag.audio_offset),  # number of bytes before audio data begins
    str(tag.bitdepth),      # bit depth for lossless audio
    str(tag.bitrate),       # bitrate in kBits/s
    str(tag.comment),       # file comment as string
    str(tag.composer),      # composer as string 
    str(tag.disc),          # disc number
    str(tag.disc_total),    # the total number of discs
    str(tag.duration),      # duration of the song in seconds
    str(tag.filesize),      # file size in bytes
    str(tag.genre),         # genre as string
    str(tag.samplerate),    # samples per second
    str(tag.title),         # title of the song
    str(tag.track),         # track number as string
    str(tag.track_total),   # total number of tracks as string
    str(tag.year),          # year or date as string
    str(tag.extra),         # a dict of additional data
    str(tag.get_image())    # Cover art of file
    ]

    return result

def download_file(FILE_NAME):

    response = requests.get(FILE_NAME)

    with open(f"Audio/audio_file.mp3", "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    # print(json_loader('holidays'))
    pass