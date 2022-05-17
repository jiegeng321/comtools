#!/bin/bash
cd /data01/xu.fx/comtools/content_security_tools/oss-updown/
source config.sh
python3 updown_model.py --action upload \
                    --bucket ai_vision\
                    --local /data01/xu.fx/my_app/p40_model/20220513_yolov5_pattern_15bs_22ks_P40.trt \
                    --remote ai-brand-pattern/1.1.1/20220513_yolov5_pattern_15bs_22ks_P40.trt

python3 updown_model.py --action upload \
                    --bucket ai_vision\
                    --local /data01/xu.fx/my_app/t4_model/20220513_yolov5_pattern_15bs_22ks_T4.trt \
                    --remote ai-brand-pattern/1.1.1/20220513_yolov5_pattern_15bs_22ks_T4.trt


python3 updown_model.py --action upload \
                    --bucket ai_vision\
                    --local /data01/xu.fx/my_app/ai-brand-pattern/model/config.py \
                    --remote ai-brand-pattern/1.1.1/config.py
