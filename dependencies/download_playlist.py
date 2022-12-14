from dependencies.functions import format_title
from os import system as cmd, makedirs, environ, path, pathsep, getcwd
from pytube import Playlist, YouTube, extract
from shutil import rmtree
from requests import get
from music_tag import load_file
from termcolor import cprint, colored


def start():

    playlist_symbol_tilde = colored('[~]', 'yellow', attrs=['bold'])
    playlist_text_beside1 = colored('Progress: ', 'white', attrs=['bold'])

    playlist_symbol_plus = colored('[+]', 'yellow', attrs=['bold'])
    playlist_text_beside2 = colored('The playlist was downloaded successfully!', 'white', attrs=['bold'])

    playlist_symbol_line = colored('-', 'white', attrs=['bold'])

    cmd('cls')

    print()
    cprint("     _ _   _       _                     _ _               _                           _", 'yellow', attrs=['bold'])
    cprint(" ___|_| |_| |_ _ _| |_   ___ ___ _____  / | |_ ___ ___ ___|_|___ _ _ ___ ___ ___ ___ _| |___ ___", 'yellow', attrs=['bold'])
    cprint("| . | |  _|   | | | . |_|  _| . |     |/ /|   | -_|   |  _| | . | | | -_|___|  _| . | . | -_|  _|", 'yellow', attrs=['bold'])
    cprint("|_  |_|_| |_|_|___|___|_|___|___|_|_|_|_/ |_|_|___|_|_|_| |_|_  |___|___|   |___|___|___|___|_|", 'yellow', attrs=['bold'])
    cprint("|___|                                                         |_|", 'yellow', attrs=['bold'])
    print()
    print()

    playlist_text3_examples = colored('Example: ', 'red', attrs=['bold'])
    playlist_text4_links = colored('"https://youtu.be/xXxXxXxX_xX?list=xXxXxXxXxXxXxXxXxXxXxXxXxXxX-xXxXx"', 'white', attrs=['bold'])
    playlist_text2_input = colored('YouTube - Playlist URL: ', 'red', attrs=['bold'])
    print(playlist_text3_examples + playlist_text4_links)
    url = input(playlist_text2_input)
    print()

    finished_downloads_counter = 0

    userprofile_name = environ['userprofile']

    playlist = Playlist(url)
    for video in playlist.videos:
        formatted_playlist_title = format_title(playlist.title)
        makedirs(fr'{userprofile_name}\AppData\Local\Instaplay Project\temp', exist_ok=True)
        video_title_in_playlist = format_title(video.title)
        video.streams.filter(only_audio=True).first().download(output_path=fr'{userprofile_name}\AppData\Local\Instaplay Project\temp', filename=video_title_in_playlist + '.mp3')

        # Convert to MP3
        userprofile_name = environ['userprofile']
        environ['PATH'] += pathsep + path.join(getcwd(), fr'{userprofile_name}\AppData\Local\Instaplay Project\dependencies')
        cmd_formatted_title = format_title(video_title_in_playlist) + '.mp3'
        makedirs(fr'Playlists\{formatted_playlist_title}', exist_ok=True)
        cmd(fr'ffmpeg -i "%userprofile%\AppData\Local\Instaplay Project\temp\{cmd_formatted_title}" -b:a 128K -vn "Playlists\{formatted_playlist_title}\{cmd_formatted_title}" -y -loglevel quiet')

        # Adding metadata...
        userprofile_name = environ['userprofile']
        r = get(fr'https://img.youtube.com/vi/{video.video_id}/maxresdefault.jpg', allow_redirects=True)
        open(fr'{userprofile_name}\AppData\Local\Instaplay Project\temp\{video_title_in_playlist}.jpg', 'wb').write(r.content)
        publish_year = str(video.publish_date).split('-')[0]

        yt = YouTube(url)
        f = load_file(fr'Playlists\{formatted_playlist_title}\{video_title_in_playlist}.mp3')
        f['artwork'] = open(fr'{userprofile_name}\AppData\Local\Instaplay Project\temp\{video_title_in_playlist}.jpg', 'rb').read()
        f['tracktitle'] = video_title_in_playlist
        f['artist'] = yt.author
        f['year'] = publish_year
        f['album'] = formatted_playlist_title
        f['albumartist'] = yt.author
        f['genre'] = 'Music'
        f.save()

        # Video download counting...
        finished_downloads_counter = finished_downloads_counter + 1
        playlist_total_videos = len(playlist.video_urls)
        counting_progress_and_total_videos = colored(f'{finished_downloads_counter} of {playlist_total_videos}', 'white', attrs=['bold'])

        playlist_formatted_video_title_colored = colored(video_title_in_playlist, 'white', attrs=['bold'])
        print(f'{playlist_symbol_tilde} {playlist_text_beside1}100.0% {playlist_symbol_line} {counting_progress_and_total_videos} {playlist_symbol_line} Music: {playlist_formatted_video_title_colored}')

    # Deleting Temporary Files...
    rmtree(fr'{userprofile_name}\AppData\Local\Instaplay Project\temp', ignore_errors=True)
    print()

    print(f'{playlist_symbol_plus} {playlist_text_beside2}')
    print()
