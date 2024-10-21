import gradio as gr
import json
import os
from src.startup import initialize_app
from src.elo import update_elo, get_ranking
from src.image_utils import get_random_images, get_top_images, upload_images, Image
from src.state_utils import update_ranking, update_log

# Initialize the app
initialize_app()

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Custom CSS for image sizing and layout
custom_css = """
.image-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 70vh;
}
.image-container > div {
    width: 45%;
    height: 100%;
}
.image-container img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
.button-row {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
}
#top-gallery {
    justify-content: flex-start;
    flex-direction: column;
    align-items: center;
    height: auto;
    display: flex;
    padding: 20px 0;
}
#top-gallery > div {
    width: 45%;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 50px;
}
#top-gallery img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
#top-gallery .caption {
    margin-top: 10px;
    font-weight: bold;
    font-size: 1.2em;
}
/* Hide fullscreen buttons */
.image-container .svelte-rk35yg {
    display: none !important;
}
"""

def on_select(img1: Image, img2: Image, choice):

    if img1 is not None and img2 is not None:
        winner_id = img1.id if choice == "left" else img2.id
        loser_id = img2.id if choice == "left" else img1.id
        
        old_winner_rating = get_ranking(winner_id)
        old_loser_rating = get_ranking(loser_id)
        # Update ELO ratings
        new_winner_rating, new_loser_rating = update_elo(old_winner_rating, old_loser_rating)
        
        # Update ranking and log
        update_ranking(winner_id, new_winner_rating)
        update_ranking(loser_id, new_loser_rating)
        update_log(winner_id, loser_id)
    
    # Get next pair of images
    new_img1, new_img2 = get_random_images(2)
    return new_img1.path, new_img2.path, new_img1, new_img2

def top_images():
    top_imgs = get_top_images(config['top_count'])
    return [(img.path, f"ELO: {get_ranking(img.id)}") for img in top_imgs]

with gr.Blocks(css=custom_css) as app:
    with gr.Tab("Arena"):
        with gr.Row(elem_classes="image-container"):
            img1 = gr.Image(label="Image 1", elem_id="img1")
            img2 = gr.Image(label="Image 2", elem_id="img2")
        
        img1_obj = gr.State()
        img2_obj = gr.State()
        
        with gr.Row(elem_classes="button-row"):
            btn_left = gr.Button("Select Left", size="lg")
            btn_right = gr.Button("Select Right", size="lg")
        
        def on_select_left(img1_obj, img2_obj):
            return on_select(img1_obj, img2_obj, "left")

        def on_select_right(img1_obj, img2_obj):
            return on_select(img1_obj, img2_obj, "right")

        btn_left.click(on_select_left, inputs=[img1_obj, img2_obj], outputs=[img1, img2, img1_obj, img2_obj])
        btn_right.click(on_select_right, inputs=[img1_obj, img2_obj], outputs=[img1, img2, img1_obj, img2_obj])
    
    with gr.Tab("Top"):

        refresh_btn = gr.Button("Refresh")

        gallery = gr.Gallery(
            label="Top Images",
            show_label=False,
            elem_id="top-gallery",
            columns=1,   # Changed to 1 column
            rows=20,     # Increased to match top_count
            height="100%" # TODO: the gallery is too tall but I don't know how to fix it
        )
        
        refresh_btn.click(top_images, outputs=gallery)
        
    with gr.Tab("Upload"):
        upload_files = gr.File(
            label="Upload your images",
            file_count="multiple",
            file_types=["image"]
        )
        upload_button = gr.Button("Upload Images")
        upload_output = gr.Textbox(label="Upload Status")

        upload_button.click(
            upload_images,
            inputs=[upload_files],
            outputs=[upload_output]
        )

    # Initialize the arena
    def init_arena():
        initial_img1, initial_img2 = get_random_images(2)
        return initial_img1.path, initial_img2.path, initial_img1, initial_img2

    app.load(init_arena, outputs=[img1, img2, img1_obj, img2_obj])

    # Initialize the top images
    app.load(top_images, outputs=gallery)

if __name__ == "__main__":
    app.launch()
