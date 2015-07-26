import argparse
import time
import app


def main():
    parser = argparse.ArgumentParser(description='Clean up signals in a messy Crestron SIMPL file.')
    parser.add_argument('filename', help='Name of file to process')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite the existing file', default=False)
    parser.add_argument('-b', '--backup', action='store_true', help='Backup existing file before overwriting',
                        default=False)

    args = parser.parse_args()

    filename = args.filename
    overwrite = args.overwrite
    backup = args.backup

    start_time = time.time()

    data = app.read_file(filename)
    data.process()
    app.save_file(data, filename, overwrite, backup)

    end_time = time.time()
    print('Elapsed time: {}'.format(end_time - start_time))
