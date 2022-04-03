# WHU-MFM Dataset
This script is a Python Blender script for generating a multi-focus and misaligned image dataset, which contains scenes' depth and defocus maps, objects' masks, camera parameters, and blur and all-in-focus images.
## Installation
* Blender 2.93 or above, downloadable at "https://www.blender.org/".<br>
* Download the repository:<br>
	`git clone https://github.com/PeimingCHEN/WHU-MFM-Dataset`<br>
* Install the dependencies in Blender's Python environment:<br>
	`pip install -r requirements.txt`<br>
for example, in Linux system, you can use<br>
`cd blender-2.93.1-linux-x64/2.93/python/bin $ ./python3.9 -m pip install -r requirements.txt`
## Getting Started
* Step 1: We need a few assets to start the rendering. 1000 cultural heritage meshes have been collected from Sketchfab (https://www.sketchfab.com/) and kept them in `mesh.zip`. Besides, `background.blend` is a Blender file which contains 5 diverse photographic backgrounds and 5 different professional photography lights. If you want to download other meshes from Sketchfab, you can download them in `.gltf` format, and use `unpack.py` and `pre-process.py` scripts provided by us for batch decompression and preprocessing to adjust the models' location and size.<br>
	* a) Object meshes.<br>
	<img src="https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/objects.png" width="598" height="360"/><br/>
	* b) Background meshes.<br>
	<img src="https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/background.png" width="640" height="127"/><br/>
	* c) Environment lighting.<br>
	<img src="https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/lighting.png" width="540" height="360"/><br/>
	* d) Camera positions.<br>
	<img src="https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/camera.png" width="350" height="347"/><br/>

* Step 2: Set dataset related parameters in dataset_create.py.<br>
At the bottom of dataset_create.py, you can set relevant parameters as needed, including the number of meshes, the number of rendered scenes, the number of focus stacks in a scene, virtual camera parameters, result output path, etc.<br>
For more details, please refer to the code notes and our paper.<br>
* Step 3: Run the rendering code.<br>
`./blender -b background.blend -P dataset_create.py`
## Result
The dataset we produced includes two resolutions, 960 \* 720 and 480 \* 360 respectively. Each resolution renders a total of 3000 scenes for training and 300 scenes for testing, each of them contains 5 blurred RGB images, which have different focal planes and camera deviations, and corresponding 5 defocus maps, 5 depth maps, 5 masks of objects, 5 all-in-focus images (taken without using DOF), and camera matrix of each camera pose.<br>
Example scene:<br>
* Focal stack defocus images.<br>
![](https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/defocus_image.png)
* Corresponding all-in-focus images.<br>
![](https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/aif.png)
* Corresponding Defocus map.<br>
![](https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/defocus_map.png)
* Corresponding Depth map.<br>
![](https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/depth_map.png)
* Corresponding mask of object.<br>
![](https://github.com/PeimingCHEN/WHU-MFM-Dataset/blob/main/figures/mask.png)

Note: For saving time, we use the Cycle rendering engine and turn on NVIDIA Optix for rendering. Please set it according to your running device.
