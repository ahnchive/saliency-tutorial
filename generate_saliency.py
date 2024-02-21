
# python generate_saliency.py --input_folder '../maps/coco-search18-test-images' --output_folder '../maps/saliency/itti-koch'

import os
# import cv2
import numpy as np

from PIL import Image
import argparse
import pysaliency

PYSALIENCY_LOCATION = os.path.dirname(pysaliency.__file__)


def normalize_map(m, softmax=False, alpha=0.05):
    if softmax:
        # softmax with alpha
        m = torch.Tensor(m).flatten()
        m = F.softmax(m/alpha)
        m = np.reshape(m.numpy(), (320, 512))
        #         m = np.exp(m/alpha) / np.sum(np.exp(m/alpha)) 

    # min-max normalization
    m = (m - m.min()) / (m.max() - m.min()) * 255
    m = m.astype(np.uint8)
    return m

def overlay_map(m, img):
    m = cv2.applyColorMap(m, cv2.COLORMAP_JET)
    m = cv2.addWeighted(m, 0.5, img, 0.5, 0)
    return m

def save_map(m, img, overlay, path_savefile):
    if overlay:
        m = overlay_map(m, img)
        m = cv2.cvtColor(m, cv2.COLOR_BGR2RGB)
        m = Image.fromarray(m)
        m.save(path_savefile)
    else:
        m = Image.fromarray(m).convert("L")
        m.save(path_savefile)


def process_images(input_folder, output_folder):

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        # ask overwrite if folder exists
        overwrite = input(f'The folder {output_folder} already exists. Do you want to overwrite it? (y/n)')
        if overwrite.lower() != 'y':
            print('Exiting...')
            return 

    # Create a saliency map object

    # saliency_model = pysaliency.IttiKoch(location='models', saliency_toolbox_archive='../resources/saliency_toolbox.zip')
    saliency_model = pysaliency.IttiKoch(location=f'{PYSALIENCY_LOCATION}/scripts/models',  saliency_toolbox_archive='../resources/saliency_toolbox.zip')

    # List all files in the input folder
    input_files = os.listdir(input_folder)

    print(f'Saliency generated for {len(input_files)} images')
    # Process each file
    for filename in input_files:
        # Load the image
        image_path = os.path.join(input_folder, filename)
        image_pil = Image.open(image_path)
        image_np = np.array(image_pil)

        # Compute the saliency map
        saliency_map = saliency_model.saliency_map(image_np)
        saliency_map = normalize_map(saliency_map, softmax=False, alpha=0.05)

        # Save the saliency map
        output_path = os.path.join(output_folder, filename)
        Image.fromarray(saliency_map).convert('L').save(output_path)

    print('All saliency maps computed and saved.')

def main():
    parser = argparse.ArgumentParser(description='Compute saliency maps for images in a folder using the Itti and Koch model.')
    parser.add_argument('--input_folder', type=str, help='Path to the folder containing input images.')
    parser.add_argument('--output_folder', type=str, help='Path to the folder to save the output saliency maps.')
    args = parser.parse_args()

    process_images(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()