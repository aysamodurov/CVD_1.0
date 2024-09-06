import datetime
import logging
from reader import Detectors


logging.basicConfig(level=logging.INFO)
FILE_NAME = './10%/KC_RU_TK070423/QED.rsa'
DETECTOR_KKS = '20JKS22FX030XQ03'


if __name__=='__main__':
    detector = Detectors()
    detector.load_rsa_file(FILE_NAME)
    print(f"Обработано {detector.count_detector}, количество точек {detector.count_values}")
    indication = detector.get_indication(DETECTOR_KKS)
    print(f"{indication}, type {type(indication)}")
