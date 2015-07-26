import collections
import shutil
import sys

import obj_types

NEW_EXT = '.new'
OLD_EXT = '.old'
NEWLINE = '\n'


def read_file(filename):
    obj_store = obj_types.ObjStore()
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
    if overwrite and backup:
        shutil.copy(filename, filename + OLD_EXT)

    new_ext = NEW_EXT if overwrite is False else ''

    with open(filename + new_ext, mode='w') as f:
        for obj in obj_store.items():
            obj_lines = ['[{}'.format(NEWLINE)]
            for k, v in obj:
                obj_lines.append('{}={}{}'.format(k, v, NEWLINE))
            obj_lines.append(']{}'.format(NEWLINE))

            f.writelines(obj_lines)
