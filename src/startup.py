import json
import os
import datetime

def initialize_app():
    # Create necessary directories
    create_directories()

    # Initialize images index
    initialize_images_index()

    # Initialize ranking
    initialize_ranking()

    # Initialize log
    initialize_log()

def create_directories():
    directories = [
        'data',
        'data/images',
        'data/images/photos',
        'data/state'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    log_action("Created necessary directories")

def initialize_images_index():
    index_path = 'data/images/index.json'
    if not os.path.exists(index_path):
        images = {}
        for root, _, files in os.walk('data/images/photos'):
            for file in files:
                image_id = f"image_{len(images) + 1}"
                print(f'root: {root}, file: {file}')
                images[image_id] = f'{root}/{file}'
        
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        with open(index_path, 'w') as f:
            json.dump({"images": images}, f, indent=2)
        log_action(f"Initialized {index_path} with {len(images)} images")

def initialize_ranking():
    ranking_path = 'data/state/ranking.json'
    if not os.path.exists(ranking_path):
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        with open('data/images/index.json', 'r') as f:
            images = json.load(f)['images']
        
        ranking = {image_id: config['initial_elo'] for image_id in images}
        
        os.makedirs(os.path.dirname(ranking_path), exist_ok=True)
        with open(ranking_path, 'w') as f:
            json.dump({"ranking": ranking}, f, indent=2)
        log_action(f"Initialized {ranking_path} with {len(ranking)} image rankings")

def initialize_log():
    log_path = 'data/state/log.txt'
    if not os.path.exists(log_path):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'w') as f:
            f.write(f"{datetime.datetime.now()} - Starting the app\n")
        log_action("Initialized log file")

def log_action(message):
    with open('data/state/log.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")

if __name__ == "__main__":
    initialize_app()
