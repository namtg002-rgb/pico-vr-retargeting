# pico-vr-retargeting

-------------data Collect------------



python gear_sonic/scripts/pico_manager_thread_server.py     --vis_smpl     --vis_vr3pt     --waist_tracking     --no_g1 --record_dir ~/workspace_robotics/data/(폴더명)



--------------GMR-----------

python batch_retarget_recordings.py ~/workspace_robotics/data/(폴더명) --output_dir ~/workspace_robotics/data/(폴더명)/retargeted_GMR --robot unitree_g1 --rate_limit

conda activate gmr
cd ~/workspace_robotics

python batch_retarget_recordings.py   ~/workspace_robotics/data/(폴더명)   --output_dir ~/workspace_robotics/data/(폴더명)/retargeted_GMR   --robot unitree_g1   --fps 30   --offset_to_ground   --overwrite


(결과 확인)

cd ~/workspace_robotics/GMR
conda activate gmr

python scripts/vis_robot_motion_dataset.py   --robot unitree_g1   --robot_motion_folder ~/workspace_robotics/data/(폴더명)/retargeted_GMR

cd ~/workspace_robotics/GMR


[ 와 ] 로 다음 액션 확인 가능


----------Phuma----------

conda activate phuma_bw


cd ~/workspace_robotics


python batch_phuma_retarget_recordings.py ~/workspace_robotics/data/(폴더명)   --output_dir ~/workspace_robotics/data/(폴더명)/retargeted/phuma   --robot_name g1   --foot_contact_threshold 0.02   --device cuda:0



python batch_phuma_retarget_recordings.py ~/workspace_robotics/data/(폴더명)   --output_dir ~/workspace_robotics/data/(폴더명)/retargeted/phuma   --robot_name g1   --foot_contact_threshold 0.02   --device cpu




python view_continuous_g1.py ~/workspace_robotics/data/(폴더명)/retargeted/phuma



[ 와 ] 로 다음 액션 확인 가능







------------------이후 deepmimic-------- mimickit으로 진행

1. GMR 결과를 MimicKit motion 포맷으로 변환


conda activate mimickit_lab
cd ~/workspace_robotics/MimicKit

mkdir -p data/motions/g1

i=0
for f in $(ls -v ~/workspace_robotics/data/(폴더명)/retargeted_GMR/*.pkl); do
  printf -v idx "%03d" "$i"
  python tools/gmr_to_mimickit/gmr_to_mimickit.py \
    --input_file "$f" \
    --output_file "data/motions/g1/g1_vertical_jump_${idx}.pkl" \
    --loop clamp \
    --output_fps 30
  i=$((i+1))
done


2. MimicKit dataset 파일 확인



cd ~/workspace_robotics/MimicKit

cat data/datasets/dataset_g1_vertical_jump_oneclip.yaml
cat data/datasets/dataset_g1_vertical_jump.yaml




3. Isaac Lab에서 reference motion 먼저 보기 


conda activate mimickit_lab
cd ~/workspace_robotics/MimicKit

OMNI_KIT_ACCEPT_EULA=YES python mimickit/run.py \
  --arg_file args/view_motion_g1_vertical_jump_lab_args.txt \
  --visualize true



4. 1clip 학습 시작


conda activate mimickit_lab
cd ~/workspace_robotics/MimicKit

OMNI_KIT_ACCEPT_EULA=YES python mimickit/run.py \
  --arg_file args/deepmimic_g1_vertical_jump_oneclip_lab_args.txt \
  --visualize false \
  --num_envs 4096 \
  --out_dir output/g1_vertical_jump_oneclip



5. TensorBoard 확인


conda activate mimickit_lab
cd ~/workspace_robotics/MimicKit

tensorboard \
  --logdir output/g1_vertical_jump_oneclip \
  --port 6006 \
  --bind_all


6. 학습 중 최신 모델 viewer로 확인


conda activate mimickit_lab
cd ~/workspace_robotics/MimicKit

LATEST=$(ls -v output/g1_vertical_jump_oneclip/int_models/model_*.pt | tail -n 1)

echo "Viewing: $LATEST"

OMNI_KIT_ACCEPT_EULA=YES python mimickit/run.py \
  --arg_file args/deepmimic_g1_vertical_jump_oneclip_lab_args.txt \
  --mode test \
  --visualize true \onda activate mimickit_lab
cd ~/workspace_robotics/MimicKit

OMNI_KIT_ACCEPT_EULA=YES python mimickit/run.py \
  --arg_file args/deepmimic_g1_vertical_jump_lab_args.txt \
  --env_config data/envs/deepmimic_g1_vertical_jump_pose05_env.yaml \
  --model_file output/g1_vertical_jump_9clip_baseline_16384/model.pt \
  --visualize false \
  --num_envs 16384 \
  --out_dir output/g1_vertical_jump_9clip_pose05_finetune


  --num_envs 1 \
  --test_episodes 999999 \
  --model_file "$LATEST" \
  --out_dir output/g1_vertical_jump_oneclip_viewer





7. 1clip이 충분히 학습되면 최종 9clip로 넘어가기



conda activate mimickit_lab
cd ~/workspace_robotics/MimicKit

OMNI_KIT_ACCEPT_EULA=YES python mimickit/run.py \
  --arg_file args/deepmimic_g1_vertical_jump_lab_args.txt \
  --visualize false \
  --num_envs 8192 \
  --out_dir output/g1_vertical_jump_9clip




-----deepmimic 확인용 -------------- 제일 최신거


conda activate mimickit_lab
cd ~/workspace_robotics/MimicKit

LATEST=$(ls -v output/g1_vertical_jump_oneclip/int_models/model_*.pt | tail -n 1)

echo "Viewing: $LATEST"

OMNI_KIT_ACCEPT_EULA=YES python mimickit/run.py \
  --arg_file args/deepmimic_g1_vertical_jump_oneclip_lab_args.txt \
  --mode test \
  --visualize true \
  --num_envs 1 \
  --test_episodes 999999 \
  --model_file "$LATEST" \
  --out_dir output/g1_vertical_jump_oneclip_viewer




