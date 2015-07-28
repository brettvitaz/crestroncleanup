import re


class ObjType(object):
    """
    Base type to store unknown types and types without specific processing ability.
    """
    ObjTp = ''
    ObjDesc = ''

    def __init__(self, obj_dict=None):
        if obj_dict is None:
            obj_dict = {}
        self._obj_dict = obj_dict

    def __len__(self):
        return len(self._obj_dict)

    def __getitem__(self, item):
        return self._obj_dict[item]

    def __setitem__(self, item, value):
        self._obj_dict[item] = value

    def __delitem__(self, item):
        del self._obj_dict[item]

    def __iter__(self):
        return iter(self._obj_dict.items())

    def __repr__(self):
        return self.desc

    def __str__(self):
        return repr(self)

    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError:
            return default

    @property
    def id(self):
        return self.get('H') or ''

    @property
    def type(self):
        return self.get('ObjTp') or ''

    @property
    def desc(self):
        return self.ObjDesc or self.type

    @property
    def name(self):
        return self.get('Nm')

    def process(self):
        return False


class ObjTypeVersion(ObjType):
    """
    Version string type.
    I have only ever observed '1' as the version...
    """
    ObjTp = None
    ObjDesc = 'Version'

    @ObjType.id.getter
    def id(self):
        return self.get('Version') or ''

    @ObjType.type.getter
    def type(self):
        return self.ObjDesc


class ObjTypeHeader(ObjType):
    """
    Header contains program data like client name, dealer name, and program name.
    """
    ObjTp = 'Hd'
    ObjDesc = 'Header'

    @property
    def dealer(self):
        """
        Dealer name.
        """
        return self.get('DlrNm')

    @property
    def programmer(self):
        """
        Programmer name.
        """
        return self.get('PgmNm')

    @ObjType.name.getter
    def name(self):
        """
        Client name.
        """
        return self.get('CltNm')


class ObjTypeDatabase(ObjType):
    ObjTp = 'Db'
    ObjDesc = 'Database'

    @ObjType.name.getter
    def name(self):
        """
        SIMPL Database item name.
        """
        return self.get('Mnf') + ' ' + self.get('Mdl')


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
        """
        Process the signal name by reformatting it.
        :return: True if signal has changed.
        :raise Exception:
        """
        orig = self['Nm']
        temp = self._process(orig)
        if temp == self._process(temp):
            self['Nm'] = temp
        else:
            # Raise exception if signal is not idempotent.
            # TODO Create and handle a special exception for this. `ProcessException`
            raise Exception('Failed to process signal. Process operation is not idempotent. '
                            'Orig:{} New:{} Test:{}'.format(orig, temp, self._process(temp)))
        return orig != temp

    @property
    def signal_type(self):
        """
        Signal type: Digital, Analog, or Serial.
        """
        return SgTp.get(self.get('SgTp'))


class ObjTypeFactory(object):
    """
    Creates ObjType subclass objects based on their ObjTp property.
    """
    # Register the all of the ObjType subclasses.
    OBJ_TYPES = {cls.ObjTp: cls for cls in ObjType.__subclasses__()}

    @staticmethod
    def create(obj_data):
        """
        Return an ObjType object from object data.
        :param obj_data: Object data dictionary.
        :return type: ObjType
        """
        return ObjTypeFactory.OBJ_TYPES.get(obj_data.get('ObjTp'), ObjType)(obj_data)
