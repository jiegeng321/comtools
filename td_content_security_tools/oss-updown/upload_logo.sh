#!/bin/bash
cd /data01/xu.fx/comtools/content_security_tools/oss-updown/
source config.sh
#t4 model
python3 updown_model.py --action upload \
                    --bucket ai_vision\
                    --local /data01/xu.fx/my_app/t4_model/20220718_yolov5l_brand784_style1394_T4.trt\
                    --remote ai-brand-logo/1.3/20220718_yolov5l_brand784_style1394_T4.trt
#p40 model
python3 updown_model.py --action upload \
                    --bucket ai_vision\
                    --local /data01/xu.fx/my_app/p40_model/20220718_yolov5l_brand784_style1394_P40.trt\
                    --remote ai-brand-logo/1.3/20220718_yolov5l_brand784_style1394_P40.trt
#config
python3 updown_model.py --action upload \
                    --bucket ai_vision\
                    --local /data01/xu.fx/my_app/ai-brand-logo/model/config.py \
                    --remote ai-brand-logo/1.3/config.py
