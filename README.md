# EARN-AI: Adaptive Bitwidth Architecture for Edge AI Inference

EARN-AI is an adaptive precision-folding architecture designed to dynamically optimize deep learning inference on resource-constrained Edge AI hardware. By analyzing the **Shannon Entropy** of incoming image data in real-time, EARN-AI shifts neural network operations away from static 16-bit execution to lower, adaptive bitwidths (e.g., 8-bit, 6-bit, 4-bit) without compromising task-critical accuracy.

This project simulates, benchmarks, and visualizes the performance of major edge models (MobileNetV2, YOLOv4-Tiny, YOLOv8-Nano, MobileViT, etc.) against custom EARN-AI adapted models under varying ambient temperatures and datasets.

## 🚀 Key Features

*   **Entropy-Driven Precision Selection:** Dynamically scales hardware execution bitwidth based on the visual complexity (Shannon Entropy) of the input image.
*   **Thermal-Aware Profiling:** Simulates real-world edge device throttling by factoring ambient operating temperature ($T^\circ\text{C}$) into latency and Frames Per Second (FPS) calculations.
*   **Comprehensive Metric Modeling:** Accurately calculates Energy Consumption (mJ), Latency (ms), Inference Throughput (FPS), and Memory Footprint Reduction (%).
*   **Hardware Baseline Calibration:** Grounded in a highly accurate "Base Paper ASIC" hardware profile, with extensible support for Jetson Nano, Raspberry Pi 4, and Custom FPGAs.

## 🗂️ Pipeline Structure

The architecture is broken down into a 5-step modular pipeline:

1.  **`step1_model_prep.py`**: Handles preliminary model loading and parameter configurations.
2.  **`step2_entropy_profiling.py`**: Scans the input image and calculates Shannon Entropy to determine the target bitwidth tier (Low, Medium, High complexity).
3.  **`step3_adaptive_folding.py`**: Applies precision folding algorithms and mathematical hardware estimations (Thermal latency penalty, Adaptive Energy Scaling, Memory footprint calculations).
4.  **`step4_generate_metrics.py`**: Evaluates individual local images, formats 5 detailed console tables, and plots 4 comparative graphs.
5.  **`step5_dataset_benchmark.py`**: Executes massive batch datasets, computing aggregated averages and thermal simulations across thousands of images simultaneously.

## 🛠️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/singamraosaiprabhas/earn-ai.git](https://github.com/singamraosaiprabhas/earn-ai.git)
    cd earn-ai
    ```
2.  **Set up a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    *(Ensure you have NumPy, Matplotlib, and OpenCV installed)*
    ```bash
    pip install numpy matplotlib opencv-python
    ```
4.  **Prepare your image directory:**
    Create a folder named `test_images` in the root directory and add `.jpg` files for testing.

## 💻 Usage & Execution

### 1. Test Individual Local Images (In-House Testing)
To analyze specific images and view how EARN-AI dynamically reacts to their individual complexities, run Step 4 directly.

Prompt: The script will detect your test_images folder and ask how many images to evaluate individually.

Output: Generates comprehensive tables and visual graphs for each processed image.

## Large Dataset Batch Benchmark (Production/Cloud Testing)
To benchmark a massive dataset (like a COCO subset) and simulate thermal throttling on edge devices, run Step 5.

python step5_dataset_benchmark.py
Prompt 1: Input the number of random samples to process (e.g., 1000).

Prompt 2: Enter the simulated ambient temperature (e.g., 45°C for a standard hot edge device, or 65°C for extreme throttling).


Output: Generates a unified, aggregated benchmark of the entire dataset.
