from collections import Counter

from crestroncleanup.obj_types import ObjTypeFactory, ObjTypeSignal


class ObjStore(object):
    """
    Store and manage all of the target program objects. Objects are stored as a list because they are written back
    in the same order as they are read. If you need a dictionary to present the data, use the `obj_dict` property.
    """
    def __init__(self):
        self.obj_list = []
        self._obj_dict = {}
        self._obj_dict_clean = False

        # Used for statistical output.
        self.obj_count = Counter()
        self.modified_count = Counter()

    @property
    def obj_dict(self):
        """
        Lazily create an object dictionary.
        :return: Dictionary of program objects with object type as the key.
        """
        if not self._obj_dict or not self._obj_dict_clean:
            obj_dict = {}
            for obj in self.obj_list:
                if obj.type not in obj_dict.keys():
                    obj_dict[obj.type] = []
                obj_dict[obj.type].append(obj)
            self._obj_dict, self._obj_dict_clean = obj_dict, True
        return self._obj_dict

    def get_header(self):
        """
        Returns the object containing the program header.
        """
        return self.obj_dict['Hd'][0]

    def get_device_info(self):
        """
        Returns the object containing the control device info.
        """
        return [obj for obj in self.obj_dict['Dv'] if obj['H'] == '2'][0]

    def add_item(self, obj_data):
        """
        Add an object to the list.
        :param obj_data: Dictionary of object data parsed from file.
        """
        self._obj_dict_clean = False
        obj = ObjTypeFactory.create(obj_data)
        self.obj_list.append(obj)
        self.obj_count.update([obj.type])

    def process(self):
        """
        Process all program objects. Signal type is currently the only type to have special processing
        :return: Detailed results as a string.
        """
        self._obj_dict_clean = False
        signal_list = set()
        dupes_list = set()

        # Process all objects. Signal type is currently the only type to have special processing.
        # TODO Pull out individual object processing to own class.
        for obj in self.obj_list:
            if obj.process():
                self.modified_count.update([obj.type])

            if isinstance(obj, ObjTypeSignal):
                signal_len = len(signal_list)
                signal_list.add(obj['Nm'].lower())
                if signal_len == len(signal_list):
                    dupes_list.add(obj['Nm'])
                    obj['Nm'] += '__DUP'

        results_text = 'Stats:\n'
        for k, v in sorted(self.obj_count.items()):
            results_text += '   {}: {} (Changed: {})\n'.format(k, v, self.modified_count[k])

        if len(dupes_list):
            results_text += 'Warning: Duplicate signal names present after processing.\n'
            for dupe in dupes_list:
                results_text += '    {}\n'.format(dupe)

        return results_text
