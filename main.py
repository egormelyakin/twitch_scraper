from twitch import TwitchAPI
from video import Video
from clip import Clip

from datetime import datetime, timedelta
import sys


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["hours"] = f"{hours:02d}"
    d["minutes"] = f"{minutes:02d}"
    d["seconds"] = f"{seconds:02d}"
    return fmt.format(**d)


def main() -> None:
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    video_id = sys.argv[3]

    api = TwitchAPI(client_id, client_secret)
    video = Video.get_by_id(api, video_id)
    clips = Clip.get_by_video(api, video, 500)
    path = f"out/{video_id}.txt"

    label = f'{video.data["id"]}'
    label += f'_{video.data["user_login"].upper()}'
    label += f'_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

    text_data = f'{label}\n'
    max_views = 0
    if clips:
        max_views = clips[0].data["view_count"]
    for clip in clips:
        start = timedelta(seconds=clip.data["vod_offset"])
        end = start + timedelta(seconds=clip.data["duration"])
        start = strfdelta(start, "{hours}:{minutes}:{seconds}")
        end = strfdelta(end, "{hours}:{minutes}:{seconds}")

        label = f"[{clip.data['view_count']/max_views:.2%}]"
        label += f" ({clip.data['view_count']:,})"
        label += f" {clip.data['title']}"

        text_data += f'{start} {end} {label}\n'

    with open(path, "w", encoding='utf-8') as f:
        f.write(text_data)

    print(f"Made {api.requests} requests.")


if __name__ == "__main__":
    main()
