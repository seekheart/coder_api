"""
Main app entry point
Mike Tung
"""

from coder_engine.coder_engine import CoderEngine


def main():
    data_engine = CoderEngine('localhost', 27017, 'coder', 'users')


if __name__ == '__main__':
    main()
