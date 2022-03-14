import mxnet as mx
import numpy as np
from PIL import Image
import os
def model(prefix, epoch):
    data_names = ['data']
    data_shapes = [(data_names[0], (1, 1, 32, 280))]
    sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
    sym = sym.get_internals()['softmaxactivation0_output']
    mod = mx.mod.Module(symbol=sym, context=mx.cpu(), data_names=data_names, label_names=None)
    mod.bind(for_training=False, data_shapes=data_shapes)
    mod.set_params(arg_params, aux_params, allow_missing=False)
    return mod
def rescale_img(img, hp=32):
    if isinstance(img, np.ndarray):
        img = mx.nd.array(img)
    scale = hp / img.shape[0]
    new_width = int(scale * img.shape[1])
    if len(img.shape) == 2:  # mx.image.imresize needs the third dim
        img = mx.nd.expand_dims(img, 2)
    img = mx.image.imresize(img, w=new_width, h=hp).asnumpy()
    img = np.squeeze(img, axis=2)
    return np.expand_dims(img, 0)
def read_charset(charset_fp):
    alphabet = [None]
    with open(charset_fp, encoding='utf-8') as fp:
        for line in fp:
            alphabet.append(line.rstrip('\n'))
    inv_alph_dict = {_char: idx for idx, _char in enumerate(alphabet)}
    return alphabet, inv_alph_dict

source_dir = '/home/admin/data/xfeng/cnocr_for_idcard_intertest/densenet-lite-gru'
model = model(source_dir+'/cnocr-v1.2.0-densenet-lite-gru',39)
_alphabet,_inv_alph_dict = read_charset(os.path.join(source_dir, 'label_cn.txt'))

def set_cand_alphabet(cand_alphabet,prob_shape):
    if cand_alphabet is None:
        _cand_alph_idx = None
    else:
        _cand_alph_idx = [0] + [_inv_alph_dict[word] for word in cand_alphabet]
        _cand_alph_idx.sort()
    mask_shape = list(prob_shape)
    mask_shape[1] = 1
    mask = np.zeros(mask_shape, dtype='int8')
    mask[:, :, _cand_alph_idx] = 1
    return mask
def ctc_label(p):
    ret = []  # each element consists of [label_id, start_idx, end_idx]
    p1 = [0] + p
    for i, _ in enumerate(p):
        c1 = p1[i]
        c2 = p1[i + 1]
        if (c2 == 0 or c2 != c1) and c1 != 0 and len(ret) > 0:
            ret[-1][-1] = i
        if c2 == 0 or c2 == c1:
            continue
        ret.append([c2, i, -1])
    if len(ret) == 0:
        return [], []
    if ret[-1][-1] < 0:
        ret[-1][-1] = len(p)
    label_ids = [ele[0] for ele in ret]
    start_end_idx = [(ele[1], ele[2]) for ele in ret]
    return label_ids, start_end_idx

def _gen_line_pred_chars(line_prob):
    class_ids = np.argmax(line_prob, axis=-1)
    prediction, start_end_idx = ctc_label(class_ids.tolist())
    res = [_alphabet[p] if _alphabet[p] != '<space>' else ' ' for p in prediction]
    return res
def cnocr(img,cand_alphabet=None):
    if img.mean() < 145:
        img = 255 - img
    img = np.array(Image.fromarray(img).convert('L'))
    img = rescale_img(img)
    img = img.astype('float32')/255.0
    prob = model.predict(mx.nd.array([img]))
    mx.nd.waitall()
    prob = prob.asnumpy()
    prob = np.reshape(prob, (-1, 1, prob.shape[1]))
    if cand_alphabet is not None:
        mask = set_cand_alphabet(cand_alphabet,prob.shape)
        prob = prob * mask
    return [_gen_line_pred_chars(prob[:, 0, :])]
if __name__ == '__main__':
    img = '/home/admin/data/xfeng/cnocr_for_idcard_intertest/test_pic4.bmp'
    img = np.array(Image.open(img))
    pre = cnocr(img,None)
    print(pre)



















