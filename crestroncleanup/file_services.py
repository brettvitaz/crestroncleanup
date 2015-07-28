import collections
import shutil
import sys
import platform

from crestroncleanup.obj_store import ObjStore

NEW_EXT = '.new'
OLD_EXT = '.old'
NEWLINE_WIN = '\n'
NEWLINE_NIX = '\r\n'


def read_file(filename):
    """
    Read a file and return a object store, which will contain all of the program objects ready for display or processing.
    :param filename: Full path to the file to process.
    :return: ObjStore object containing all of the objects to be processed.
    """
    obj_store = ObjStore()
    obj_data = collections.OrderedDict()

    # Read and parse the file
    with open(filename) as f:
        for line in f.readlines():
            line_data = line.strip()
            if line_data == '[':
                obj_data = collections.OrderedDict()
            elif line_data == ']':
                obj_store.add_item(obj_data)
            else:
                try:
                    k, v = line_data.split('=', 1)
                except ValueError:
                    print('Failed to parse line: {}'.format(line_data))
                    sys.exit(2)

                obj_data.update({k: v})

    return obj_store


def save_file(obj_store, filename, overwrite=False, backup=True):
    """
    Write an output file from the ObjStore object.
    :param obj_store: ObjStore object containing all of the processed objects.
    :param filename: Full path to the output file.
    :param overwrite: Specify True to overwrite an existing file, False to create a new file with an extension `.new`.
    :param backup: Specify True to backup the existing file if overwriting, creating a copy with the extension `.old`.
    """
    # Windows writes `\n` as `\r\n`, so it is necessary to specify the delimiter here.
    if platform.system() == 'Windows':
        newline = NEWLINE_WIN
    else:
        newline = NEWLINE_NIX

    # Backup the existing file if necessary.
    if overwrite and backup:
        shutil.copy(filename, filename + OLD_EXT)

    new_ext = NEW_EXT if overwrite is False else ''

    # Write the file
    with open(filename + new_ext, mode='w') as f:
        for obj in obj_store.items():
            obj_lines = ['[{}'.format(newline)]
            for k, v in obj:
                obj_lines.append('{}={}{}'.format(k, v, newline))
            obj_lines.append(']{}'.format(newline))

            f.writelines(obj_lines)
