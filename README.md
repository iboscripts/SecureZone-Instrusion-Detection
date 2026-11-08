# SecureZone: Tactical Perimeter Intrusion Detection System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

## Overview
**SecureZone** is a real-time computer vision prototype designed for tactical perimeter monitoring and autonomous area defense. Developed as a proof-of-concept for defense and physical security applications, the system monitors a predefined Region of Interest (ROI), detects moving unauthorized entities, and autonomously logs security breaches. 

By leveraging adaptive background subtraction and spatial geometric algorithms, SecureZone minimizes human operator fatigue while providing continuous situational awareness.

## Core Capabilities
* **Real-Time Motion Extraction:** Utilizes Gaussian Mixture-based Background/Foreground Segmentation (MOG2) to adapt to environmental changes (e.g., lighting shifts, shadows).
* **Automated Threat Assessment:** Continuously calculates Axis-Aligned Bounding Box (AABB) intersections between the designated secure perimeter and moving entities.
* **Noise Suppression & Filtering:** Implements morphological filtering (Dilation) and minimum contour area thresholds to prevent false positives caused by environmental noise (leaves, wind, etc.).
* **Tactical Alerting & Logging:** Generates immediate visual alerts on the operator interface and writes timestamped intrusion events to a discrete log file (`intrusion_logs.txt`).

## Technical Stack & Pipeline
* **Language:** Python
* **Computer Vision Library:** OpenCV (`cv2`)
* **Pipeline Stages:** 
  1. Grayscale Conversion & Gaussian Blur (Preprocessing)
  2. MOG2 Background Subtraction (Motion Detection)
  3. Morphological Operations (Noise Elimination)
  4. Contour Analysis & Spatial Intersection (Decision Logic)

## Potential Defense & Security Use Cases
* Critical Infrastructure Protection (CIP)
* Border and Facility Perimeter Monitoring
* Temporary FOB (Forward Operating Base) Security Checks
* Unmanned Aerial Vehicle (UAV) Ground Station Security

## Future Roadmap (Scaling Up)
While this prototype uses deterministic computer vision techniques, future iterations are planned to incorporate:
- **Deep Learning Integration:** Transitioning from MOG2 to YOLOv8 for precise object classification (distinguishing between 'Human', 'Vehicle', and 'Animal').
- **PTZ Camera Integration:** Auto-tracking protocols for Pan-Tilt-Zoom cameras upon intrusion detection.
- **Thermal Imaging Support:** Adapting the pipeline for IR (Infrared) camera feeds for night-time operations.

## Installation & Usage

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/SecureZone-Intrusion-Detection.git](https://github.com/yourusername/SecureZone-Intrusion-Detection.git)