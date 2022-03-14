#include <iostream>
#include <chrono>
#include <string>
#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/dnn.hpp>

#include "img_regression.h"

using namespace std;
using namespace cv;


int main(int argc, char ** argv){
    
    char * img_regression_model_name = argv[1];
    char * img_name = argv[2];
    char * save_name = argv[3];
    
    
    
    long int img_regression_handler = img_regression_init(img_regression_model_name);
    if(-1 == img_regression_handler || -2==img_regression_handler){
        cout << "detector init failed! " << img_regression_model_name << img_regression_handler << endl;
        return -1;
    }else{
        //cout << "detector init successed! " << img_regression_model_name <<endl;
    }
    
    Mat image = imread(img_name);
    if(image.empty()){
        cout << "load image failed! " << img_name << endl;
        return -1;
    }
    int regression_result;
    vector<float> output;
    //for (int i=0;i<4000;i++) {
    //chrono::steady_clock::time_point t1 = chrono::steady_clock::now();
    regression_result = img_regression(img_regression_handler, image,output);
    //chrono::steady_clock::time_point t2 = chrono::steady_clock::now();
    //chrono::duration<double> time_costed = chrono::duration_cast<chrono::duration<double>>(t2-t1);
    //cout << "one detect recog time: " << time_costed.count() << " seconds" <<endl;   
    //}
    //std::cout << "result: " << regression_result << endl;
    for (int i = 0; i < 22; i++)
    {
        Point pt;
        pt.x = output[2*i];
        pt.y = output[2*i+1];
       circle(image, pt, 2, CV_RGB(255, 0, 0), 2);
    }
    imwrite(save_name, image);
    img_regression_destroy(img_regression_handler);
    return 0;  
}
