import os
import json
import os.path as osp
from collections import defaultdict

cats = {
    'pm30': '30t',
    'w63' : 'caution',
    'pl15': '15speed',
    'p11' : 'no car horn',
    'pne' : 'no reverse',
    'p19' : 'no right turn',
    'i13' : 'go ahead',
    'ip'  : 'crosswalk',
    'ps'  : 'stop',
    'pl30': '30speed',
    'ph2.2': '2.2m',
    'pn'  : 'no parking'
}

categories = [
        {
            "id": 1,
            "name": "go ahead",
        },
        {
            "id": 2,
            "name": "crosswalk",
        },
        {
            "id": 3,
            "name": "no car horn",
        },
        {
            "id": 4,
            "name": "no right turn",
        },
        {
            "id": 5,
            "name": "2.2m",
        },
        {
            "id": 6,
            "name": "15speed",
        },
        {
            "id": 7,
            "name": "30speed",
        },
        {
            "id": 8,
            "name": "30t",
        },
        {
            "id": 9,
            "name": "no parking",
        },
        {
            "id": 10,
            "name": "no reverse",
        },
        {
            "id": 11,
            "name": "stop",
        },
        {
            "id": 12,
            "name": "caution",
        }
    ]

cat2id = {cat['name']: cat['id'] for cat in categories}

root = 'tt100k'

with open(osp.join(root, 'annotations.json')) as f:
    ori_json = json.load(f)

images = []
annotations = []

count = defaultdict(int)

imgs = ori_json['imgs']
anno_id = 0
for img_id, img in imgs.items():
    path = img['path']
    objs = img['objects']
    if len(objs) == 0: continue
    add = False
    for obj in objs:
        if obj['category'] in cats:
            cat = cats[obj['category']]
            bbox = obj['bbox']
            xmin, ymin, xmax, ymax = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']
            x, y, w, h = xmin, ymin, xmax - xmin, ymax - ymin
            area = w * h
            anno_id += 1
            add = True
            annotations.append({
                'area': area,
                'bbox': [x,y,w,h],
                'category_id': cat2id[cat],
                'id': anno_id,
                'image_id': img['id'],
                'iscrowd': 0
            })
            count[cat] += 1
    if add:
        images.append({
            'file_name': path,
            'id': img['id'],
            'width': 2048,
            'height': 2048
        })

print(count)

os.makedirs('tt100k/annotations', exist_ok=True)

with open('tt100k/annotations/train.json', 'w') as f:
    json.dump({'categories': categories, 'images': images, 'annotations': annotations}, f)
