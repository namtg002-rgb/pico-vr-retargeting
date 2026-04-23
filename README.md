# pico-vr-retargeting

python gear_sonic/scripts/pico_manager_thread_server.py     --vis_smpl     --vis_vr3pt     --waist_tracking     --no_g1 --record_dir ~/workspace_robotics/data/test_dance


python merge_to_pkl.py

python visualize_root_path.py

python inspect_data.py

python prepare_gmr_data.py - 무적


(gmr) namtg002@riro:~/workspace_robotics/GMR$ python scripts/smplx_to_robot.py   --smplx_file ~/workspace_robotics/data/dance_gmr_input_fixed.npz   --robot unitree_g1   --save_path ~/workspace_robotics/data/g1_retargeted_dance.pkl


xrobotoolkit_sdk not found, skip for now. If you do not use XRobotStreamer, it's fine.
