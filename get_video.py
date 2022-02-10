import re
import vlc
from time import sleep
from packages import pafy
import urllib.request
import spotify_tracker
import random

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
        if youtube_links:
            for _link in youtube_links:
                html = urllib.request.urlopen(watch.format(_link))
                html = html.read().decode()
                for _pattern in re_patterns:
                    found = re.findall(_pattern, html)
                    if found:
                        print("Found best guess for music video")
                        return watch.format(_link)
        else:
            return self.get_random_visual()


    def format_youtube_query(self, song_title, artist=None):
        
        query = ""
        final_query = ""

        if artist:
            query = song_title + "+" + artist
            query = query.replace(" ", "+")
        else:
            query = song_title.replace(" ", "+")

        for _char in query:
            if _char.isalpha() or _char.isnumeric() or _char == "+":

                final_query = final_query + _char

        return final_query
 
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
        i = 1
        while media.is_playing():
            
            check = st.get_current_song()
            if check == current_song:
                sleep(1)

            else:
                media.stop()
                print("Stopping")
                break

    def get_random_visual(self):
        songs = [
            "https://www.youtube.com/watch?v=qUavbO3Y3gY&ab_channel=TrippyEverything",
            "https://www.youtube.com/watch?v=wFYFLpdrQL0&ab_channel=TrippyEverything",
            "https://www.youtube.com/watch?v=MagELQywiGI&ab_channel=Proli",
            "https://www.youtube.com/watch?v=oSmUI3m2kLk&ab_channel=4KRelaxationChannel",
            "https://www.youtube.com/watch?v=ef1wAfrMg5I&ab_channel=OneManWolfPack",
            "https://www.youtube.com/watch?v=DAlzlebbdPo&ab_channel=PRIMALEARTH",
            "https://www.youtube.com/watch?v=3PZ65s2qLTE&ab_channel=ScenicRelaxation",
            "https://www.youtube.com/watch?v=rhLy5LBj1kU&ab_channel=4KRelaxationChannel"
        ]

        return songs[random.randrange(len(songs))]