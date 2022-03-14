#!/bin/bash
cd /data01/xu.fx/comtools/content_security_tools/oss-updown/
source config.sh
python3 updown_model.py --action upload \
                    --bucket ai_vision\
                    --local /data01/xu.fx/my_app/p40_model/20211215_yolov5m_brand440_style710.trt \
                    --remote ai-brand-logo-tm/1.0/20211215_yolov5m_brand440_style710.trt

python3 updown_model.py --action upload \
                    --bucket ai_vision\
                    --local /data01/xu.fx/my_app/ai-brand-logo-tm/model/config.py \
                    --remote ai-brand-logo-tm/1.0/config.py
