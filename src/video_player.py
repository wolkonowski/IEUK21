"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random


class VideoException(Exception):
    def __init__(self, command, message):
        self.command = command
        self.message = f"Cannot {self.command} video: {message}"
        super().__init__(f"Cannot {self.command} video: {message}")


class PlaylistException(Exception):
    def __init__(self, command, message, name="playlist"):
        self.command = command
        self.message = f"Cannot {self.command} {name}: {message}"
        super().__init__(f"Cannot {self.command} {name}: {message}")


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing_id = ""
        self.paused = False
        self.playlists = {}

    def get_current_title(self):
        return self.get_title(self.playing_id)

    def get_title(self, video_id):
        return self._video_library.get_video(video_id)._title

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
            msg = ""
            if video._video_id in self._video_library.flagged:
                reason = self._video_library.flagged[video._video_id]
                msg = f" - FLAGGED (reason: {reason})"
            print(f"\t{video._title} ({video._video_id}) [{tags}]{msg}")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        try:
            if video is None:
                raise VideoException("play", "Video does not exist")
            if video_id in self._video_library.flagged.keys():
                reason = self._video_library.flagged[video_id]
                raise VideoException("play", f"Video is currently "
                                     f"flagged (reason: {reason})")
            else:
                if self.playing_id != "":
                    self.stop_video()
                self.playing_id = video_id
                self.paused = False
                print(f"Playing video: {self.get_current_title()}")
        except VideoException as e:
            print(e.message)

    def stop_video(self):
        """Stops the current video."""
        try:
            if self.playing_id != "":
                title = self.get_current_title()
                self.playing_id = ""
                print(f"Stopping video: {title}")
            else:
                raise VideoException("stop", "No video is currently playing")
        except VideoException as e:
            print(e.message)

    def play_random_video(self):
        """Plays a random video from the video library."""
        num = self._video_library.get_number_of_legal_videos()
        if num == 0:
            print("No videos available")
            return
        rand = random.randrange(num)
        self.play_video(self._video_library.get_legal_videos()[rand]._video_id)

    def pause_video(self):
        """Pauses the current video."""
        try:
            if self.playing_id == "":
                raise VideoException("pause", "No video is currently playing")
            if self.paused:
                print(f"Video already paused: {self.get_current_title()}")
            else:
                self.paused = True
                print(f"Pausing video: {self.get_current_title()}")
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
            print(f"Continuing video: {self.get_current_title()}")
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
        message = \
            f"Currently playing: {video._title} ({video._video_id}) [{tags}]"
        if self.paused:
            message += " - PAUSED"
        print(message)

    def show_video(self, video_id):
        video = self._video_library.get_video(video_id)
        tags = ""
        for tag in video._tags:
            tags += f"{tag} "
        if tags != "":
            tags = tags[:-1]
        msg = ""
        if video_id in self._video_library.flagged:
            reason = self._video_library.flagged[video_id]
            msg = f" - FLAGGED (reason: {reason})"
        return f"{video._title} ({video_id}) [{tags}]{msg}"

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            if playlist_name.upper() in self.playlists.keys():
                raise PlaylistException(
                    "create", "A playlist with the same name already exists")
            self.playlists[playlist_name.upper()] = Playlist(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")
        except PlaylistException as e:
            print(e.message)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        try:
            if playlist_name.upper() not in self.playlists.keys():
                raise PlaylistException(
                    "add video to", "Playlist does not exist",
                    name=playlist_name)
            if self._video_library.get_video(video_id) is None:
                raise PlaylistException(
                    "add video to", "Video does not exist",
                    name=playlist_name)
            if video_id in self._video_library.flagged:
                reason = self._video_library.flagged[video_id]
                raise PlaylistException(
                    "add video to",
                    f"Video is currently flagged (reason: {reason})",
                    name=playlist_name)
            if video_id in self.playlists.get(playlist_name.upper()).videos:
                raise PlaylistException(
                    "add video to", "Video already added",
                    name=playlist_name)
            self.playlists.get(playlist_name.upper()).videos.add(video_id)
            title = self.get_title(video_id)
            print(f"Added video to {playlist_name}: {title}")
        except PlaylistException as e:
            print(e.message)

    def show_all_playlists(self):
        """Display all playlists."""
        if not self.playlists:
            print("No playlists exist yet")
            return
        print("Showing all playlists:")
        for elem in sorted(self.playlists.keys()):
            print(f"\t{self.playlists.get(elem)._name}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            if playlist_name.upper() not in self.playlists.keys():
                raise PlaylistException(
                    "show playlist", "Playlist does not exist",
                    name=playlist_name)
            print(f"Showing playlist: {playlist_name}")
            p = self.playlists.get(playlist_name.upper())
            if len(p.videos) == 0:
                print("\tNo videos here yet")
            else:
                for v in p.videos:
                    print(f"\t{self.show_video(v)}")
        except PlaylistException as e:
            print(e.message)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        try:
            if playlist_name.upper() not in self.playlists.keys():
                raise PlaylistException(
                    "remove video from", "Playlist does not exist",
                    name=playlist_name)
            if self._video_library.get_video(video_id) is None:
                raise PlaylistException(
                    "remove video from", "Video does not exist",
                    name=playlist_name)
            p = self.playlists.get(playlist_name.upper())
            if video_id not in p.videos:
                raise PlaylistException(
                    "remove video from", "Video is not in playlist",
                    name=playlist_name)
            p.videos.remove(video_id)
            print(f"Removed video from {playlist_name}: "
                  f"{self.get_title(video_id)}")
        except PlaylistException as e:
            print(e.message)

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            if playlist_name.upper() not in self.playlists.keys():
                raise PlaylistException(
                    "clear playlist", "Playlist does not exist",
                    name=playlist_name)
            p = self.playlists.get(playlist_name.upper())
            p.videos.clear()
            print(f"Successfully removed all videos from {playlist_name}")
        except PlaylistException as e:
            print(e.message)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            if playlist_name.upper() not in self.playlists.keys():
                raise PlaylistException(
                    "delete playlist", "Playlist does not exist",
                    name=playlist_name)
            p = self.playlists.get(playlist_name.upper())
            p.videos.clear()
            print(f"Deleted playlist: {playlist_name}")
        except PlaylistException as e:
            print(e.message)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        results = [v for v in self._video_library.get_legal_videos()
                   if search_term.upper() in v._title.upper()]
        if not results:
            print(f"No search results for {search_term}")
            return

        def index(x):
            return x._title
        results = sorted(results, key=index)
        print(f"Here are the results for {search_term}:")
        for count, video in enumerate(results):
            print(f"\t{count+1}) {self.show_video(video._video_id)}")
        print("Would you like to play any of the above? If yes, "
              "specify the number of the video.")
        print("If your answer is not a valid number, "
              "we will assume it's a no.")
        num = input()
        try:
            num = int(num)
        except ValueError:
            return
        num = num-1
        if num >= 0 and num < len(results):
            self.play_video(results[num]._video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        results = [v for v in self._video_library.get_legal_videos()
                   if video_tag.upper() in [t.upper() for t in v._tags]]
        if not results:
            print(f"No search results for {video_tag}")
            return

        def index(x):
            return x._title
        results = sorted(results, key=index)
        print(f"Here are the results for {video_tag}:")
        for count, video in enumerate(results):
            print(f"\t{count+1}) {self.show_video(video._video_id)}")
        print("Would you like to play any of the above? If yes, "
              "specify the number of the video.")
        print("If your answer is not a valid number, "
              "we will assume it's a no.")
        num = input()
        try:
            num = int(num)
        except ValueError:
            return
        num = num-1
        if num >= 0 and num < len(results):
            self.play_video(results[num]._video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        try:
            if self._video_library.get_video(video_id) is None:
                raise VideoException(
                    "flag", "Video does not exist")
            if video_id in self._video_library.flagged.keys():
                raise VideoException(
                    "flag", "Video is already flagged")
            if flag_reason == "":
                flag_reason = "Not supplied"
            self._video_library.flagged[video_id] = flag_reason
            if video_id == self.playing_id:
                self.stop_video()
            print(f"Successfully flagged video: {self.get_title(video_id)} "
                  f"(reason: {flag_reason})")
        except VideoException as e:
            print(e.message)

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        try:
            if self._video_library.get_video(video_id) is None:
                raise VideoException(
                    "remove flag from", "Video does not exist")
            if video_id not in self._video_library.flagged.keys():
                raise VideoException(
                    "remove flag from", "Video is not flagged")
            self._video_library.flagged.pop(video_id)
            print(f"Successfully removed flag from video: "
                  f"{self.get_title(video_id)}")
        except VideoException as e:
            print(e.message)
