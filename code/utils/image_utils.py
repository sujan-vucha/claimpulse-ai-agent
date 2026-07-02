"""
image_utils.py

Helpers for loading and preparing images before sending to Gemini.
"""
from pathlib import Path


def load_images(image_paths_str: str, dataset_root: str) -> list[str]:
    """
    Parse the semicolon-separated image_paths field and return
    a list of resolved absolute file paths.

    Args:
        image_paths_str: Raw value from the CSV image_paths column.
        dataset_root: Absolute path to the dataset/ directory.

    Returns:
        List of absolute path strings.
    """
    raise NotImplementedError


def get_image_ids(image_paths_str: str) -> list[str]:
    """
    Extract image IDs (filename without extension) from image_paths string.

    Args:
        image_paths_str: Raw value from the CSV image_paths column.

    Returns:
        List of image ID strings, e.g. ['img_1', 'img_2'].
    """
    raise NotImplementedError
