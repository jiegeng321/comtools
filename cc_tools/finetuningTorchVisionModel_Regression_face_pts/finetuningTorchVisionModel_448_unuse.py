from __future__ import print_function
from __future__ import division
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
from my_resnet_448 import ResNet
from my_datasets_448 import DatasetImgTxtPair
from my_loss import AdaptiveWingLoss, WingLoss, AWing
from tqdm import tqdm
from torch import Tensor
print("PyTorch Version: ",torch.__version__)
print("Torchvision Version: ",torchvision.__version__)

data_dir = "/home/admin/data/xfeng/COMDATA/face_pts_train_data/face_pts_train_data_torch_myself"
save_model_dir = '/home/admin/data/xfeng/COMMODEL/face_pts_16th_with_init_myself_rot/'
model_name = "my_resnet"  # 从[my_resnet,resnet, alexnet, vgg, squeezenet, densenet, inception]中选择模型
#pretrain_model = "/home/admin/data/xfeng/COMMODEL/face_pts_16th_with_init_norm_comb3_rot/best_acc.pth"
pretrain_model = None
layers = [1,1,1,1,1]
input_size = 448 
num_classes = 44 
batch_size = 128 
num_epochs = 1000
lr = 0.001
lr_sch = [num_epochs//2,int(num_epochs*7/8)]
gamma = 0.1
feature_extract = False

#criterion = nn.CrossEntropyLoss()
#criterion = AdaptiveWingLoss()
#criterion = nn.MSELoss()
criterion = WingLoss()
#criterion = AWing()

initLandmark68 = [ 18.947369, 44.576477, 19.297388, 58.534885, 20.853374,
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
         89.384537, 93.454147, 77.515793, 96.632805, 72.000000, 97.289673, 66.484215, 96.632805 ]
initLandmark22 = initLandmark68[2*17:2*(9+17)+2] + initLandmark68[2*(10+26):2*(21+26)+2]
initLandmark22 = Tensor(initLandmark22)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
initLandmark22 = initLandmark22.to(device)

data_transforms = {
    'train': transforms.Compose([
        #transforms.Grayscale(num_output_channels=1),
        transforms.Resize((input_size,input_size)),
        transforms.RandomApply([transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.2)],p=0.5),
        #transforms.RandomResizedCrop(input_size),
        #transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        #transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
    ]),
    'val': transforms.Compose([
        #transforms.Grayscale(num_output_channels=1),
        transforms.Resize((input_size,input_size)),
        #transforms.CenterCrop(input_size),
        transforms.ToTensor(),
        #transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
    ]),
}
if not os.path.exists(save_model_dir):
    os.makedirs(save_model_dir)

def train_model(model, dataloaders, criterion, optimizer, scheduler, num_epochs=25, is_inception=False):
   since = time.time()

   val_acc_history = []

   best_model_wts = copy.deepcopy(model.state_dict())
   best_acc = 0.0
   best_loss = 1000000
   for epoch in range(num_epochs):
       print('Epoch {}/{}'.format(epoch, num_epochs - 1))
       print('-' * 10)

       # 每个epoch都有一个训练和验证阶段
       for phase in ['train', 'val']:
           if phase == 'train':
               model.train()  # Set model to training mode
           else:
               model.eval()   # Set model to evaluate mode

           running_loss = 0.0
           running_corrects = 0

           # 迭代数据
           for inputs, labels in dataloaders[phase]:
               inputs = inputs.to(device)
               labels = labels.to(device)
               #print(inputs)
               #print(labels)
               # 零参数梯度
               optimizer.zero_grad()

               # 前向
               # 如果只在训练时则跟踪轨迹
               with torch.set_grad_enabled(phase == 'train'):
                   # 获取模型输出并计算损失
                   # 开始的特殊情况，因为在训练中它有一个辅助输出。
                   # 在训练模式下，我们通过将最终输出和辅助输出相加来计算损耗
                   # 但在测试中我们只考虑最终输出。
                   if is_inception and phase == 'train':
                       # From https://discuss.pytorch.org/t/how-to-optimize-inception-model-with-auxiliary-classifiers/7958
                       outputs, aux_outputs = model(inputs)
                       loss1 = criterion(outputs, labels)
                       loss2 = criterion(aux_outputs, labels)
                       loss = loss1 + 0.4*loss2
                   else:
                       outputs = model(inputs)
                       #outputs += (initLandmark22/144.0)
                       outputs += initLandmark22*448/144
                       #outputs /= 144.0
                       loss = criterion(outputs, labels)
                       #print(loss)
                       #print(loss.item())

                   _, preds = torch.max(outputs, 1)
                   _, preds_label = torch.max(labels.data, 1)
                   

                   # backward + optimize only if in training phase
                   if phase == 'train':
                       loss.backward()
                       optimizer.step()

               # 统计
               scheduler.step()            
               running_loss += loss.item() * inputs.size(0)
               running_corrects += torch.sum(preds == preds_label)

           epoch_loss = running_loss / len(dataloaders[phase].dataset)
           epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

           print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

           # deep copy the model
            
           if phase == 'val':
               torch.save(model, save_model_dir+'model_epoch_%d'%epoch+'.pth')
           if (phase == 'val' and epoch_loss < best_loss):#epoch_acc > best_acc
               best_loss = epoch_loss
               best_acc = epoch_acc
               best_model_wts = copy.deepcopy(model.state_dict())
               torch.save(model, save_model_dir+'best_acc.pth')
               print("better model is saved in %s"%(save_model_dir+'best_acc.pth'))
           if phase == 'val':
               val_acc_history.append(epoch_acc)



   time_elapsed = time.time() - since
   print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
   print('Best val Acc: {:4f}'.format(best_acc))

   # load best model weights
   model.load_state_dict(best_model_wts)
   return model, val_acc_history
def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False
def initialize_model(model_name, num_classes, feature_extract, use_pretrained=True, pretrain_model=None):
    # 初始化将在此if语句中设置的这些变量。
    # 每个变量都是模型特定的。
    model_ft = None
    #input_size = 224

    if model_name == "resnet":
        """ Resnet18
 """
        model_ft = models.resnet18(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_ftrs, num_classes),
        nn.Softmax(dim=1)
        )
        #input_size = 384
    elif model_name == "my_resnet":
        model_ft = ResNet(layers,num_classes=num_classes)
        if pretrain_model:
            model_ft = torch.load(pretrain_model)
        
        #input_size = 224

    elif model_name == "alexnet":
        """ Alexnet
 """
        model_ft = models.alexnet(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes)
        #input_size = 224

    elif model_name == "vgg":
        """ VGG11_bn
 """
        model_ft = models.vgg11_bn(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_ftrs,num_classes)
        #input_size = 224

    elif model_name == "squeezenet":
        """ Squeezenet
 """
        model_ft = models.squeezenet1_0(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        model_ft.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=(1,1), stride=(1,1))
        model_ft.num_classes = num_classes
        #input_size = 224

    elif model_name == "densenet":
        """ Densenet
 """
        model_ft = models.densenet121(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.classifier.in_features
        model_ft.classifier = nn.Linear(num_ftrs, num_classes)
        #input_size = 224

    elif model_name == "inception":
        """ Inception v3
 Be careful, expects (299,299) sized images and has auxiliary output
 """
        model_ft = models.inception_v3(pretrained=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        # 处理辅助网络
        num_ftrs = model_ft.AuxLogits.fc.in_features
        model_ft.AuxLogits.fc = nn.Linear(num_ftrs, num_classes)
        # 处理主要网络
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs,num_classes)
        #input_size = 299

    else:
        print("Invalid model name, exiting...")
        exit()

    return model_ft

# 在这步中初始化模型
model_ft = initialize_model(model_name, num_classes, feature_extract, use_pretrained=True, pretrain_model=pretrain_model)

# 打印我们刚刚实例化的模型
print(model_ft)



print("Initializing Datasets and Dataloaders...")

# 创建训练和验证数据集
image_datasets = {x: DatasetImgTxtPair(data_dir, train_val=x, transform=data_transforms[x]) for x in ['train', 'val']}
# 创建训练和验证数据加载器
dataloaders_dict = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=1) for x in ['train', 'val']}


# 将模型发送到GPU
model_ft = model_ft.to(device)

# 在此运行中收集要优化/更新的参数。
# 如果我们正在进行微调，我们将更新所有参数。
# 但如果我们正在进行特征提取方法，我们只会更新刚刚初始化的参数，即`requires_grad`的参数为True。
params_to_update = model_ft.parameters()
print("Params to learn:")
if feature_extract:
    params_to_update = []
    for name,param in model_ft.named_parameters():
        if param.requires_grad == True:
            params_to_update.append(param)
            print("\t",name)
else:
    for name,param in model_ft.named_parameters():
        if param.requires_grad == True:
            print("\t",name)
optimizer_ft = optim.Adam(params_to_update, lr=lr)
scheduler = lr_scheduler.MultiStepLR(optimizer_ft, milestones=lr_sch, gamma=gamma)
#criterion = nn.CrossEntropyLoss()
#criterion = AdaptiveWingLoss()
#criterion = nn.MSELoss()
#criterion = WingLoss()
model_ft, hist = train_model(model_ft, dataloaders_dict, criterion, optimizer_ft, scheduler, num_epochs=num_epochs, is_inception=(model_name=="inception"))

