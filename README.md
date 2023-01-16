# Traffic-Sign-Recognition
SUSTech Computer Vision 2022 Fall Final Project

## Installation

### Requirements

- Python ≥ 3.7
- PyTorch ≥ 1.8 and [torchvision](https://github.com/pytorch/vision/) that matches the PyTorch installation
- OpenCV is optional but needed by demo and visualization

### Build

```
git clone https://github.com/M0lotov/Traffic-Sign-Recognition.git
cd Traffic-Sign-Recognition/
python -m pip install -e detectron2
```

## Usage

### Prepare Datasets

#### Download Dataset

First download the tt100k dataset and the SUSTech dataset under `datasets` directory.

```
cd datasets/
wget http://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/data.zip
```

Then run `convert.py` to convert the annotation into **COCO** format. 

The SUSTech dataset can be downloaded from blackboard.

#### Data Preprocessing

Run the scripts `aug.py`, `aug_balance.py` to perform correspounding preprocessing.

### Training

For Retinanet and Faster RCNN, run the following command under `detectron2/` 

```
python tools/train_net.py --config-file <config-file> OUTPUT_DIR <output_dir>
```

where \<config-file\> are configs/COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml and configs/COCO-Detection/retinanet_R_50_FPN_1x.yaml and <output_dir> is the directory to store outputs like model parameters and logs.

To change the datasets for traning, modify the `DATASETS.TRAINING` field in the above config files, the available datasets are `tt100k`, `tt100k_aug`, `tt100k_aug_balance`.

### Evaluation

Run the following script to evaluate on the test dataset and output the metrics

```
python tools/train_net.py --config-file <config-file> --eval-only MODEL.WEIGHTS /path/to/checkpoint_file
```

### Demo

Run the following script to make predictions on the test dataset and visualize them

```
python demo/demo.py --config-file <configs-file> --input ../datasets/sustech/imgs/*.jpg --output <output_dir> --opts MODEL.WEIGHTS /path/to/checkpoint_file
```
