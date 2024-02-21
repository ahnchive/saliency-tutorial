# This README explains the setup used for running [pysaliency](https://github.com/matthias-k/pysaliency)
Tested with Python 3.9, matlab 2023b 

## Installation
Execute the following commands to install the necessary libraries:
```bash
pip install Cython numpy six pysaliency opencv-python matlabengine
```

## Download [SaliencyToolbox](http://www.saliencytoolbox.net/)
Due to license restrictions, the Toolbox cannot be downloaded automatically. You must download it yourself and specify the location of the zipfile via the `saliency_toolbox_archive` parameter when you build the saliency model.

## Running the Saliency Model Script
To generate saliency maps, use the following command:
```bash
python generate_saliency.py --input_folder '../maps/coco-search18-test-images' --output_folder '../maps/saliency/itti-koch'
```

### Modify in the Script
#### Building the Saliency Model
```python
saliency_model = pysaliency.IttiKoch(location=f'{PYSALIENCY_LOCATION}/scripts/models', saliency_toolbox_archive='../resources/saliency_toolbox.zip')
```
- This will create or copy `SaliencyToolbox` under `models/IttiKoch`. Ensure the wrapper file, `ittikoch_wrapper.m`, is located in the same folder.
- The unzipped Toolbox folder should be named `SaliencyToolbox`. If you downloaded it from the GitHub main branch, you may need to manually remove the suffix `-main`.

#### Generating the Saliency Map
```python
saliency_map = saliency_model.saliency_map(image_np)
```

## Troubleshooting
- If your system can't find your MATLAB installation, add your application to PATH variable. For macOS, use:
```bash
export PATH=$PATH:"/Applications/MATLAB_R2023b.app/bin"
```