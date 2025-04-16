from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import dlt
from dlt.sources.helpers import requests
import os
import glob
import io


def show_sample_images(data_root: str, dataset: str = "dagm", category: str = "01", n: int = 5):
    """
    Show n sample images from the dataset.

    Parameters:
        data_root (str): Path to resized dataset root
        dataset (str): "dagm" or "mvtec"
        category (str): Category/folder name
        split (str): "clean" or "defects"
        n (int): Number of images to show
    """

    # Define directories of imagery
    img_dir = Path(data_root) / dataset / category / "test"
    mask_dir = Path(data_root) / dataset / category / "ground_truth"
    mask_dir_dagm = Path(data_root) / dataset / category / "test" / "Label"

    # Add paths for different naming conventions
    image_paths = sorted(list(img_dir.glob("*.png")) + list(img_dir.glob("*.PNG")))[:n]

    # Iterate over paths
    for img_path in image_paths:
        fig, axes = plt.subplots(1, 2 if (mask_dir / (img_path.stem + "_mask.png")).exists() or (mask_dir / (img_path.stem + "_label.PNG")).exists() else 2, figsize=(5,3))
        
        img = Image.open(img_path)

        print("Image size: ", img.size)

        axes = [axes] if not isinstance(axes, (list, np.ndarray)) else axes
        axes[0].imshow(img, cmap="gray")
        axes[0].set_title(f"Image: {img_path.name}")
        axes[0].axis("off")

        # Try finding the corresponding mask
        possible_mask_1 = mask_dir / (img_path.stem + "_mask.png")
        possible_mask_2 = mask_dir_dagm / (img_path.stem + "_label.PNG")


        if possible_mask_1.exists():
            mask = Image.open(possible_mask_1)
            axes[1].imshow(mask, cmap="gray")
            axes[1].set_title(f"Mask: {possible_mask_1.name}")
            axes[1].axis("off")
        elif possible_mask_2.exists():
            mask = Image.open(possible_mask_2)
            axes[1].imshow(mask, cmap="gray")
            axes[1].set_title(f"Mask: {possible_mask_2.name}")
            axes[1].axis("off")

        plt.tight_layout()
        plt.show()


def get_image_dimensions(image_data):
    """
    Extract the dimensions of an image from its binary data.
    
    Args:
        image_data (bytes): Binary image data
        
    Returns:
        str: Image dimensions in format "widthxheight" (e.g., "1024x768") or "Unknown" if processing fails
    """
    try:
        img = Image.open(io.BytesIO(image_data))
        return f"{img.width}x{img.height}"
    except:
        return "Unknown"
    
def image_extractor(input_dirs, size=256):
    """
    Extract images from directories, resize them, and yield structured metadata.
    
    This function recursively searches input directories for image files, processes
    each image by resizing it to the specified dimensions, and extracts metadata
    from the file path. The function automatically categorizes images based on path
    patterns (dataset type, class, split).
    
    Args:
        input_dirs (list or tuple): List of directory paths to search for images.
                                   Can be a single directory or multiple.
        size (int, optional): Target size (width and height) to resize images to.
                             Default is 256.
    
    Yields:
        dict: Dictionary containing image metadata and binary data:
            - filename (str): Original filename
            - original_path (str): Full path to the original image
            - dataset (str): Detected dataset type ('mvtec', 'dagm', or 'unknown')
            - class (str): Detected class name (e.g., 'bottle', 'Class1')
            - split (str): Detected split type ('train', 'test', 'ground_truth', or 'unknown')
            - image_data (bytes): Binary image data of the resized image
            - image_size (str): Dimensions of the resized image (e.g., '256x256')
    
    Raises:
        Exception: If an error occurs during image processing, the error is printed
                  and the image is skipped.
    """
    
    for input_dir in input_dirs:
        # Find all image files
        image_files = []
        # Check for common endings even though for this case only .png and .PNG are relevant
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']:
            # Search for paths matching the pattern
            image_files.extend(glob.glob(os.path.join(input_dir, '**', ext), recursive=True))
        
        print(f"Found {len(image_files)} images in {input_dir}")
        
        for img_path in image_files:
            try:
                # Resize image
                img = Image.open(img_path)
                img_resized = img.resize((size, size), Image.LANCZOS)
                
                # Convert to bytes
                buffer = io.BytesIO()
                img_resized.save(buffer, format='PNG')
                
                # Parse path to extract metadata
                path_parts = img_path.split(os.sep)
                
                # Default values
                dataset = "unknown"
                class_name = "unknown"
                split = "unknown"
                
                # Extract dataset type
                if "mvtec" in img_path.lower():
                    dataset = "mvtec"
                elif "dagm" in img_path.lower():
                    dataset = "dagm"
                
                # Extract split (train/test/ground_truth)
                if "train" in img_path.lower():
                    split = "train"
                elif "test" in img_path.lower():
                    split = "test"
                elif "ground_truth" in img_path.lower() or "label" in img_path.lower():
                    split = "ground_truth"
                
                # Try to extract class name
                for part in path_parts:
                    if part.startswith("Class") or part == "bottle":
                        class_name = part
                        break
                
                yield {
                    'filename': os.path.basename(img_path),
                    'original_path': img_path,
                    'dataset': dataset,
                    'class': class_name,
                    'split': split,
                    'image_data': buffer.getvalue(),
                    'image_size': f"{img_resized.width}x{img_resized.height}"
                }
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")

def run_pipeline(*input_dirs, size=256, pipeline_name="uniform_images", dataset_name="image_dataset"):
    """
    Run the dlt pipeline to process images with incremental loading support
    
    Args:
        *input_dirs: One or more input directories containing images
        size: Target size for image resizing (default: 256)
        pipeline_name: Name for the pipeline
        dataset_name: Name for the dataset in DuckDB
    """
    # Create the pipeline
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination='duckdb', 
        dataset_name=dataset_name
    )
    
    # Create a data source with incremental loading
    @dlt.source
    def image_source(dirs=None, img_size=256):
        @dlt.resource(
            primary_key="original_path",
            write_disposition="merge",  # Enable merge strategy for updates
            columns={
                # Define explicit schema for important columns
                "filename": {"data_type": "text"},
                "dataset": {"data_type": "text"},
                "class": {"data_type": "text"},
                "split": {"data_type": "text"},
                "original_width": {"data_type": "bigint"},
                "original_height": {"data_type": "bigint"},
                "resized_width": {"data_type": "bigint"},
                "resized_height": {"data_type": "bigint"},
                "image_data": {"data_type": "binary"}
            }
        )
        def images():
            yield from image_extractor(dirs, img_size)
        return images
    
    # Load the data with incremental processing
    info = pipeline.run(
        image_source(dirs=input_dirs, img_size=size),
        write_disposition="merge"  # Specify merge at the pipeline level
    )
    
    print(f"Pipeline info: {info}")
    return info