import matplotlib
from transformers import DetrImageProcessor, DetrForObjectDetection, AutoImageProcessor, AutoModelForObjectDetection
import torch
from PIL import Image
from urllib.request import urlopen
import requests
import os
import matplotlib.pyplot as plt
import pathlib
matplotlib.use('agg')

BASE_PATH = pathlib.Path(__file__).parent
MODEL = 'detr-resnet-50'

# COCO classes
CLASSES = [
    'N/A', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A',
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack',
    'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
    'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
    'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]


def plot_results(pil_img, prob, boxes, labels, path_to_save_to):
    fig = plt.figure(figsize=(16,10))
    
    ax = plt.gca()
    for p, (xmin, ymin, xmax, ymax), c, label in zip(prob, boxes.tolist(), COLORS * 100, labels):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))

        text = f'{CLASSES[label]}: {p :0.4f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.imshow(pil_img)
    fig.savefig(path_to_save_to)


def process_image(image_link_or_path):
    processor = DetrImageProcessor.from_pretrained(os.path.join(BASE_PATH, MODEL))
    try:
        urlopen(image_link_or_path)
        image_data = requests.get(image_link_or_path, stream=True).raw
    except : 
        image_data = image_link_or_path
    finally:
        image = Image.open(image_data)
        return image, processor

def predict_image(image, processor, threshold, path_to_save_to):
    model = DetrForObjectDetection.from_pretrained(os.path.join(BASE_PATH, MODEL))
    
    inputs = processor(images=image, return_tensors='pt')
    outputs = model(**inputs)

    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=threshold)[0]

    return plot_results(image, results['scores'], results['boxes'], results['labels'], path_to_save_to=path_to_save_to)
