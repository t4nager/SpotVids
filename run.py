import spotify_tracker
import get_video
from getpass import getpass

def main():
    spotify_token = getpass("Please enter Spotify Access Token: ")
    video_player = get_video.GetVideo(spotify_token)
    
    while True:
        song = spotify_tracker.SpotifyTracker(spotify_token)
        song = song.get_current_song()
        videos = video_player.get_list_of_videos(song.get("song"), song.get("artist"))
        offical_video = video_player.get_offical_music_video(videos)
        video_player.play_video(offical_video, song)

if __name__ == "__main__":
    main()