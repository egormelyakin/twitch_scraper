from twitch import TwitchAPI


class Video:
    def __init__(self, data: dict) -> None:
        self.data = data

    @staticmethod
    def get_by_id(api: TwitchAPI, video_id: str) -> "Video":
        url = "https://api.twitch.tv/helix/videos"
        params = {"id": video_id}
        data = api.get_data(url, params)["data"][0]
        return Video(data)
