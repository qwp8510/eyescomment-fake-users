from same_page import run
import argparse
import logging
from os import path


logger = logging.getLogger(__name__)
CURRENT_PATH = path.dirname(path.abspath(__file__))


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fake-users', type=int, default=3,
                        help='the number of fake users ')
    return parser.parse_args()


def main():
    args = _parse_args()
    for user_num in range(args.fake_users):
        run(delay=1)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
    main()
