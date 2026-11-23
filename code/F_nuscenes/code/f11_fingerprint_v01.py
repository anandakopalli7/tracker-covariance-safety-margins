"""Package F (revision v13): provenance fingerprint of the CenterPoint results (STATUS.md, "Detector provenance"). New file,
19 Nov 2026 (Claude Opus 5.5). After Lock 2 only (it reads the val scenes): the nuScenes devkit's own detection evaluation
(DetectionEval, config detection_cvpr_2019) of the folder's val result file; the NDS is compared with the 68.5 that the
CenterPoint maintainer states for the "with flip augmentation" predictions in GitHub issue tianweiy/CenterPoint#249 (and 66.8
without). It changes no F rule and enters no hypothesis. Writes out\\F_DETECTOR_FINGERPRINT_v01.json (and the devkit's own
metrics files in out\\fingerprint_val\\).
Usage: python -I f11_fingerprint_v01.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402

sys.path.insert(0, str(FC.LIB / 'devkit' / 'python-sdk'))
sys.path.append(str(FC.LIB / 'shims_v01'))


def main():
    FC.require_split('val')
    from nuscenes import NuScenes
    from nuscenes.eval.detection.evaluate import DetectionEval
    from nuscenes.eval.common.config import config_factory
    outd = FC.OUT / 'fingerprint_val'
    outd.mkdir(exist_ok=True)
    nusc = NuScenes(version='v1.0-trainval', dataroot=str(FC.DATA), verbose=False)
    ev = DetectionEval(nusc, config=config_factory('detection_cvpr_2019'), result_path=str(FC.RESULT_FILES['val']), eval_set='val',
                       output_dir=str(outd), verbose=False)
    metrics, _ = ev.evaluate()
    md = metrics.serialize()
    doc = dict(code='f11_fingerprint_v01.py', result_file=str(FC.RESULT_FILES['val']), result_sha256=FC.sha256_file(FC.RESULT_FILES['val']),
               nd_score=md['nd_score'], mean_ap=md['mean_ap'], tp_errors=md['tp_errors'],
               reference='GitHub tianweiy/CenterPoint#249, 18 Jan 2022: val NDS 68.5 with flip augmentation, 66.8 without',
               written=FC.clock())
    (FC.OUT / 'F_DETECTOR_FINGERPRINT_v01.json').write_text(FC.jdump(doc), encoding='utf-8')
    print('NDS %.4f mAP %.4f' % (md['nd_score'], md['mean_ap']))


if __name__ == '__main__':
    main()
