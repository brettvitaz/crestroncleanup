import re
import pprint
from collections import Counter


class ObjStore(object):
    def __init__(self):
        self.obj_count = Counter()
        self.obj_list = []

    @property
    def obj_dict(self):
        obj_dict = {}
        for obj in self.obj_list:
            if obj.type not in obj_dict.keys():
                obj_dict[obj.type] = []
            obj_dict[obj.type].append(obj)
        return obj_dict

    def get_header(self):
        return self.obj_dict['Hd']

    def get_device_info(self):
        return next([obj for obj in self.obj_dict['Dv'] if obj['H'] == '2'])

    def add_item(self, k):
        obj = ObjTypeFactory.create(k)
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

        print('Types', self.obj_count)
        print('Modified', modified_count)
        print('Stats:')
        for k, v in sorted(self.obj_count.items()):
            print('   {}: {} (Changed: {})'.format(k, v, modified_count[k]))

        if len(dupes_list):
            print('Warning: Duplicate signal names present after processing.')
            pp = pprint.PrettyPrinter()
            pp.pprint('{}'.format(list(dupes_list)))


class ObjType(object):
    ObjTp = None
    ObjDesc = None

    def __init__(self, k=None):
        if k is None:
            k = {}
        self.obj_dict = k

    def __len__(self):
        return len(self.obj_dict)

    def __getitem__(self, item):
        return self.obj_dict[item]

    def __setitem__(self, item, value):
        self.obj_dict[item] = value

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

    @property
    def desc(self):
        return self.ObjDesc or self.type

    def process(self):
        return False

    def __repr__(self):
        return self.desc

    def __str__(self):
        return repr(self)

    @property
    def name(self):
        return self.get('Nm')


class ObjTypeHeader(ObjType):
    ObjTp = 'Hd'
    ObjDesc = 'Header'

    @property
    def dealer(self):
        return self['DlrNm']

    @property
    def programmer(self):
        return self['PgmNm']

    @property
    def controller_name(self):
        return self['CltNm']


class ObjTypeDevice(ObjType):
    ObjTp = 'Dv'
    ObjDesc = 'Device'


class ObjTypeSymbol(ObjType):
    ObjTp = 'Sm'
    ObjDesc = 'Symbol'


SgTp = {
    None: 'Digital',
    '2': 'Analog',
    '4': 'String',
}

DO_NOT_PROCESS_SIGNAL = ['//__digital_reserved__', '//__analog_reserved__', '//__serial_reserved__']


class ObjTypeSignal(ObjType):
    ObjTp = 'Sg'
    ObjDesc = 'Signal'

    def _process(self, str_in):
        if str_in in DO_NOT_PROCESS_SIGNAL:
            return str_in

        str_out = str_in
        # Capitalize letters after a dash or underscore.
        str_out = re.sub(r'(^|[-_\[\(<])([a-z])', lambda _: _.group(1) + _.group(2).upper(), str_out)
        # Capitalize 'fb' if it is not part of another word.
        str_out = re.sub(re.compile(r'(_)(fb)($|[^A-Za-z])', re.IGNORECASE),
                         lambda _: _.group(1) + _.group(2).upper() + _.group(3), str_out)
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

    @property
    def signal_type(self):
        return SgTp.get(self.get('SgTp'))

    @ObjType.desc.getter
    def desc(self):
        desc = '%s: %s - %s' % (super(ObjTypeSignal, self).desc, self.name, self.signal_type)
        return desc


class ObjTypeFactory(object):
    OBJ_TYPES = {cls.ObjTp: cls for cls in ObjType.__subclasses__()}

    @staticmethod
    def create(k):
        return ObjTypeFactory.OBJ_TYPES.get(k.get('ObjTp'), ObjType)(k)
