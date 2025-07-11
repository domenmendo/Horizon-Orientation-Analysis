# 🌄 Horizon Orientation Analysis

This Python script analyzes image gradients to detect the **dominant orientation of horizons or linear features** in an image or within specific regions. It's particularly useful for analyzing terrain, skyline direction, or structural alignments.

---

## 🔍 Features

- 📈 **Gradient-Based Analysis**: Uses Gaussian and Sobel filters to compute image gradients.
- 🧭 **Dominant Angle Detection**: Constructs a histogram of gradient directions (weighted by magnitude) to find the strongest orientation.
- 🖼 **Full Image or Region-Specific**: Supports analysis of the entire image or predefined rectangular regions.
- 🧪 **Histogram Visualization**: Displays gradient angle distributions to assist with visual validation.
- 🧠 **Orientation Calculation**: Returns the dominant gradient angle (in both radians and degrees).

---

## 🧰 Prerequisites

Install the required Python libraries:

```bash
pip install numpy opencv-python matplotlib scipy
```

---

## 📁 How to Use

### 1. 🔎 Analyze a Single Image

For full image horizon detection (e.g., `horizont.py`):

1. Place your image (`grass3.png`) in the same directory as `horizont.py`.
2. Ensure the following code is in your `main` block:

```python
if __name__ == "__main__":
    image = cv2.imread("grass3.png")
    ...
    dominant_angle, hist_values, hist_bins, direction_map, magnitude_map = orientacija_horizonta(gray_image)
```

3. Run:

```bash
python horizont.py
```

#### Output:
- Console: Dominant angle in **radians** and **degrees**.
- Plot: 
  - Grayscale version of the image.
  - Histogram of gradient directions (weighted by magnitude).

---

### 2. 🔲 Analyze Multiple Regions

For region-specific analysis (e.g., `main.py`):

1. Place your image (`gore.jpg`) in the same directory.
2. Define regions like this:

```python
regions = [
    ((x1, y1), (x2, y2)),  # Region 1
    ((x3, y3), (x4, y4)),  # Region 2
    ...
]
```

3. In your `main.py`, ensure regions are analyzed like so:

```python
for top_left, bottom_right in regions:
    region = image[y1:y2, x1:x2]
    ...
    angle, _, _, _, _ = orientacija_horizonta(region_gray)
```

4. Run:

```bash
python main.py
```

#### Output:
- Console: Dominant angle (in degrees) for each region.
- Plot: For each region:
  - Cropped region.
  - Histogram of gradient directions.
- GUI: A `cv2.imshow` window displaying the full image with green rectangles around analyzed regions.

---

## 🧠 How It Works: `orientacija_horizonta()`

```python
def orientacija_horizonta(slika: np.ndarray) -> float:
```

### Internals:

1. **Preprocessing**:
   - Gaussian blur (`σ = 3.0`) smooths noise.
   - Sobel filters extract gradients (`dx`, `dy`).

2. **Direction & Magnitude**:
   - Compute direction: `arctan2(dy, dx)`
   - Compute magnitude: `sqrt(dx² + dy²)`

3. **Histogram**:
   - Histogram of direction angles (in `[-π, π]`), weighted by magnitude.
   - Uses `np.histogram()` to build this histogram.

4. **Dominant Angle**:
   - Chooses the bin with the maximum weighted magnitude.
   - Normalizes angle to range `[-π/2, π/2]` for horizon relevance.

5. **Returns**:
   - Dominant angle (radians)
   - Histogram values and bins
   - Direction and magnitude maps

---

## 🛠 Customization

- 📁 **Input Images**:
  - `grass3.png` → Full image analysis
  - `gore.jpg` → Region analysis

- 📐 **Regions of Interest**:
  Modify the `regions` list in `main.py`:
  ```python
  regions = [((100, 100), (300, 300)), ((400, 150), (550, 350))]
  ```

- 🌫 **Gaussian Smoothing**:
  Adjust the `sigma` value:
  ```python
  ndimage.gaussian_filter(..., sigma=3.0)
  ```

- 📊 **Histogram Resolution**:
  Change bin resolution (default = 64 bins):
  ```python
  hist_bins = np.linspace(-np.pi, np.pi, 65)
  ```

---

## 📁 File Structure

```
project/
├── horizont.py            # Full image horizon analysis
├── main.py                # Region-based horizon analysis
├── grass3.png             # Sample full image
├── gore.jpg               # Sample image for region analysis
└── README.md              # This file
```

---

## 🧪 Example Output

```
Dominant angle: 1.570796 rad (90.00°)
```

🖼 Histogram:
- Peaks near vertical → Suggests a strong vertical edge orientation.
