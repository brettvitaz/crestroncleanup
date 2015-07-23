import re
import pprint
from collections import Counter


class ObjStore:
    def __init__(self):
        self.obj_count = Counter()
        self.obj_list = []

    def add_item(self, k):
        obj = ObjType.get_obj(k)
        self.obj_list.append(obj)
        self.obj_count.update([obj.type])

    def items(self):
        for obj in self.obj_list:
            yield obj

    def process(self):
        modified_count = Counter()
        signal_list = set()
        dupes_list = set()

        for obj in self.items():
            if obj.process():
                modified_count.update([obj.type])

            if isinstance(obj, ObjTypeSignal):
                signal_len = len(signal_list)
                signal_list.add(obj['Nm'].lower())
                if signal_len == len(signal_list):
                    dupes_list.add(obj['Nm'])
                    obj['Nm'] += '__DUP'
        
        # modified_count = Counter([_.get('ObjTp') for _ in self.items()])

        print('Types', self.obj_count)
        print('Modified', modified_count)
        print('Stats:')
        for k, v in sorted(self.obj_count.items()):
            print('   {}: {} (Changed: {})'.format(k, v, modified_count[k]))

        if len(dupes_list):
            print('Warning: Duplicate signal names present after processing.')
            pp = pprint.PrettyPrinter()
            pp.pprint('{}'.format(list(dupes_list)))


class ObjType:
    def __init__(self, k):
        self.obj_dict = k

    def __len__(self):
        return len(self.obj_dict)

    def __getitem__(self, item):
        return self.obj_dict[item]

    def __setitem__(self, item, value):
        return self.obj_dict.update({item: value})

    def __delitem__(self, item):
        del (self.obj_dict[item])

    def __iter__(self):
        return iter(self.obj_dict.items())

    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError:
            return default

    @property
    def type(self):
        return str(self.get('ObjTp'))

    def process(self):
        return False

    @classmethod
    def get_type(cls, tp):
        return {
            'Sg': ObjTypeSignal
        }.get(tp, ObjType)

    @classmethod
    def get_obj(cls, k):
        return {
            'Sg': ObjTypeSignal
        }.get(k.get('ObjTp'), ObjType)(k)


class ObjTypeSignal(ObjType):
    def _process(self, str_in):
        str_out = str_in
        # Capitalize letters after a dash or underscore.
        str_out = re.sub(r'(^|[-_\[\(<])([a-z])', lambda _: _.group(1) + _.group(2).upper(), str_out)
        # Capitalize 'fb' if it is not part of another word.
        str_out = re.sub(re.compile(r'(_)(fb)($|[^A-Za-z])', re.IGNORECASE), lambda _: _.group(1) + _.group(2).upper() + _.group(3), str_out)
        # Split numbers from words.
        str_out = re.sub(re.compile(r'([a-z])(\d)', re.IGNORECASE), r'\1_\2', str_out)
        # Pad numbers with a 0.
        # TODO: Identify and correctly pad number sequences over 2 digits when necessary.
        str_out = re.sub(r'(_)(\d)(?![\d-])', lambda _: '{}{:0>2s}'.format(*_.groups()), str_out)

        # Substitute known words with correct formatting.
        str_out = re.sub(re.compile(r'DirecTV', re.IGNORECASE), 'DirecTV', str_out)
        str_out = re.sub(re.compile(r'_TV_', re.IGNORECASE), '_TV_', str_out)
        str_out = re.sub(re.compile(r'_RCVR_', re.IGNORECASE), '_Rcvr_', str_out)
        str_out = re.sub(re.compile(r'HDMI', re.IGNORECASE), 'HDMI', str_out)

        return str_out

    def process(self):
        orig = self['Nm']
        temp = self._process(orig)
        if temp == self._process(temp):
            self['Nm'] = temp
        else:
            raise Exception('Failed to process signal. Process operation is not idempotent. '
                            'Orig:{} New:{} Test:{}'.format(orig, temp, self._process(temp)))
        return orig != temp
