import os
import json
# import torch.nn as nn
import torch
from PIL import Image
from torchvision import transforms
# import matplotlib.pyplot as plt
import numpy as np
import requests
import datetime
from response import make_err_response, make_succ_response
from weplant_model import resnext101_32x8d as resnext_best
# from weplant_model import squeezenet1_0 as resnext_best

def main(url):
    r = requests.get(url)
    img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)) , 'static','uploads', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S_") + "girl.jpg")
    # #打开文件夹并写入图片
    with open(img_path,'wb+') as f:
        f.write(r.content)
        device = torch.device("cuda:1" if torch.cuda.is_available() else"cpu")
        # "cuda:0" if torch.cuda.is_available() else
        data_transform = transforms.Compose(
            [transforms.Resize(224),
            #  transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

        # # load image
        # img_file = open(img_path, "rb")
        # print(img_file)
        img = Image.open(f)
        # # plt.imshow(img)
        # # [N, C, H, W]
        img = data_transform(img)
        # # expand batch dimension
        img = torch.unsqueeze(img, dim=0)

        # # read class_indict
        json_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), './class_indices.json')
        assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

        json_file = open(json_path, "r")
        class_indict = json.load(json_file)

        # create model
        model = resnext_best()
        # model.classifier[1] = nn.Conv2d(512, 8, kernel_size=(1, 1), stride=(1, 1))
        # in_channel = model.fc.in_features
        # model.fc = nn.Linear(in_channel, 8)
        model.to(device)

        # load model weights
        weights_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./_best.pth")
        assert os.path.exists(weights_path), "file: '{}' dose not exist.".format(weights_path)
        # model.load_state_dict(torch.load(weights_path, map_location=device))
        model.load_state_dict(torch.load(weights_path, map_location=device))

        # prediction
        model.eval()
        with torch.no_grad():
            # predict class
            output = torch.squeeze(model(img.to(device))).cpu()
            predict = torch.softmax(output, dim=0)
            # predict_cla = torch.argmax(predict).numpy()

        # print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_cla)],
        #                                              predict[predict_cla].numpy())
        # plt.title(print_res)
        # for i in range(len(predict)):
        #     print("class: {:10}   prob: {:.3}".format(class_indict[str(i)],
        #                                             predict[i].numpy()))
        predict = np.array(predict).tolist()
        if max(predict) < 0.9:
            return make_err_response("图片上传错误或质量不佳，请上传生菜/芹菜的清晰图片") 
        else:
            maxindex = predict.index(max(predict))
            
            return  make_succ_response("最可能的情况为: {:10}".format(class_indict[str(maxindex)]))
        # plt.show()
