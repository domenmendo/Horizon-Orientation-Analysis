
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import ndimage

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

    # Find the average angle (test)
    #bin_centers = (hist_bins[:-1] + hist_bins[1:]) / 2
    #average_angle = np.average(bin_centers, weights=hist)
    
    #return average_angle, hist, hist_bins, direction, magnitude
    return np.clip(dominant_angle+np.pi/2, -np.pi/2, np.pi/2), hist, hist_bins, direction, magnitude

# Load the image
slika = plt.imread('grass3.png')[::4, ::4, :3].mean(2)/255.

# Analyze the entire image
angle, hist, hist_bins, direction, magnitude = orientacija_horizonta(slika)

# Print the results
print('rad:', angle)
angle_degrees = np.degrees(angle)
print(f'degrees: {angle_degrees}')

# Plot the image and the histogram
plt.figure(figsize=(12, 6))

# Plot the image
plt.subplot(1, 2, 1)
plt.imshow(slika, cmap='gray')
plt.title('Image')

# Plot the histogram
plt.subplot(1, 2, 2)
plt.bar(hist_bins[:-1], hist, width=np.diff(hist_bins), edgecolor='black')
plt.title('Histogram of Gradient Directions')
plt.xlabel('Angle (radians)')
plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()