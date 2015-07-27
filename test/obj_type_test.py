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

    def test__setitem__(self):
        for obj in self.TEST_DATA:
            test_obj = ObjType()
            for name, data in obj.items():
                test_obj[name] = data
                self.assertEqual(test_obj[name], data)


if __name__ == '__main__':
    unittest.main()
