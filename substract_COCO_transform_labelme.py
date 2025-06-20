import os
import json
import shutil
from pycocotools.coco import COCO
import cv2
import numpy as np

# 需要设置的路径
dataDir = 'D:/tempdata/COCO/'  # COCO 数据集路径
saveDir = 'D:/tempdata/generate_json/'  # 保存生成的 JSON 文件和图片的路径
img_save_dir1 = os.path.join(saveDir, 'animal')  # 保存的路径
img_save_dir2 = os.path.join(saveDir, 'animal_and_person')  # 保存的路径


# 创建保存目录
os.makedirs(img_save_dir1, exist_ok=True)
os.makedirs(img_save_dir2, exist_ok=True)

# COCO 数据集的类别列表
classes_names = ['person','cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'teddy bear']

# LabelMe 格式的颜色映射
colors = {
    'person': (255, 0, 0),  # 红色
    'cat': (0, 255, 0),  # 绿色
    'dog': (0, 0, 255),  # 蓝色
    'horse': (255, 255, 0),  # 黄色
    'sheep': (255, 0, 255),  # 粉色
    'cow': (0, 255, 255),  # 青色
    'elephant': (150, 150, 50),  # 灰色
    'bear': (150, 50, 150),  # 深紫色
    'zebra': (50, 150, 150),  # 浅青色
    'giraffe': (128, 128, 128),  # 深灰色
    'teddy bear': (0, 0, 0),  # 黑色
    'backpack': (139, 69, 19),  # 棕色
    'handbag': (255, 182, 193),  # 粉红色
    'suitcase': (105, 105, 105)  # 铅灰色
}


def check_image(coco, img_id, classes, classes_names):
    ann_ids = coco.getAnnIds(imgIds=img_id)
    anns = coco.loadAnns(ann_ids)
    has_person = False
    has_animal = False
    other_animals = False

    for ann in anns:
        class_name = classes[ann['category_id']]
        if class_name == 'person':
            has_person = True
        elif class_name in classes_names:
            has_animal = True
        else:
            other_animals = True
            break
    #return not has_person and has_animal and not other_animals
    # 检查图片是否不包含人，只包含列表中的其他动物
    if (not has_person and has_animal and not other_animals):
        return 1
    # 检查图片是否包含人且包含列表中的其他动物
    elif    (has_person and has_animal and not other_animals):
        return 2
    else:
        return 0



# 转换为 LabelMe 格式的 JSON
def coco_to_labelme(coco_json, img_info, classes):
    labelme_json = {
        #自己找一个labelme格式的json文件，修改好固定信息
        "version": "5.1.1",
        "flags": {},
        "shapes": [],
        "imagePath": img_info['file_name'],
        "imageData": None,
        "imageHeight": img_info['height'],
        "imageWidth": img_info['width']
    }
    group_id=0
    for ann in coco_json['annotations']:
        class_name = [cat['name'] for cat in coco_json['categories'] if cat['id'] == ann['category_id']][0]
        shape = {
            "label": class_name,
            "confidence":1,
            "points": [
                [ann['bbox'][0], ann['bbox'][1]],
                [ann['bbox'][0] + ann['bbox'][2], ann['bbox'][1] + ann['bbox'][3]]
            ],
            "shape_type": "rectangle",
            "group_id":group_id,
            "fill_color": None,
            "line_color":colors[class_name],
            "flags": {}
        }
        group_id=group_id+1
        labelme_json['shapes'].append(shape)

    return labelme_json

# 主程序
datasets_list = ['train2017', 'val2017']  # 数据集列表
count_1=0
count_2=0
for dataset in datasets_list:
    annFile = '{}/annotations/instances_{}.json'.format(dataDir, dataset)
    coco = COCO(annFile)
    classes = {cat['id']: cat['name'] for cat in coco.loadCats(coco.getCatIds())}
    img_ids = coco.getImgIds()

    for img_id in img_ids:
        i=check_image(coco, img_id, classes, classes_names)
        if i:
            img = coco.loadImgs(img_id)[0]
            filename = img['file_name']
            ann_ids = coco.getAnnIds(imgIds=img_id, catIds=coco.getCatIds(catNms=classes_names))
            anns = coco.loadAnns(ann_ids)

            # 创建小 JSON 文件的内容
            small_json = {
                'images': [img],
                'annotations': anns,
                'categories': coco.loadCats(coco.getCatIds(catNms=classes_names))
            }
            if i==1:
                count_1=count_1+1
                # 保存第一类对应的图片，这里是animal
                img_path = os.path.join(dataDir, dataset, filename)
                img_save_path = os.path.join(img_save_dir1, filename)
                shutil.copy(img_path, img_save_path)

                # 转换为 LabelMe 格式的 JSON
                labelme_json = coco_to_labelme(small_json, img, classes)
                labelme_save_path = os.path.join(img_save_dir1, filename.replace('.jpg', '.json'))
                with open(labelme_save_path, 'w') as f:
                    json.dump(labelme_json, f, indent=4)
            elif i==2:
                count_2=count_2+1
                # 保存第二类对应的图片，这里是animal and person
                img_path = os.path.join(dataDir, dataset, filename)
                img_save_path = os.path.join(img_save_dir2, filename)
                shutil.copy(img_path, img_save_path)

                # 转换为 LabelMe 格式的 JSON
                labelme_json = coco_to_labelme(small_json, img, classes)
                labelme_save_path = os.path.join(img_save_dir2, filename.replace('.jpg', '.json'))
                with open(labelme_save_path, 'w') as f:
                    json.dump(labelme_json, f, indent=4)
print(f"第一类animal：{count_1}")
print(f"第二类animal_and_person：{count_2}")

            