# this readme explains the setup used for running pysaliency
tested with python 3.9

pip install
- Cython
- numpy
- six
- pysaliency
- opencv-python
- matlabengine

# download [SaliencyToolbox](http://www.saliencytoolbox.net/)
Due to licence restrictions the Toolbox cannot be downloaded automatically. You have to download it yourself and provide the location of the zipfile via the `saliency_toolbox_archive` when you build saliency model

# run generate_saliency.py
`python generate_saliency.py --input_folder '../maps/coco-search18-test-images' --output_folder '../maps/saliency/itti-koch'`

inside the code, two parts you wan to change:
## build saliency model
```
saliency_model = pysaliency.IttiKoch(location=f'{PYSALIENCY_LOCATION}/scripts/models',  saliency_toolbox_archive='../resources/saliency_toolbox.zip')
```
- this will create/copy `SaliencyToolbox` under `models/IttiKoch`. you should locate wrapper file, `ittikoch_wrapper.m` under the same folder
- unzipped Toolbox should be `SaliencyToolbox`, you may need to remove manually suffix -main if you downloaded from github main branch. 

## generate saliency map
```
saliency_map = saliency_model.saliency_map(image_np)
```


# trouble shoot
- if your system can't find your matlab: `export PATH=$PATH:"/Applications/MATLAB_R2023b.app/bin` (for mac)



