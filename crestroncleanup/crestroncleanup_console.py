import argparse
import time
import file_services


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

    data = file_services.read_file(filename)
    result_text = data.process()
    file_services.save_file(data, filename, overwrite, backup)

    end_time = time.time()
    print(result_text)
    print('Elapsed time: {}'.format(end_time - start_time))
