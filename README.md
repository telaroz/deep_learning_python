# Project Setup

This repository uses Git LFS (Large File Storage) to handle large files, such as models in the `/models` directory.

You must have Git LFS installed on your system to clone this repository correctly and retrieve the large model files.

## Install Git LFS (if needed) 
- Download and install Git LFS from [https://git-lfs.github.com/](https://git-lfs.github.com/).
- After installation, initialize LFS for your user account (only needs to be done once per machine):

```bash
git lfs install
```

## Cloning the Repository

Once Git LFS is installed, you can clone the repository as usual

```bash
git clone https://github.com/telaroz/deep_learning_python
```

### Create the environment

```
python -m venv .venv
# Activate the environment:
# On Windows (cmd.exe/powershell)
.\.venv\Scripts\activate
```

### Install dependencies

```python
pip install -r requirements.txt
```

## How to run the project
To detect the License plates on an image follow these instructions:

1. Run the script
   
```bash
python script.py 
```

2. Follow the prompts
   
   2.1 Select Detection Model: The script will ask you to choose a detection model
   
   2.2 Select OCR Model: Next, choose the OCR method
   
   2.3 Enter Image Path: Finally, provide the path to the image you want to process

### Output
- The detected license plate text and the confidence score for the plate detection will be printed.
- An annotated image will be saved: `output_annotated_image.jpg`
