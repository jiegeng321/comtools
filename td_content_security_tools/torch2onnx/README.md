### 功能
1. export model from pytorch to onnx
2. merge softmax op to onnx model
3. preprocess improvement
4. check accuracy consistency between torch and onnxruntime

### 依赖
1. onnxruntime
```
pip install onnxruntime==1.1.0
```

### 使用说明
copy terror_classification initialize_model
```
python export_inference_model.py --help
```
