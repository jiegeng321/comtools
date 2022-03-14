#mode_path="../../test.onnx"
#mode_path="../../face_pts_20210203.onnx"
mode_path="../../face_pts_small_20210220.onnx"
#img_path="/home/admin/data/xfeng/COMDATA/hymenoptera_data/val/ants/Ant-1818.jpg"
#img_path="/home/admin/data/xfeng/COMDATA/face_pts_test_img100"
#img_path="/home/admin/data/xfeng/COMDATA/face_pts_test_img100_with_mask_2nd"
img_path="/home/admin/data/xfeng/COMDATA/face_pts_train_data/face_pts_train_data_torch_final_no_open/val/images"
#img_path="/home/admin/data/xfeng/COMDATA/driver_mask_crop_face/driver_face_crop_face"
#img_path="/home/admin/data/xfeng/COMDATA/driver_mask_crop_face"
#img_path="./driver_mask_crop_face2"
save_path="./test_result"
rm -r $save_path
mkdir $save_path
#img_path="/home/admin/data/xfeng/COMDATA/insurance_angle_train_data/val/0"
for img in $(ls $img_path);
do
    echo $img
    ./img_regression_test $mode_path $img_path/$img $save_path/$img
done

tar cvf test_result.rar $save_path
cp test_result.rar /tmp/fx/
