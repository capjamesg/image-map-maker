# Image Map Maker

A web tool for generating image maps.

## Demo

https://github.com/capjamesg/image-map-maker/assets/37276661/4516f2bf-9fac-4f65-86c6-9b81821a5773

## Installation

First, clone this project and install the required dependencies:

```
git clone https://github.com/capjamesg/image-map-maker
cd image-map-maker
git clone https://github.com/CASIA-IVA-Lab/FastSAM
cd FastSAM
pip3 install -e .
cd ../
mkdir assets/
```

Then, [download the FastSAM weights](https://github.com/CASIA-IVA-Lab/FastSAM?tab=readme-ov-file#model-checkpoints) and save them in the `image-map-maker` folder

To run the application, run:

```
python3 fs.py -i assets/894px-2024-132-iwc-dus-schedule-grid.jpeg
```

Where the `-i` argument is the name of the file you want to use. This file must be placed in the `assets` folder so it is accessible to the application.

## Technologies Used

* [Fast SAM](https://github.com/CASIA-IVA-Lab/FastSAM)

## License

This project is licensed under an [MIT license](LICENSE).
