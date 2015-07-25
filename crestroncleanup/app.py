import collections
import time
import shutil
import sys
import obj_types

NEW_EXT = '.new'
OLD_EXT = '.old'
NEWLINE = '\n'


class App:
    def __init__(self, filename, overwrite, backup):
        self.filename = filename
        self.overwrite = overwrite
        self.backup = backup
        self.new_ext = NEW_EXT if overwrite is False else ''

    def process(self):
        start_time = time.time()

        if self.overwrite and self.backup:
            shutil.copy(self.filename, self.filename + OLD_EXT)

        obj_store = obj_types.ObjStore()
        obj_data = collections.OrderedDict()
        with open(self.filename) as f:
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

        obj_store.process()

        with open(self.filename + self.new_ext, mode='w') as f:
            for obj in obj_store.items():
                obj_lines = ['[{}'.format(NEWLINE)]
                for k, v in obj:
                    obj_lines.append('{}={}{}'.format(k, v, NEWLINE))
                obj_lines.append(']{}'.format(NEWLINE))

                f.writelines(obj_lines)

        end_time = time.time()

        print('Elapsed time: {}'.format(end_time - start_time))
