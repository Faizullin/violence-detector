from app.modules.violence_detection.task_manager import (
    ViolenceAlarmDetectorWorker, ViolenceBasicDetectorWorker)

violence_basic_detector_worker = ViolenceBasicDetectorWorker()
violence_alarm_detector_worker = ViolenceAlarmDetectorWorker()

__ALL__ = ['violence_basic_detector_worker', 'violence_alarm_detector_worker']
