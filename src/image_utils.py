import datetime
import json
from dataclasses import dataclass
import shutil
from src.elo import get_ranking
from src.state_utils import update_ranking
import random
import os

@dataclass
class Image:
    id: str
    path: str

def get_top_images(count):
    with open('data/images/index.json', 'r') as f:
        index = json.load(f)['images']
    images = [Image(id, path) for id, path in index.items()]
    return sorted(images, key=lambda x: get_ranking(x.id), reverse=True)[:count]

def get_random_images(count):
    with open('data/images/index.json', 'r') as f:
        images = json.load(f)['images']
    ids = list(images.keys())
    sampled_ids = random.sample(ids, count)
    return [Image(id, images[id]) for id in sampled_ids]

def upload_images(files):

    if len(files) == 0 or files is None:
        return "No files uploaded"

    uploaded_count = 0
    for file in files:
        # Generate a unique filename
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # handle a windows filename
        filename = file.name.split('\\')[-1]
        # handle a unix filename
        filename = filename.split('/')[-1]
        filename = f'{now}_{filename}'
        filepath = f'data/images/photos/{filename}'
        
        # Save file
        shutil.copy2(file.name, filepath)
        
        # Update index
        with open('data/images/index.json', 'r') as f:
            index = json.load(f)
        new_image_id = f'image_{len(index["images"]) + 1}'
        index['images'][new_image_id] = filepath
        with open('data/images/index.json', 'w') as f:
            json.dump(index, f)

        # Update ranking
        with open('config.json', 'r') as f:
            config = json.load(f)
        initial_elo = config['initial_elo']
        update_ranking(new_image_id, initial_elo)
        
        uploaded_count += 1
    
    return f'Uploaded {uploaded_count} images'
