import re
import vlc
from time import sleep
from packages import pafy
import urllib.request
import spotify_tracker
from getpass import getpass

class GetVideo:
    def __init__(self, access_token) -> None:
        self.spotify_access_token = access_token

    def get_list_of_videos(self, song_title, artist):

        re_pattern = r"watch\?v=(\S{11})"
        song_title = self.format_youtube_query(song_title, artist=artist)
        try:
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query={}".format(song_title))
            html = html.read().decode()
            video_refs = re.findall(re_pattern, html)
            print("Found video links")
            return video_refs
        except:
            print("Unable to find videos for {}".format(song_title))


    def get_offical_music_video(self, youtube_links):
        
        watch = "https://www.youtube.com/watch?v={}"
        re_patterns = [r"offical video", r"Official Video", r"Offical Music Video", r"offical music video"]

        for _link in youtube_links:
            html = urllib.request.urlopen(watch.format(_link))
            html = html.read().decode()
            for _pattern in re_patterns:
                found = re.findall(_pattern, html)
                if found:
                    print("Found best guess for music video")
                    return watch.format(_link)


    def format_youtube_query(self, song_title, artist=None):
        
        query = ""

        if artist:
            query = song_title + "+" + artist
            query = query.replace(" ", "+")
        else:
            query = song_title.replace(" ", "+")
        
        return query
 
    def play_video(self, youtube_url, current_song):
        print("Playing video")
        st = spotify_tracker.SpotifyTracker(self.spotify_access_token)
        video = pafy.new(youtube_url)
        video = video.streams[0]
        media = vlc.MediaPlayer(video.url)
        media.audio_set_volume(0)
        media.toggle_fullscreen()
        media.play()

        sleep(5)
        check = dict()
        while media.is_playing():
            check = st.get_current_song()
            if check == current_song:
                sleep(1)
            else:
                media.stop()
                break