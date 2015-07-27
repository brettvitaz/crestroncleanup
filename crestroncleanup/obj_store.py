from collections import Counter

from crestroncleanup.obj_types import ObjTypeFactory, ObjTypeSignal


class ObjStore(object):
    def __init__(self):
        self.obj_count = Counter()
        self.obj_list = []
        self._obj_dict = {}
        self._obj_dict_clean = False
        self.modified_count = Counter()

    @property
    def obj_dict(self):
        if not self._obj_dict or not self._obj_dict_clean:
            obj_dict = {}
            for obj in self.obj_list:
                if obj.type not in obj_dict.keys():
                    obj_dict[obj.type] = []
                obj_dict[obj.type].append(obj)
            self._obj_dict, self._obj_dict_clean = obj_dict, True
        return self._obj_dict

    def get_header(self):
        return self.obj_dict['Hd'][0]

    def get_device_info(self):
        return [obj for obj in self.obj_dict['Dv'] if obj['H'] == '2'][0]

    def add_item(self, k):
        self._obj_dict_clean = False
        obj = ObjTypeFactory.create(k)
        self.obj_list.append(obj)
        self.obj_count.update([obj.type])

    def items(self):
        for obj in self.obj_list:
            yield obj

    def process(self):
        self._obj_dict_clean = False
        signal_list = set()
        dupes_list = set()

        for obj in self.items():
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
