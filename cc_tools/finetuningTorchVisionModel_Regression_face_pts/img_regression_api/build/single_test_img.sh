mode_path="../../face_pts_baseline_210126.onnx"
#mode_path="/home/admin/data/xfeng/finetuningTorchVisionModel_idcard_f_b/idcard_f_b.onnx"
#img_path="/home/admin/data/xfeng/COMDATA/hymenoptera_data/val/ants/Ant-1818.jpg"
img_path="/home/admin/data/xfeng/COMDATA/driver_gen_test_img100_w/4.jpg"
img_path_save="result.jpg"

./img_regression_test $mode_path $img_path $img_path_save
