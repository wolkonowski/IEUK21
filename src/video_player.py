"""A video player class."""

from .video_library import VideoLibrary
import random


class VideoException(Exception):
    def __init__(self, command, message):
        self.command = command
        self.message = f"Cannot {self.command} video: {message}"
        super().__init__(f"Cannot {self.command} video: {message}")


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing_id = ""
        self.paused = False

    def get_title(self):
        return self._video_library.get_video(self.playing_id)._title

    def number_of_videos(self):
        num = self._video_library.get_number_of_videos()
        print(f"{num} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")

        def index(x):
            return x._title
        for video in sorted(self._video_library.get_all_videos(), key=index):
            tags = ""
            for tag in video._tags:
                tags += f"{tag} "
            if tags != "":
                tags = tags[:-1]
            print(f"\t{video._title} ({video._video_id}) [{tags}]")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        try:
            if video is None:
                raise VideoException("play", "Video does not exist")
            else:
                if self.playing_id != "":
                    self.stop_video()
                self.playing_id = video_id
                self.paused = False
                print(f"Playing video: {self.get_title()}")
        except VideoException as e:
            print(e.message)

    def stop_video(self):
        """Stops the current video."""
        try:
            if self.playing_id != "":
                title = self.get_title()
                self.playing_id = ""
                print(f"Stopping video: {title}")
            else:
                raise VideoException("stop", "No video is currently playing")
        except VideoException as e:
            print(e.message)

    def play_random_video(self):
        """Plays a random video from the video library."""
        num = random.randrange(self._video_library.get_number_of_videos())
        self.play_video(self._video_library.get_all_videos()[num]._video_id)

    def pause_video(self):
        """Pauses the current video."""
        try:
            if self.playing_id == "":
                raise VideoException("pause", "No video is currently playing")
            if self.paused:
                print(f"Video already paused: {self.get_title()}")
            else:
                self.paused = True
                print(f"Pausing video: {self.get_title()}")
        except VideoException as e:
            print(e.message)

    def continue_video(self):
        """Resumes playing the current video."""
        try:
            if self.playing_id == "":
                raise VideoException("continue",
                                     "No video is currently playing")
            if self.paused is False:
                raise VideoException("continue", "Video is not paused")
            self.paused = False
            print(f"Continuing video: {self.get_title()}")
        except VideoException as e:
            print(e.message)

    def show_playing(self):
        """Displays video currently playing."""
        if self.playing_id == "":
            print("No video is currently playing")
            return
        video = self._video_library.get_video(self.playing_id)
        tags = ""
        for tag in video._tags:
            tags += f"{tag} "
        if tags != "":
            tags = tags[:-1]
        message = f"Currently playing: \
            {video._title} ({video._video_id}) [{tags}]"
        if self.paused:
            message += " - PAUSED"
        print(message)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("create_playlist needs implementation")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        print("add_to_playlist needs implementation")

    def show_all_playlists(self):
        """Display all playlists."""

        print("show_all_playlists needs implementation")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("show_playlist needs implementation")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("deletes_playlist needs implementation")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
