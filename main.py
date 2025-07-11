
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import ndimage

# Load the image
slika = cv2.imread('gore.jpg')

# Define the regions (top-left and bottom-right coordinates)
regions = [
    ((100, 100), (200, 200)),
    ((280, 140), (380, 240)),
    ((400, 500), (500, 600)),
    ((500, 250), (600, 350)),
    ((873, 359), (973, 459))
]

def orientacija_horizonta(slika: np.ndarray) -> float:
    # Apply Gaussian filter 
    slika_filt = ndimage.gaussian_filter(slika, 3.0, mode='reflect', cval=0)
    # Apply Sobel filter to get gradients in x and y directions
    slika_dx = ndimage.sobel(slika_filt, 1, mode='reflect', cval=0)
    slika_dy = ndimage.sobel(slika_filt, 0, mode='reflect', cval=0)
    # Calculate gradient magnitude and direction
    magnitude = (slika_dx**2 + slika_dy**2)**0.5
    direction = np.arctan2(slika_dy, slika_dx)
    # Create histogram with provided bins
    hist_bins = np.linspace(-np.pi, np.pi, 65)
    hist, _ = np.histogram(direction, bins=hist_bins, weights=magnitude)
    # Find the bin with the maximum value, corresponding to the dominant angle
    max_bin = np.argmax(hist)
    dominant_angle = (hist_bins[max_bin] + hist_bins[max_bin + 1]) / 2
    return np.clip(dominant_angle+np.pi/2, -np.pi/2, np.pi/2), hist, hist_bins, direction, magnitude

# Analyze each region
for i, (tl, br) in enumerate(regions):
    # Crop the region
    region = slika[tl[1]:br[1], tl[0]:br[0]]
    # Analyze the region
    angle, hist, hist_bins, direction, magnitude = orientacija_horizonta(region[::4, ::4, :3].mean(2)/255.)
    angle_degrees = np.degrees(angle)
    # Print the result
    print(f'Region {i+1}: {angle_degrees} degrees')

    # Plot the image and the histogram
    plt.figure(figsize=(12, 6))

    # Plot the image
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
    plt.title(f'Region {i+1}')

    # Plot the histogram
    plt.subplot(1, 2, 2)
    plt.bar(hist_bins[:-1], hist, width=np.diff(hist_bins), edgecolor='black')
    plt.title('Histogram of Gradient Directions')
    plt.xlabel('Angle (radians)')
    plt.ylabel('Magnitude')

    plt.tight_layout()
    plt.show()

    # Draw a rectangle on the image
    cv2.rectangle(slika, tl, br, (0, 255, 0), 2)

# Display the image with the regions
cv2.imshow('Regions', slika)
cv2.waitKey(0)
cv2.destroyAllWindows()