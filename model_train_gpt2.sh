#!/bin/bash
#---------------------------------------
CEND="\e[0m"
CGREEN="\e[1;32m"
#---------------------------------------


DT=$(date +"%Y_%m_%d_%I_%M_%p")
DATASET_FILE="dataset.txt"
SRC_MODEL="gpt2_small_for_train"
PROJECT_NAME="finetune"
SAVE_STEPS=500
BATCH_SIZE=1
GAS=1
WEIGHT_DECAY="0.03"
SIZE="$(du $DATASET_FILE | awk '{print $1/1000}')MB"
LR="0.00006"
OPTIMIZER="adamw_bnb_8bit"
CACHE_DIR=".train_cache"
LOGS_DIR="runs"

RUN_NAME="$PROJECT_NAME-bs$BATCH_SIZE-gas$GAS-drop$DROPOUT-$OPTIMIZER-lr$LR-$SIZE-$DT"

echo -e "$CGREEN$RUN_NAME$CEND"

./_run_clm.py \
    --model_name_or_path $SRC_MODEL \
    --train_file $DATASET_FILE \
    --per_device_train_batch_size $BATCH_SIZE \
    --dataset_config_name plain_text \
    --num_train_epochs 1 \
    --save_total_limit 2 \
    --save_steps $SAVE_STEPS \
    --optim $OPTIMIZER \
    --do_train \
    --block_size 2048 \
    --cache_dir $CACHE_DIR \
    --output_dir $PROJECT_NAME \
    --logging_first_step \
    --logging_steps 2 \
    --logging_dir $LOGS_DIR \
    --include_inputs_for_metrics \
    --no_skip_memory_metrics \
    --report_to tensorboard \
    --weight_decay $WEIGHT_DECAY \
    --lr_scheduler_type constant \
    --learning_rate $LR \
    --save_safetensors \
    --torch_dtype float32 \
    --warmup_ratio 0.03 \
    --gradient_checkpointing True \
    --gradient_accumulation_steps $GAS \
#    --log_level debug \
#  --fp16 \

