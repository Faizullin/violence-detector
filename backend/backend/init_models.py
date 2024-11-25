from apps.violence_detection.violence_detection.utils.image import imdecode
from apps.violence_detection.violence_detection.violence_alarm_detection.detector import \
    ViolenceAlarmDetector
from apps.violence_detection.violence_detection.violence_basic_detection.detector import \
    ViolenceBasicDetector


basic_detector = ViolenceBasicDetector()
basic_detector.load_model_and_prepare()
alarm_detector = ViolenceAlarmDetector()
alarm_detector.load_model_and_prepare()
