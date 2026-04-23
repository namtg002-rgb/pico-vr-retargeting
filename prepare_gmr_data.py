import os
import glob
import numpy as np
from scipy.spatial.transform import Rotation as R

def prepare_data_for_sim():
    # 1. 입력 및 출력 경로 설정
    data_dir = os.path.expanduser('~/workspace_robotics/data/test_dance')
    # 중간 pkl 파일을 거치지 않고 바로 GMR 입력용 npz로 다이렉트 저장!
    out_path = os.path.expanduser('~/workspace_robotics/data/dance_gmr_input_fixed.npz')

    npz_files = sorted(glob.glob(os.path.join(data_dir, 'pose_*.npz')))
    
    if not npz_files:
        print(f"❌ {data_dir} 폴더에 파일이 없습니다.")
        return

    print(f"🔄 총 {len(npz_files)}개의 npz 파일을 읽어 시뮬레이션용으로 즉시 변환합니다...")

    # 2. 데이터 병합 (메모리 상에서 바로 처리)
    keys_to_extract = ['smpl_pose', 'smpl_joints', 'body_quat_w', 'transl']
    sequence_data = {key: [] for key in keys_to_extract}

    for f in npz_files:
        try:
            data = np.load(f, allow_pickle=True)
            for key in keys_to_extract:
                if key in data:
                    sequence_data[key].append(data[key])
        except Exception as e:
            print(f"파일 읽기 에러 ({f}): {e}")

    for key in keys_to_extract:
        if sequence_data[key]:
            sequence_data[key] = np.concatenate(sequence_data[key], axis=0)

    # 3. GMR 포맷으로 변환 및 Key 에러 완벽 패치
    transl = sequence_data['transl']
    quats = sequence_data['body_quat_w'] 
    smpl_pose = sequence_data['smpl_pose'] 
    N = transl.shape[0]

    # ① Root Orientation (3차원)
    scipy_quats = np.column_stack((quats[:, 1], quats[:, 2], quats[:, 3], quats[:, 0]))
    root_orient = R.from_quat(scipy_quats).as_rotvec()

    # ② Body Pose (63차원)
    body_pose = smpl_pose.reshape(N, 63)

    # 🚨 GMR이 정확히 요구하는 Key인 'mocap_frame_rate'로 저장! (30fps 기준)
    target_fps = 30.0 

    np.savez(out_path,
             pose_body=body_pose,       
             root_orient=root_orient,   
             trans=transl,              
             betas=np.zeros(16),        
             gender=np.array('neutral'),
             mocap_frame_rate=np.array(target_fps))

    print(f"\n✅ 파이프라인 통합 변환 완료! (프레임 레이트 패치 포함)")
    print(f"📁 최종 파일 저장 위치: {out_path}")
    print(f"📊 최종 크기 - 프레임 수: {N}, FPS: {target_fps}")

if __name__ == '__main__':
    prepare_data_for_sim()