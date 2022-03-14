cmake_minimum_required(VERSION 3.0)

project(img_regression)
set(CMAKE_BUILD_TYPE "Relase")
# 添加c++ 11标准支持
#TIMETESTset(CMAKE_CXX_FLAGS "-std=c++11 -O3 -DDEBUG")
#set(CMAKE_CXX_FLAGS "-std=c++11 -O3 -DRELASE")
set(CMAKE_CXX_FLAGS "-std=c++11 -O3 -DRELASE")
#SET(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")
#find_package(OpenCV REQUIRED)

#include_directories("/home/admin/data/xfeng/COMLIB/opencv4.3.0-openvino/include/opencv4/")
include_directories("/home/admin/data/xfeng/COMLIB/opencv4.3.0/include/opencv4/")
include_directories("${PROJECT_SOURCE_DIR}/include/")
#message(${PROJECT_SOURCE_DIR})
#LINK_DIRECTORIES("/home/admin/data/xfeng/COMLIB/opencv4.3.0-openvino/lib64/")
LINK_DIRECTORIES("/home/admin/data/xfeng/COMLIB/opencv4.3.0/lib64/")
set(OpenCV_LIBS "-lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_dnn -lopencv_calib3d -lopencv_imgcodecs -lopencv_flann -lopencv_features2d")

add_library(img_regression SHARED "./src/img_regression.cpp")
target_link_libraries(img_regression ${OpenCV_LIBS} )
add_executable(img_regression_test main_img_regression.cpp)
target_link_libraries(img_regression_test ${OpenCV_LIBS} img_regression)


#add_library(ocr_recog SHARED "./src/ocr_recog.cpp")
#target_link_libraries(ocr_recog ${OpenCV_LIBS} )
#add_executable(ocr_recog_test main_ocr_recog.cpp)
#target_link_libraries(ocr_recog_test ${OpenCV_LIBS} ocr_recog)

#add_library(angle SHARED "./src/angle.cpp")
#target_link_libraries(angle ${OpenCV_LIBS} )
#add_executable(ocr_angle_test main_angle.cpp)
#target_link_libraries(ocr_angle_test ${OpenCV_LIBS} angle)

#add_library(ocr_detect_recog SHARED "./src/ocr_detect_recog.cpp")
#target_link_libraries(ocr_detect_recog ${OpenCV_LIBS} ocr_detect ocr_recog)
#add_executable(ocr_detect_recog_test main_ocr_detect_recog.cpp)
#target_link_libraries(ocr_detect_recog_test ${OpenCV_LIBS} ocr_detect_recog ocr_detect ocr_recog)
