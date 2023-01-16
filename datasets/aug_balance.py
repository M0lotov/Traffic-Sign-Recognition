'''
用于创建图像识别数据集
'''
import os.path
import os
import json
from PIL import Image
import random
from collections import defaultdict

root = 'tt100k'
preprocessed_root = 'tt100k_aug_balance'
os.makedirs(preprocessed_root, exist_ok=True)
os.makedirs(os.path.join(preprocessed_root, 'train'), exist_ok=True)
os.makedirs(os.path.join(preprocessed_root, 'annotations'), exist_ok=True)

cat_num = defaultdict(int)
cat_objs = defaultdict(list)

with open(os.path.join(root, 'annotations', 'train.json')) as f:
    json_data = json.load(f)
imgs = {img['id']: img['file_name'] for img in json_data['images']}
categories = json_data['categories']
for obj in json_data['annotations']:
    if obj['area'] > 3600:
        cat = obj['category_id']
        obj['file_name'] = imgs[obj['image_id']]
        cat_objs[cat].append(obj)
        cat_num[cat] += 1

annotations = []
images = []

ids = list(range(5000))
random.shuffle(ids)
img_id = 1
for cat, objs in cat_objs.items():
    n = 0
    while n < 400:
        obj = objs[n % len(objs)]
        x, y, w, h = obj['bbox']
        img = Image.open(os.path.join(root, obj['file_name']))
        scale = (5 + random.random() * 15) / 100
        k = 1 / scale
        x1 = max(0, int(x - (k/2 - 0.5) * w))
        x2 = min(2048, int(x + (k/2 + 0.5) * w))
        y1 = max(0, int(y - (k/2 - 0.5) * h))
        y2 = min(2048, int(y + (k/2 + 0.5) * h))
        x, y = x - x1, y - y1
        img = img.crop((x1,y1,x2,y2))
        if random.random() < 0.3:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            x = x2 - x1 - (x + w)
        if random.random() < 0.5:
            scale = 1 + random.random() * 0.5
            img = img.resize((int(img.width*scale), int(img.height*scale)), resample=Image.Resampling.BICUBIC)
            x, y, w, h = x*scale, y*scale, w*scale, h*scale, 
        id = ids[img_id]
        img.save(os.path.join(preprocessed_root, 'train', str(id)+'.jpg'))
        annotations.append({
            'id': id,
            'image_id': id,
            'category_id': cat,
            'bbox': [x, y, w, h],
            'area': w*h,
            'iscrowd': 0
        })
        images.append({
            'id': id,
            'width': img.width,
            'height': img.height,
            'file_name': 'train' + '/' + str(id) + '.jpg'
        })
        n +=1
        img_id += 1

augmented = {
    'categories': categories,
    'images': images,
    'annotations': annotations
}

with open(os.path.join(preprocessed_root, 'annotations', 'train.json'), 'w') as f:
    json.dump(augmented, f)


