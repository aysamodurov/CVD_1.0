import unittest
from datetime import datetime
from reader import Detectors

FILE_NAME = './10%/KC_RU_TK070423/QED.rsa'
DETECTOR_KKS = '20JKS22FX030XQ03'
START_DATE = datetime.fromisoformat('2023-04-07 10:00:00')
FINISH_DATE = datetime.fromisoformat('2023-04-07 10:00:20')

class TestReader(unittest.TestCase):
    detectors = Detectors()
    detectors.load_rsa_file(FILE_NAME)

    def test_de(self):
        self.assertEqual(self.detectors.count_values,900)
        self.assertEqual(self.detectors.count_detector, 378)
        self.assertEqual(len(self.detectors.get_indication(DETECTOR_KKS,START_DATE)),60)
        self.assertEqual(len(self.detectors.get_indication(DETECTOR_KKS,finish_time=FINISH_DATE)),861)
        self.assertEqual(len(self.detectors.get_indication(DETECTOR_KKS,START_DATE,FINISH_DATE)),21)


if __name__ == '__main__':
    unittest.main()