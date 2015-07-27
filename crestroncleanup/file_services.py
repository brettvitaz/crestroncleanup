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
    obj_store = ObjStore()
    obj_data = collections.OrderedDict()
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
    if platform.system() == 'Windows':
        newline = NEWLINE_WIN
    else:
        newline = NEWLINE_NIX

    if overwrite and backup:
        shutil.copy(filename, filename + OLD_EXT)

    new_ext = NEW_EXT if overwrite is False else ''

    with open(filename + new_ext, mode='w') as f:
        for obj in obj_store.items():
            obj_lines = ['[{}'.format(newline)]
            for k, v in obj:
                obj_lines.append('{}={}{}'.format(k, v, newline))
            obj_lines.append(']{}'.format(newline))

            f.writelines(obj_lines)
