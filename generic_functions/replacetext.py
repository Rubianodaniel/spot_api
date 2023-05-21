import re

def clean_filename(filename):
    """
    Cleans a filename by replacing whitespace with underscores, removing colons,
    and eliminating any other characters not allowed in filenames.

    Args:
        filename (str): The filename to be cleaned.

    Returns:
        str: The cleaned filename.

    Raises:
        None.
    """

    filename = filename.replace(" ", "_")

    filename = filename.replace(":", "")

    filename = re.sub(r"[^\w.-]", "", filename)
    return filename


def extract_base64_image(image_base64: str, pattern:str):
    """
    Extracts the base64-encoded image data from a string based on a given pattern.

    Args:
        image_base64 (str): The string containing the base64-encoded image data.
        pattern (str): The pattern to match and extract the image data.

    Returns:
        Union[str, bool]: The extracted base64-encoded image data if a match is found,
                        False otherwise.

    Raises:
        None.
    """
    match = re.match(pattern, image_base64)
    if match:
        return match.group(1)
    return False