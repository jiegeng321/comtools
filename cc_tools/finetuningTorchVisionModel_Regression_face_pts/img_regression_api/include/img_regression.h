#ifndef __IMG_CLASSIFIER_H__
#define __IMG_CLASSIFIER_H__

#include "opencv2/core.hpp"

long int img_regression_init(const char * model_path);

int img_regression(long int img_regression_handler, const cv::Mat & image, std::vector<float> & output);

void img_regression_destroy(long int img_regression_handler);

#endif
