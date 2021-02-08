from ckick_into_page import run
import argparse
import logging
from os import path
from random import randrange

from eyescomment.youtube import YoutubeVideo, YoutubeChannel
from eyescomment.config import Config


logger = logging.getLogger(__name__)
CURRENT_PATH = path.dirname(path.abspath(__file__))


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fake-users', type=int, default=3,
                        help='the number of fake users ')
    return parser.parse_args()


def get_random_index(range_):
    return randrange(range_)


def get_random_channel_name():
    yt_channels = YoutubeChannel(
        host=Config.instance().get('PORTAL_SERVER'),
        cache_path=Config.instance().get('CACHE_DIR'),
        filter_params={"fields": {"channelName": True}})
    return yt_channels[get_random_index(len(yt_channels))].get('channelName')


def get_random_video_name(channel_name):
    yt_videos = YoutubeVideo(
        host=Config.instance().get('PORTAL_SERVER'),
        cache_path=Config.instance().get('CACHE_DIR'),
        filter_params={"where": {"channelName": channel_name}})
    return yt_videos[get_random_index(len(yt_videos))].get('videoName')


def main():
    args = _parse_args()
    Config.set_dir(path.join(CURRENT_PATH, 'config.json'))
    for user_num in range(args.fake_users):
        channel_name = get_random_channel_name()
        video_name = get_random_video_name(channel_name)
        run(channel_name=channel_name, video_name=video_name,delay=1)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
    main()
