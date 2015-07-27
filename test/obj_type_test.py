import unittest

from crestroncleanup.obj_types import ObjType


class ObjTypeTest(unittest.TestCase):
    TEST_DATA = [
        {
            'ObjTp': 'Sg',
            'H': '4',
            'Nm': 'sys_init',
        },
        {
            'ObjTp': 'Sg',
            'H': '5',
            'Nm': 'sys_init_delay_5s',
        },
        {
            'ObjTp': 'Sg',
            'H': '6',
            'Nm': 'ui-a_sys_init',
        },
    ]

    def test_objType(self):
        for obj in self.TEST_DATA:
            test_obj = ObjType(obj.copy())
            for name, data in obj.items():
                self.assertEqual(data, test_obj[name])

    def test__len__(self):
        self.assertEqual(3, len(ObjType(self.TEST_DATA[0].copy())))

    def test__delitem__(self):
        test_obj = ObjType(self.TEST_DATA[0].copy())
        del test_obj['Nm']

        self.assertEqual(2, len(test_obj))

    def test__setitem__(self):
        for obj in self.TEST_DATA:
            test_obj = ObjType()
            for name, data in obj.items():
                test_obj[name] = data
                self.assertEqual(data, test_obj[name])

    def test_id(self):
        test_obj = ObjType(self.TEST_DATA[0].copy())
        self.assertEqual('4', test_obj.id)

    def test_type(self):
        test_obj = ObjType(self.TEST_DATA[0].copy())
        self.assertEqual('Sg', test_obj.type)

    def test_desc(self):
        test_obj = ObjType(self.TEST_DATA[0].copy())
        self.assertEqual('Sg', test_obj.desc)

    def test_name(self):
        test_obj = ObjType(self.TEST_DATA[0].copy())
        self.assertEqual('sys_init', test_obj.name)

    def test_process(self):
        test_obj = ObjType(self.TEST_DATA[0].copy())
        self.assertFalse(test_obj.process())


if __name__ == '__main__':
    unittest.main()
