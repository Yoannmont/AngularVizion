import matplotlib
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import  torchvision.transforms as T
import matplotlib.pyplot as plt
matplotlib.use('agg')

MODEL = 'facebook/detr-resnet-50'
REVISION = 'no_timm'

# COCO classes
CLASSES ={'fr' : [
    'N/A', 'personne', 'vélo', 'voiture', 'moto', 'avion', 'bus',
    'train', 'camion', 'bateau', 'feu de signalisation', "borne d'incendie", 'N/A',
    'panneau stop', 'parcmètre', 'banc', 'oiseau', 'chat', 'chien', 'cheval',
    'mouton', 'vache', 'éléphant', 'ours', 'zèbre', 'girafe', 'N/A', 'sac à dos',
    'parapluie', 'N/A', 'N/A', 'sac à main', 'cravate', 'valise', 'frisbee', 'skis',
    'snowboard', 'ballon de sport', 'cerf-volant', 'batte de baseball', 'gant de baseball',
    'skateboard', 'surf', 'raquette de tennis', 'bouteille', 'N/A', 'verre à vin',
    'tasse', 'fourchette', 'couteau', 'cuillère', 'bol', 'banane', 'pomme', 'sandwich',
    'orange', 'brocoli', 'carotte', 'hot-dog', 'pizza', 'beignet', 'gâteau',
    'chaise', 'canapé', 'plante en pot', 'lit', 'N/A', 'table à manger', 'N/A',
    'N/A', 'toilette', 'N/A', 'télévision', 'ordinateur portable', 'souris', 'télécommande', 'clavier',
    'téléphone portable', 'micro-ondes', 'four', 'grille-pain', 'évier', 'réfrigérateur', 'N/A',
    'livre', 'horloge', 'vase', 'ciseaux', 'ours en peluche', 'sèche-cheveux',
    'brosse à dents'
], 'en' : [
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
]}

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]



def plot_results(pil_img, prob, boxes, labels, lang):
    fig = plt.figure(figsize=(15,10), facecolor='none')
    plt.imshow(pil_img)
    
    ax = plt.gca()
    for p, (xmin, ymin, xmax, ymax), c, label in zip(prob, boxes.tolist(), COLORS * 100, labels):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))

        text = f'{CLASSES[lang][label]}: {p :0.4f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    ax.axis('off')
    plt.box(False)
    ax.margins(x=0, y=0)

    return fig



def predict_image(image, threshold, lang):
    processor = DetrImageProcessor.from_pretrained(MODEL, revision=REVISION)
    model = DetrForObjectDetection.from_pretrained(MODEL, revision=REVISION)
    
    inputs = processor(images=image, return_tensors='pt')
    outputs = model(**inputs)

    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=threshold)[0]

    return plot_results(image, results['scores'], results['boxes'], results['labels'], lang)

