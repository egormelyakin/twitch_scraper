from twitch import TwitchAPI
from video import Video


def link(uri, label=None):
    if label is None:
        label = uri
    parameters = ''
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format(parameters, uri, label)


class Clip:
    def __init__(self, data: dict) -> None:
        self.data = data

    def __str__(self) -> str:
        text = ''
        text += f'[{link(self.data["url"], "URL")}] '
        text += f"({self.data['view_count']:,}) "
        max_len = 40
        if len(self.data["title"]) > max_len:
            text += f"{self.data['title'][:max_len-3]}..."
        else:
            text += self.data["title"]
        return text

    @staticmethod
    def print_clips(clips: list['Clip']) -> None:
        if not clips:
            print("No clips.")
            return
        number_len = len(str(len(clips)))
        views_len = len(f"{clips[0].data['view_count']:,}")

        for i, clip in enumerate(clips):
            text = f'{i+1:0>{number_len}}. '
            text += f'[{link(clip.data["url"], "URL")}] '
            text += f"({clip.data['view_count']:>{views_len},}) "
            max_len = 60
            if len(clip.data["title"]) > max_len:
                text += f"{clip.data['title'][:max_len-3]}..."
            else:
                text += clip.data["title"]
            print(text)

    @staticmethod
    def get_by_video(api: TwitchAPI, video: Video, count: int = 10) -> list['Clip']:
        params = {
            "broadcaster_id": video.data["user_id"],
            "started_at": video.data["created_at"],
        }

        def filter_fn(clip): return clip["video_id"] == video.data["id"]
        return Clip.get_clip_loop(api, params, count, filter_fn)

    @staticmethod
    def get_clip_loop(
        api: TwitchAPI,
        params: dict,
        count: int,
        filter_fn: callable = None
    ) -> list['Clip']:
        url = "https://api.twitch.tv/helix/clips"
        clips = []
        cursor = None
        while len(clips) < count:
            if cursor:
                params["after"] = cursor
            params["first"] = min(count - len(clips), 100)
            data = api.get_data(url, params)
            if filter_fn:
                clips.extend(filter(filter_fn, data["data"]))
            else:
                clips.extend(data["data"])
            print(f"Getting clips... {len(clips)}/{count}", end="\r")
            cursor = data.get("pagination", {}).get("cursor")
            if not cursor:
                print("No more clips.")
                break
        print(f"Got {len(clips)} clips."+(" "*20))
        return [Clip(clip) for clip in clips]
