import os
import sys

from image_processing import ImageProcessor

# 1. Segmentation
image = sys.argv[1]
#os.system("python3 Fashion-AI-segmentation/run.py "+image)

# 2. Pre-processing the Fashion-AI output
processor = ImageProcessor(image)
processor.prep_run()

# 3. Removing the perspective
processor.remove_perspective()

# 4. Cutting and resizing the image
processor.cut_n_resize()

# 5. Filtering the image

# 6. Aplaying the model over the image