import unittest
import random
from pysinthe import feature, polymer


class TestPolymerMethods(unittest.TestCase):

    def setUp(self):
        promoter = feature.Promoter("promoter1",
                                    5,
                                    15,
                                    ["ecolipol", "rnapol"]
                                    )
        terminator = feature.Terminator("myterm",
                                        50,
                                        55,
                                        {"rnapol": {"efficiency": 1.0},
                                         "ecolipol": {"efficiency": 0.6}
                                         })
        mask = feature.Mask("mask",
                            16,
                            100,
                            ["ecolipol"])

        self.polymer = polymer.Polymer("mygenome",
                                       100,
                                       [promoter, terminator],
                                       mask)

        self.assertTrue(terminator.is_covered())
        self.assertFalse(promoter.is_covered())
        self.assertEqual(self.polymer.uncovered["promoter1"], 1)
        self.assertEqual(self.polymer.uncovered["myterm"], 0)

    def test_bind_polymerase(self):
        random.seed(22)
        pol = feature.Polymerase("ecolipol",
                                 20,
                                 40,
                                 30,
                                 ["ecolipol", "terminator", "rnapol"]
                                 )
        self.polymer.bind_polymerase(pol, "promoter1")
        self.assertEqual(pol.start, 5)
        self.assertEqual(pol.stop, 45)
        self.assertEqual(self.polymer.uncovered["promoter1"], 0)
        self.assertEqual(self.polymer.prop_sum, 30)
