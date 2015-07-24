import argparse
from app import App


def main():
    parser = argparse.ArgumentParser(description='Clean up signals in a messy Crestron SIMPL file.')
    parser.add_argument('filename', help='Name of file to process')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite the existing file', default=False)
    parser.add_argument('-b', '--backup', action='store_true', help='Backup existing file before writing', default=False)

    args = parser.parse_args()

    filename = args.filename
    overwrite = args.overwrite
    backup = args.backup

    print(filename, overwrite, backup)

    app = App(filename, overwrite, backup)
    app.process()
