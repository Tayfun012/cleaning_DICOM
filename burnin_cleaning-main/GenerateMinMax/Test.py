import cv2
import numpy as np

# Example binary mask
binary_mask = np.array([
    [0, 0, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
], dtype=np.uint8)

# Find contours in the binary mask
contours, _ = cv2.findContours(binary_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# List to store rectangles
rectangles = []

# Iterate over contours and find bounding rectangles
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    rectangles.append((x, y, w, h))

# Output the list of rectangles
print("Rectangles:", rectangles)