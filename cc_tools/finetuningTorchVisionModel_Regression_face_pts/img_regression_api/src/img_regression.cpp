#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/dnn.hpp"

#include "img_regression.h"

struct regressionWrapper{
    cv::dnn::Net img_regression;
};
static float initLandmark68[136] = { 18.947369, 44.576477, 19.297388, 58.534885, 20.853374,
         72.432930, 23.765581, 86.102028, 29.172928, 98.812378, 37.540443, 109.831223, 47.837433,
         119.026711, 59.167023, 126.469444, 72.000000, 128.660843, 84.832977, 126.469444, 96.162567,
         119.026711, 106.459557, 109.831223, 114.827057, 98.812378, 120.234413, 86.102028, 123.146614,
         72.432930, 124.702614, 58.534885, 125.052620, 44.576485, 28.809628, 34.215424, 35.450314, 28.208271,
         44.826038, 26.445757, 54.493114, 27.855995, 63.541664, 31.644030, 80.458336, 31.644030, 89.506889,
         27.855995, 99.173973, 26.445757, 108.549675, 28.208271, 115.190376, 34.215424, 72.000000, 42.634579,
         72.000000, 51.725540, 72.000000, 60.748806, 72.000000, 70.051857, 61.326126, 76.187454, 66.464874,
         78.051048, 72.000000, 79.703957, 77.535103, 78.051048, 82.673882, 76.187454, 39.606556, 43.702717,
         45.309280, 40.343479, 52.219509, 40.449978, 58.233978, 45.110622, 51.741467, 46.324669, 44.871082,
         46.219921, 85.766022, 45.110622, 91.780495, 40.449978, 98.690704, 40.343479, 104.393456, 43.702717,
         99.128922, 46.219921, 92.258530, 46.324669, 51.426418, 93.035606, 59.004028, 90.055481, 66.665260,
         88.396675, 72.000000, 89.773117, 77.334747, 88.396675, 84.995956, 90.055481, 92.573578, 93.035606,
         85.229919, 100.316994, 77.807640, 103.499031, 72.000000, 104.112617, 66.192360, 103.499031, 58.770092,
         100.316994, 54.615459, 93.454147, 66.584976, 92.945946, 72.000000, 93.535690, 77.415024, 92.945946,
         89.384537, 93.454147, 77.515793, 96.632805, 72.000000, 97.289673, 66.484215, 96.632805 };
long int img_regression_init(const char* mode_path){
    if(!mode_path){
        return -1;
    }
    regressionWrapper * img_regression_ptr = new regressionWrapper();
    img_regression_ptr->img_regression = cv::dnn::readNet(mode_path);
    if (img_regression_ptr->img_regression.empty()){
        delete img_regression_ptr;
        return -2;
    }
    //img_regression_ptr->img_regression.setPreferableBackend(cv::dnn::DNN_BACKEND_INFERENCE_ENGINE);
    //img_regression_ptr->img_regression.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);
    return reinterpret_cast<long int>(img_regression_ptr);
}

void img_regression_destroy(long int img_regression_handler){
    if (-1 == img_regression_handler or -2 == img_regression_handler)
        return;
    regressionWrapper * img_regression_ptr = reinterpret_cast<regressionWrapper *>(img_regression_handler);
    delete img_regression_ptr;
}

int img_regression(long img_regression_handler, const cv::Mat & img, std::vector<float> & output){
    if (-1 == img_regression_handler or -2 == img_regression_handler){
        std::cout << "init fail: " << std::endl;   
        return -1;
}
    regressionWrapper * img_regression_ptr = reinterpret_cast<regressionWrapper *>(img_regression_handler);
    int wd = img.cols;
    int ht = img.rows;
    int left;
    int top;
    //if(wd>ht){
    //left = (int)(wd*0.2);
    //top = (int)(ht*0.1);
    //}else{
    //left = (int)(wd*0.1);
    //top = (int)(ht*0.2);
    //}
    //int right = wd - left;
    //int bot = ht - top;
    //cv::Mat img_rec(img, cv::Rect(left, top, right, bot));
    cv::Mat img_cvt;
    //cv::cvtColor(img,img_cvt,cv::COLOR_BGR2GRAY);//CV_BGR2GRAY
    cv::cvtColor(img,img_cvt,cv::COLOR_BGR2RGB);//CV_BGR2GRAY
    cv::Mat blob_img;
    cv::dnn::blobFromImage(img_cvt, blob_img, 1.0/127.5, cv::Size(144, 144), cv::Scalar(127.5,127.5,127.5), false, false);
    //cv::setNumThreads(1);
    img_regression_ptr->img_regression.setInput(blob_img);
    cv::Mat out = img_regression_ptr->img_regression.forward();
    output = out.row(0);
    for(int i = 0; i < 10; i++)
    {
        //output[2*i] *= 144.0;
        output[2*i] += initLandmark68[2*(i+17)];
        output[2*i] *= (float)wd/144.0;
        output[2*i] = (int)(output[2*i] + 0.5);
        
        //output[2*i+1] *= 144.0;
        output[2*i+1] += initLandmark68[2*(i+17)+1];
        output[2*i+1] *= (float)ht/144.0;
        output[2*i+1] = (int)(output[2*i+1] + 0.5);
    }
    for(int i = 10; i < 22; i++)
    {   
        //output[2*i] *= 144.0;
        output[2*i] += initLandmark68[2*(i+26)];
        output[2*i] *= (float)wd/144.0;
        output[2*i] = (int)(output[2*i] + 0.5);
        
        //output[2*i+1] *= 144.0;
        output[2*i+1] += initLandmark68[2*(i+26)+1];
        output[2*i+1] *= (float)ht/144.0;
        output[2*i+1] = (int)(output[2*i+1] + 0.5);
    }
    //cv::setNumThreads(-1);
    //std::cout << "optput: " << out.row(0) << std::endl;
    //cv::Point p;
    //double score;   
    //cv::minMaxLoc(out.row(0),0,&score,0,&p);
#ifdef DEBUG
    //std::cout << "in size: " << blob_img.size << std::endl;
    //std::cout << "out size: " << out.size << std::endl;
    //std::cout << "out: " << out << std::endl;
    //std::cout << "max score: " << score << std::endl;
    //std::cout << "max label: " << p.x << std::endl;
#endif
    //cv::Mat rotate;
    //int rotate_flag;
    //if(2 == p.x){
    //    rotate_flag = cv::ROTATE_90_CLOCKWISE;}
    //else if(3 == p.x){
    //    rotate_flag = cv::ROTATE_180;}
    //else if(1 == p.x){
    //    rotate_flag = cv::ROTATE_90_COUNTERCLOCKWISE;}
    //else{
    //    return img;}
    //cv::rotate(img, rotate, rotate_flag);
    return 1;

    

}
