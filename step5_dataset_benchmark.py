import os
import random
from step2_entropy_profiling import step2_entropy_profiling
from step3_adaptive_folding import step3_adaptive_folding_and_estimation
from step4_generate_metrics import step4_generate_metrics

def run_random_dataset_benchmark():
    # If running in Google Colab, change this to "/content/test_images"
    folder_name = "test_images" 
    
    if not os.path.exists(folder_name):
        print(f"[Error] Could not find folder '{folder_name}'.")
        return
        
    image_files = [f for f in os.listdir(folder_name) if f.endswith('.jpg')]
    total_available = len(image_files)

    if total_available == 0:
        print("[Error] No images found in the folder.")
        return

    # 1. Get Dataset Size
    try:
        num_samples = int(input(f"Found {total_available} images in '{folder_name}'. How many random images do you want to process? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if num_samples > total_available:
        print(f"You only have {total_available} images. Processing all of them instead.")
        num_samples = total_available

    # 2. Get Thermal Simulation Parameter
    try:
        temp_input = input("Enter simulated ambient temperature for the Edge device in °C (Press Enter for default 45°C): ")
        temperature_c = float(temp_input) if temp_input.strip() else 45.0
    except ValueError:
        print("Invalid temperature. Defaulting to 45.0°C")
        temperature_c = 45.0

    selected_images = random.sample(image_files, num_samples)

    print("\n=======================================================================================")
    print(f"EARN-AI DATASET BENCHMARK: {num_samples} Images @ {temperature_c}°C Thermal Simulation")
    print("=======================================================================================")
    print("SELECTED TEST IMAGES FOR THIS RUN:")
    print(", ".join(selected_images))
    print("=======================================================================================\n")

    total_entropy = 0.0
    valid_images = 0

    # 3. Process Entropy Across Dataset
    for i, img_name in enumerate(selected_images, 1):
        img_path = os.path.join(folder_name, img_name)
        ent, _, _ = step2_entropy_profiling(img_path)
        
        if ent is not None:
            total_entropy += ent
            valid_images += 1
            
        if num_samples <= 50:
            print(f" -> Processed [{i}/{num_samples}] : {img_name}")
        else:
            if i % (max(1, num_samples // 10)) == 0 or i == num_samples:
                print(f" -> Processed {i}/{num_samples} random images...")

    if valid_images == 0:
        print("\n[Error] Failed to calculate entropy from the selected images.")
        return

    avg_entropy = total_entropy / valid_images

    if avg_entropy < 4.5:
        complexity_tier = "Low (Simple Backgrounds Dominant)"
        target_bw = 4
    elif avg_entropy < 6.5:
        complexity_tier = "Medium (Standard Real-World Dataset)"
        target_bw = 6
    else:
        complexity_tier = "High (Complex Textures Dominant)"
        target_bw = 8

    # 4. Feed Dataset Average AND Temperature into Step 3
    models = step3_adaptive_folding_and_estimation(target_bw, temperature_c=temperature_c)
    
    print("\n[SUCCESS] Dataset processing complete. Generating average metrics...")
    
    # 5. Output via Step 4
    step4_generate_metrics(
        evaluated_models=models, 
        image_path=f"Dataset Average ({num_samples} images)", 
        entropy=avg_entropy, 
        complexity_tier=complexity_tier, 
        target_bw=target_bw, 
        image_num="RANDOM_SUBSET"
    )

if __name__ == "__main__":
    run_random_dataset_benchmark()