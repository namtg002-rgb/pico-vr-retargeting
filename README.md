# pico-vr-retargeting

-------------data Collect------------

python gear_sonic/scripts/pico_manager_thread_server.py     --vis_smpl     --vis_vr3pt     --waist_tracking     --no_g1 --record_dir ~/workspace_robotics/data/(폴더명)

--------------GMR-----------

python batch_retarget_recordings.py ~/workspace_robotics/data/(폴더명) --output_dir ~/workspace_robotics/data/(폴더명)/retargeted_GMR --robot unitree_g1 --rate_limit

(결과 확인)

cd ~/workspace_robotics/GMR
conda activate gmr

python scripts/vis_robot_motion_dataset.py   --robot unitree_g1   --robot_motion_folder ~/workspace_robotics/data/(폴더명)/retargeted_GMR

cd ~/workspace_robotics/GMR


conda activate gmr

python scripts/vis_robot_motion_dataset.py   --robot unitree_g1   --robot_motion_folder ~/workspace_robotics/data/(폴더명)/retargeted_GMR

python scripts/vis_robot_motion_dataset.py   --robot unitree_g1   --robot_motion_folder ~/workspace_robotics/data/test0512/retargeted_GMR

[ 와 ] 로 다음 액션 확인 가능


----------Phuma----------

conda activate phuma_bw


cd ~/workspace_robotics


python batch_phuma_retarget_recordings.py ~/workspace_robotics/data/(폴더명)   --output_dir ~/workspace_robotics/data/(폴더명)/retargeted/phuma   --robot_name g1   --foot_contact_threshold 0.02   --device cuda:0



python batch_phuma_retarget_recordings.py ~/workspace_robotics/data/(폴더명)   --output_dir ~/workspace_robotics/data/(폴더명)/retargeted/phuma   --robot_name g1   --foot_contact_threshold 0.02   --device cpu




python view_continuous_g1.py ~/workspace_robotics/data/(폴더명)/retargeted/phuma

[ 와 ] 로 다음 액션 확인 가능
