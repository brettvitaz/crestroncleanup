import collections
import getopt
import shutil
import sys
import time

from crestroncleanup import obj_types

if __name__ == '__main__':
    start_time = time.time()

    filename = ''
    new_ext = '.new'
    old_ext = '.old'
    newline = '\n'
    overwrite = False
    backup = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:n:', ['overwrite'])
    except getopt.GetoptError:
        print('-i <filename>')
        sys.exit(2)
    else:
        if not len(opts):
            print('-i <filename>')
            sys.exit(2)

    for opt, arg in opts:
        if opt == '-i':
            filename = arg
        elif opt == '-n':
            newline = bytes(arg, 'utf8').decode('unicode-escape')
        elif opt == '--overwrite':
            overwrite = True
            new_ext = ''

    if overwrite and backup:
        shutil.copy(filename, filename + old_ext)

    obj_store = obj_types.ObjStore()
    obj_data = collections.OrderedDict()
    with open(filename) as file:
        for line in file.readlines():
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

    with open(filename + new_ext, mode='w') as file:
        for obj in obj_store.items():
            obj_lines = ['[{}'.format(newline)]
            for k, v in obj:
                obj_lines.append('{}={}{}'.format(k, v, newline))
            obj_lines.append(']{}'.format(newline))

            file.writelines(obj_lines)

    end_time = time.time()

    print('Elapsed time: {}'.format(end_time - start_time))
