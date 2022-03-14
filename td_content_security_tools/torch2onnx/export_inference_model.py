import argparse
import logging
from pathlib import Path
from tqdm import tqdm
import numpy as np
from sklearn.metrics import classification_report
from PIL import Image
import torch
import onnx
import onnxruntime as ort
from preprocess import torch_preprocess, onnx_preprocess
from torchvision import models
# from porn_classification import initialize_model


parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint', type=str, default='')
parser.add_argument('--num_class', type=int, default=5)
parser.add_argument('--legacy', type=bool, default=True)
parser.add_argument('--check', type=bool, default=False)
parser.add_argument('--test_file', type=str,
                    default='five_label/test.lst_filter')
parser.add_argument('--onnx_model', type=str, default='porn.onnx')

args = parser.parse_args()


def print_model_param_name(model):
    for name, param in model.named_parameters():
        print(name)


# load construct model
# model = initialize_model(num_classes=args.num_class, use_pretrained=True)
model = models.resnet50(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = torch.nn.Sequential(
    torch.nn.Linear(num_ftrs, args.num_class),
    torch.nn.Softmax(dim=-1)
)

logging.info('load trained model...')
trained_model = torch.load(args.checkpoint)
new_state_dict = {}
if args.legacy:
    state_dict = trained_model
    for key, val in state_dict.items():
        if key == 'module.fc.weight':
            new_state_dict['fc.0.weight'] = state_dict['module.fc.weight']
        elif key == 'module.fc.bias':
            new_state_dict['fc.0.bias'] = state_dict['module.fc.bias']
        else:
            new_state_dict[key[7:]] = val
else:
    state_dict = trained_model['state_dict']
    for key, val in state_dict.items():
        if key == 'fc.weight':
            new_state_dict['fc.0.weight'] = state_dict['fc.weight']
        elif key == 'fc.bias':
            new_state_dict['fc.0.bias'] = state_dict['fc.bias']
        else:
            new_state_dict[key[6:]] = val

model.load_state_dict(new_state_dict)
model.eval().cuda()

for param in model.parameters():
    param.requires_grad = False

torch.manual_seed(7)
dummy_input = torch.randn(1, 3, 224, 224, device='cuda')
# model.eval()
prob = model(dummy_input).cpu().numpy()

model_name = args.onnx_model
output_names = ['prob']
input_names = ['image']
logging.info("export from pytorch to onnx model.")
torch.onnx.export(model, dummy_input, model_name,
                  output_names=output_names, input_names=input_names, verbose=False,
                  dynamic_axes={'image': {0: 'batch'}, 'prob': {0: 'batch'}},
                  do_constant_folding=True)

onnx.checker.check_model(model_name)
logging.info("onnx check passed.")

np.printoptions(precision=4)
# run in onnxruntime with gpu and cudnn
logging.info('check numerical diff between torch and onnxruntime')
sess_config = ort.SessionOptions()
sess_config.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
sess_config.log_severity_level = 3
sess_config.optimized_model_filepath = 'porn_optimized.onnx'
print(ort.get_available_providers())
sess = ort.InferenceSession(model_name, sess_options=sess_config, )

input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name

prob_onnx = sess.run(None, {input_name: dummy_input.cpu().numpy()})

print('test on random data:')
print(f'torch prob: {prob.squeeze()}')
print(f'onnxruntime prob: {prob_onnx[0].squeeze()}')
print(f'diff between: {prob_onnx[0].squeeze() - prob.squeeze()}')

print("="*20)

if args.check:
    print('test on real image:')
    gt = []
    pred = []
    test_file = 'five_label/test.lst_filter'
    with open(test_file, 'r') as example:
        for line in tqdm(example.readlines()):
            image_name, label = line.split(',')
            image = Image.open(image_name).convert('RGB')
            # preprocessed_image = torch_preprocess(image)
            # prob = model(preprocessed_image.cuda()).squeeze()

            preprocessed_image = onnx_preprocess(image)
            prob_onnx = sess.run(None, {input_name: np.expand_dims(
                preprocessed_image, axis=0).transpose((0, 3, 1, 2))})
            prob_onnx = prob_onnx[0].squeeze()

            # prob_torch = prob.cpu().numpy()

            # print(f'diff between torch and onnx {prob_torch - prob_onnx}')
            # print(np.argmax(prob_onnx), np.argmax(prob_torch))
            predict_label = np.argmax(prob_onnx)
            gt.append(int(label))
            pred.append(int(predict_label))

    print(classification_report(gt, pred, digits=3))
