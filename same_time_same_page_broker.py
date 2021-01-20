import argparse
import logging
import subprocess
from os import path
from utils import get_json_content


logger = logging.getLogger(__name__)
CURRENT_PATH = path.dirname(path.abspath(__file__))


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fake-users', type=int, default=3,
                        help='the number of fake users ')
    return parser.parse_args()


def main():
    args = _parse_args()
    cmd = get_json_content(path.join(CURRENT_PATH, 'config.json')).get(
        'SAME_PAGE_USER_CMD')
    for user_num in range(args.fake_users):
        logger.info('user number: {}'.format(user_num))
        subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
    main()
