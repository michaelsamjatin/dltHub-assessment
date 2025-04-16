import shutil
from pathlib import Path

def sample_dagm(dagm_root: Path, output_root: Path, cls: str = "class01", limit: int = 10):
    """
    Sample and copy a subset of DAGM dataset images.
    
    This function extracts both clean training images and anomaly/mask pairs from the 
    DAGM dataset, organizing them into a structured directory.
    
    Parameters:
    -----------
    dagm_root : Path
        Root directory containing the DAGM dataset
    output_root : Path
        Base directory where sampled images will be copied
    cls : str, default="class01"
        Class name/folder to sample from (e.g., "class01", "class02")
    limit : int, default=10
        Maximum number of images to copy for each category (clean, defect)
        
    Returns:
    --------
    None
        Files are copied to the output directory structure
    """
    
    # Paths for source directories
    class_root = dagm_root / cls
    train_img_dir = class_root / "Train"
    test_img_dir = class_root / "Test"
    label_dir = test_img_dir / "Label"

    # Output directory structure and paths
    base_out = output_root / "dagm_excerpt" / cls
    clean_dst = base_out / "Train"
    defect_dst = base_out / "Test"
    mask_dst = base_out / "Test" / "Label"

    # Copy clean images to the new directory
    clean_dst.mkdir(parents=True, exist_ok=True) # Create destination directory for clean images
    clean_imgs = sorted([f for f in train_img_dir.glob("*.PNG")])[:limit] # Create list with "limit"-amount of clean images
    for img in clean_imgs:
        shutil.copy(img, clean_dst / img.name)

    # Create destination directories for anomaly / mask pairs
    defect_dst.mkdir(parents=True, exist_ok=True)
    mask_dst.mkdir(parents=True, exist_ok=True)

    # Sort the masks 
    label_files = sorted(label_dir.glob("*_label.PNG"))
    copied = 0

    # Iterate over the masks
    for label_file in label_files:
        # Extract the image ID by removing the "_label" suffix
        img_id = label_file.stem.split("_label")[0]
        img_file = test_img_dir / f"{img_id}.PNG"

        # Only copy if both anomalous image and corresponding mask exist
        if img_file.exists():
            shutil.copy(img_file, defect_dst / img_file.name)
            shutil.copy(label_file, mask_dst / label_file.name)
            copied += 1

        # Stop once limit is reached
        if copied >= limit:
            break

    print(f"DAGM '{cls}': {len(clean_imgs)} clean + {copied} anomaly/mask pairs copied.")


def sample_mvtec(mvtec_root: Path, output_root: Path, cls: str = "bottle", limit: int = 10):
    """
    Sample and copy a subset of MVTec dataset images.
    
    This function extracts both clean training images and anomaly/mask pairs from the
    MVTec dataset, organizing them into a structured directory.
    
    Parameters:
    -----------
    mvtec_root : Path
        Root directory containing the MVTec dataset
    output_root : Path
        Base directory where sampled images will be copied
    cls : str, default="bottle"
        Class name/folder to sample from (e.g., "bottle", "cable", "pill")
    limit : int, default=10
        Maximum number of images to copy for each category (clean, defect)
        
    Returns:
    --------
    None
        Files are copied to the output directory structure
    """
    import random

    # Set up source paths according to MVTec directory structure
    class_root = mvtec_root / cls
    train_img_dir = class_root / "train" / "good"
    test_img_dir = class_root / "test" / "broken_small"
    gt_mask_dir = class_root / "ground_truth" / "broken_small"

    # Create output directory structure
    base_out = output_root / "mvtec_excerpt" / cls
    clean_dst = base_out / "train"
    defect_dst = base_out / "test"
    mask_dst = base_out / "ground_truth"

    clean_dst.mkdir(parents=True, exist_ok=True)
    defect_dst.mkdir(parents=True, exist_ok=True)
    mask_dst.mkdir(parents=True, exist_ok=True)

    # Copy a subset of the clean images
    clean_imgs = sorted(train_img_dir.glob("*.png")) # Sort images
    selected_clean = random.sample(clean_imgs, min(limit, len(clean_imgs))) # Randomly select images
    for img in selected_clean[:limit]:
        shutil.copy(img, clean_dst / img.name) # Copy into new directory

    # Copy a subset of the anomaly/mask pairs
    # Start with anomaly images
    defect_imgs = []
    for defect_type in sorted([d for d in test_img_dir.iterdir()]): # Fetch all anomaly images
        defect_imgs.append(defect_type)
        print(defect_type)
    
    # Get corresponding mask for complete anomaly/mask pair
    copied = 0
    for img in defect_imgs:
        # Construct corresponding mask path based on MVTec naming convention
        rel_path = img.relative_to(test_img_dir)
        mask_file = rel_path.with_name(rel_path.stem + "_mask" + rel_path.suffix)
        mask_path = gt_mask_dir / mask_file
        
        # Only copy if mask exists
        if mask_path.exists():
            shutil.copy(img, defect_dst / img.name)
            shutil.copy(mask_path, mask_dst / mask_path.name)
            copied += 1
            print("copied")
            
        # Stop once we reach the limit
        if copied >= limit:
            break

    print(f"MVTec '{cls}': {len(selected_clean)} clean + {copied} defect/mask pairs copied.")


if __name__ == "__main__":
    """
    Main execution block for sampling industrial anomaly detection datasets.
    
    This script creates excerpts from both MVTec and DAGM datasets, organizing
    them into a structured directory format with clean and anomaly/mask samples.
    """
    # To replicate: Replace the paths below with your own paths
    mvtec_root = Path("mvtec")     # Root directory for MVTec dataset
    dagm_root = Path("dagm")       # Root directory for DAGM dataset
    output_root = Path("./data")   # Where samples will be saved

    # Sample 10 images each from MVTec bottle class and DAGM Class1
    sample_mvtec(mvtec_root, output_root, cls="bottle", limit=10)
    sample_dagm(dagm_root, output_root, cls="Class1", limit=10)

    print("Sample data created in './data/'")