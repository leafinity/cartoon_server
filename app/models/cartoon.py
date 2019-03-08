#!/usr/bin/env python

import os
import io
from enum import Enum
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.utils as vutils

from networks.cartoonTransformer import CartoonTransformer as ct
from utils import *

_model_path = 'pretrained_models'
_gpu = -1
_load_size = 450

class Style(Enum):
    '''cartoon style for tansformer'''
    HAYAO = 0
    HOSODA = 1
    PAPRIKA = 2
    SHINKAI = 3

class CartoonTransformer(object):
    """docstring for CartoonTransformer"""

    __metaclass__ = Singleton

    def __init__(self):
        super(CartoonTransformer, self).__init__()
        self._transformer = ct()

    @staticmethod
    def resize_image(image, max_size):
        ''' Resize image and keep aspect ratio

        params: 
            image: PIL image object
        '''

        h = image.size[0]
        w = image.size[1]
        ratio = h * 1.0 / w
        if ratio > 1:
            h = max_size
            w = int(h*1.0/ratio)
        else:
            w = max_size
            h = int(w * ratio)

        return image.resize((h, w), Image.BICUBIC)

    def transform(self, extension, image_list, style=Style.HAYAO):
        ''' Transform photo to cartoon

            params:
                extension: file extension, accept values: png, jpg.
                imagefile: File from request.
                style Style: target cartoon Style, 
                    passible values: Style.HAYAO, Style.HOSODA, Style.PAPRIKA, Style.SHINKAI,
                    default: Style.HAYAO.

            return tuple of file extension and trainsformed image.
        '''

        if extension not in ['png', 'jpg']:
            return None

        image = Image.fromarray(np.uint8(image_list))

        # load model
        self._transformer.load_state_dict(torch.load(os.path.join(_model_path, 
            style.name.capitalize() + '_net_G_float.pth')))
        self._transformer.eval()

        if _gpu > -1:
            # gpu mode
            self._transformer.cuda()
        else:
            # cpu mode
            self._transformer.float()

        # load image
        input_image = image#.convert("RGB")
        input_image = self.resize_image(input_image, _load_size)
        input_image = np.array(input_image)
        # RGB -> GBR
        input_image = input_image[:, :, [2, 1, 0]]
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)
        # preprocess, (-1, 1)
        input_image = -1 + 2 * input_image 
        if _gpu > -1:
            input_image = Variable(input_image, requires_grad=True).cuda()
        else:
            input_image = Variable(input_image, requires_grad=True).float()
        # forward
        output_image = self._transformer(input_image)
        with torch.no_grad():
            output_image = output_image[0]

        # BGR -> RGB
        output_image = output_image[[2, 1, 0], :, :]
        
        # deprocess, (0, 1)
        output_image = output_image.data.cpu().float() * 0.5 + 0.5

        # to png byte
        output_image = transforms.ToPILImage()(output_image)

        return extension, np.array(output_image).tolist()

if __name__ == '__main__':
    for s in Style:
        ext, image = CartoonTransformer().transform('png', open('test.png', 'rb'), s)

        f = open('output%s.%s' %(s.name, ext), 'wb')
        f.write(image)
        f.close()
