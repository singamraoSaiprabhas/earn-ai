# import math

# class ThermalMemorySimulator:
#     def __init__(self, kappa=0.015):
#         # kappa is a thermal-efficient constant derived from hardware calibration[cite: 1]
#         self.kappa = kappa
#         print("--- Initializing Phase 4: Thermal & Memory Emulation ---")

#     def estimate_thermal_energy(self, temp_celsius, activity_factor):
#         """
#         Calculates estimated energy using the quantum-inspired thermodynamic model.
#         Formula: E_tile = kappa * T * log2(1 + A)[cite: 1]
#         """
#         # Convert Celsius to Kelvin as required by the formula[cite: 1]
#         temp_kelvin = temp_celsius + 273.15
        
#         # Calculate the thermal-aware energy estimation[cite: 1]
#         e_tile = self.kappa * temp_kelvin * math.log2(1 + activity_factor)
#         return e_tile

#     def emulate_memory_access(self, num_layers, is_sparse=False):
#         """
#         Simulates access counts for Hybrid NVM (weights) and SRAM (activations)[cite: 1].
#         """
#         # Baseline arbitrary memory access counts for simulation purposes
#         base_weight_access = 5000 * num_layers
#         base_activation_access = 10000 * num_layers
        
#         if is_sparse:
#             # Adaptive tensor folding compresses data, reducing memory accesses[cite: 1]
#             nvm_access = int(base_weight_access * 0.4)
#             sram_access = int(base_activation_access * 0.6)
#         else:
#             nvm_access = base_weight_access
#             sram_access = base_activation_access
            
#         return nvm_access, sram_access

# if __name__ == "__main__":
#     simulator = ThermalMemorySimulator(kappa=0.015)
    
#     # 1. Thermal Simulation
#     # Sweeping temperatures as defined in the EARN-AI benchmarks[cite: 1]
#     temperatures = [25, 45, 65, 85] 
#     simulated_activity = 3.5 # Represents switching activity 'A'[cite: 1]
    
#     print("\n--- 1. Thermodynamic Energy Estimation ---")
#     for temp in temperatures:
#         energy = simulator.estimate_thermal_energy(temp, simulated_activity)
#         print(f"Ambient Temp: {temp}°C | Estimated Tile Energy (E_tile): {energy:.2f} mJ")
        
#     # 2. Memory Hierarchy Simulation
#     print("\n--- 2. Hybrid Memory Emulation (NVM & SRAM) ---")
#     # Using the 233 YOLOv8-Nano layers we parsed in Phase 1
#     yolo_layers = 233
    
#     # Simulating access patterns for both dense and sparse configurations[cite: 1]
#     dense_nvm, dense_sram = simulator.emulate_memory_access(yolo_layers, is_sparse=False)
#     sparse_nvm, sparse_sram = simulator.emulate_memory_access(yolo_layers, is_sparse=True)
    
#     print(f"[Dense Workload - YOLOv8-Nano]")
#     print(f"  - NVM Accesses (Weights): {dense_nvm:,}")
#     print(f"  - SRAM Accesses (Activations): {dense_sram:,}")
    
#     print(f"\n[Sparse Workload (Tensor Folding Active) - YOLOv8-Nano]")
#     print(f"  - NVM Accesses (Weights): {sparse_nvm:,}")
#     print(f"  - SRAM Accesses (Activations): {sparse_sram:,}\n")










# import matplotlib.pyplot as plt

# def step4_generate_metrics(evaluated_models, image_path, entropy, complexity_tier, target_bw):
#     # --- LIVE WORKLOAD ANALYZER HEADER (From Slide Image) ---
#     print("=======================================================================================")
#     print(f"EARN-AI LIVE WORKLOAD ANALYZER: [{image_path}]")
#     print("=======================================================================================")
#     print(f"  * Measured Shannon Entropy : {entropy:.3f} bits/pixel")
#     print(f"  * Visual Complexity Tier   : {complexity_tier}")
#     print(f"  * EARN-AI Target Bitwidth  : {target_bw}-bit Adaptive Folded Logic")
#     print("=======================================================================================\n")

#     print("=" * 80)
#     print("STEP 4: OPTIMIZED EVALUATION & PERFORMANCE METRICS OUTPUT")
#     print("=" * 80)
#     print("  -> Rendering benchmark tables and generating dual-axis visualization plots...\n")

#     y4 = next(m for m in evaluated_models if "YOLOv4" in m["name"])
#     y8 = next(m for m in evaluated_models if "YOLOv8" in m["name"])
#     mvit = next(m for m in evaluated_models if "MobileViT" in m["name"])
    
#     y8_base_improvement = ((y4["base_mj"] - y8["base_mj"]) / y4["base_mj"]) * 100
#     y8_run_improvement = ((y4["run_mj"] - y8["run_mj"]) / y4["run_mj"]) * 100
#     mvit_run_improvement = ((y4["run_mj"] - mvit["run_mj"]) / y4["run_mj"]) * 100

#     # --- TABLE 1 ---
#     print("=" * 80)
#     print("TABLE 1: 16-BIT BASELINE ENERGY & ARCHITECTURAL IMPROVEMENT")
#     print("=" * 80)
#     print(f"{'Parameter':<22} | {'YOLOv4':<16} | {'YOLOv8 (Ours)':<16} | {'MobileViT (Ours)'}")
#     print("-" * 80)
#     print(f"{'Mode':<22} | {'Static':<16} | {'Adaptive':<16} | {'Adaptive'}")
#     print(f"{'16-bit energy':<22} | {f'{y4.get("base_mj"):.1f} mJ':<16} | {f'{y8.get("base_mj"):.1f} mJ':<16} | {f'{mvit.get("base_mj"):.1f} mJ'}")
#     print(f"{'% improvement':<22} | {'Baseline':<16} | {f'{y8_base_improvement:.1f}%':<16} | {'N/A'}")
#     print("=" * 80)

#     # --- TABLE 2 ---
#     print("\n" + "=" * 80)
#     print("TABLE 2: RUN ENERGY SAVINGS UNDER ADAPTIVE BITWIDTH")
#     print("=" * 80)
#     print(f"{'Parameter':<22} | {'YOLOv4':<16} | {'YOLOv8 (Ours)':<16} | {'MobileViT (Ours)'}")
#     print("-" * 80)
#     print(f"{'Bitwidth':<22} | {y4['bitwidth']:<16} | {y8['bitwidth']:<16} | {mvit['bitwidth']}")
#     print(f"{'Run Energy':<22} | {f'{y4.get("run_mj"):.1f} mJ':<16} | {f'{y8.get("run_mj"):.1f} mJ':<16} | {f'{mvit.get("run_mj"):.1f} mJ'}")
#     print(f"{'% energy saved':<22} | {'Baseline':<16} | {f'{y8_run_improvement:.1f}%':<16} | {f'{mvit_run_improvement:.1f}%'}")
#     print("=" * 80)

#     # --- TABLE 3 ---
#     print("\n" + "=" * 70)
#     print("TABLE 3: MODEL RUN ENERGY & PRECISION SELECTION TABLE")
#     print("=" * 70)
#     print(f"{'Models':<24} | {'Bit Size (Bitwidth)':<20} | {'Run Energy'}")
#     print("-" * 70)
#     for m in evaluated_models:
#         print(f"{m['name']:<24} | {m['bitwidth']:<20} | {m['run_mj']:>8.1f} mJ")
#     print("=" * 70)

#     # --- TABLE 4 ---
#     print("\n" + "=" * 76)
#     print("TABLE 4: GRAPH 1 DATA - 16-BIT HARDWARE BASELINE ENERGY")
#     print("=" * 76)
#     print(f"{'Model Architecture':<24} | {'Execution Precision':<22} | {'Baseline Energy'}")
#     print("-" * 76)
#     for m in evaluated_models:
#         precision_label = "16-bit Baseline" if "Ours" in m["name"] else "16-bit Static"
#         print(f"{m['name']:<24} | {precision_label:<22} | {m['base_mj']:>10.1f} mJ")
#     print("=" * 76 + "\n")

#     # Plotting Graphs
#     models = [m["name"].replace(" (Ours)", "\n(Ours)") for m in evaluated_models]
#     base_energies = [m["base_mj"] for m in evaluated_models]
    
#     plt.figure(figsize=(14, 6))
#     bars = plt.bar(models, base_energies, color="#e76f51", edgecolor="black", width=0.55)
#     for bar in bars:
#         yval = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width() / 2.0, yval + (max(base_energies) * 0.02), f"{yval:.1f} mJ\n(16-bit)",
#                  ha="center", va="bottom", fontsize=8.5, fontweight="bold")
#     plt.ylabel("Baseline Energy (mJ)", fontsize=12, fontweight="bold")
#     plt.xlabel("Model", fontsize=12, fontweight="bold")
#     plt.title(f"Hardware Baseline Energy (16-bit) [Input: {image_path}]", fontsize=14, fontweight="bold")
#     plt.xticks(rotation=25, ha="right", fontweight="bold")
#     plt.ylim(0, max(base_energies) * 1.2)
#     plt.grid(axis="y", linestyle="--", alpha=0.4)
#     plt.tight_layout()
#     plt.savefig("graph1_16bit_baseline.png", dpi=300)
#     plt.close()
#     print("[Done] Generated 16-bit Baseline Graph: 'graph1_16bit_baseline.png'")

#     run_energies = [m["run_mj"] for m in evaluated_models]
#     bar_colors = ["#2a9d8f" if "Ours" in m["name"] else "#e76f51" for m in evaluated_models]
    
#     plt.figure(figsize=(14, 6))
#     bars = plt.bar(models, run_energies, color=bar_colors, edgecolor="black", width=0.55)
#     for i, bar in enumerate(bars):
#         bw_label = evaluated_models[i]["bitwidth"]
#         yval = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width() / 2.0, yval + (max(run_energies) * 0.02), f"{yval:.1f} mJ\n({bw_label})",
#                  ha="center", va="bottom", fontsize=8.5, fontweight="bold")
#     plt.ylabel("Operational Run Energy (mJ)", fontsize=12, fontweight="bold")
#     plt.xlabel("Model", fontsize=12, fontweight="bold")
#     plt.title(f"Run Energy Under EARN-AI Target Bitwidth Scaling [Input: {image_path}]", fontsize=14, fontweight="bold")
#     plt.xticks(rotation=25, ha="right", fontweight="bold")
#     plt.ylim(0, max(run_energies) * 1.2)
#     plt.grid(axis="y", linestyle="--", alpha=0.4)
#     plt.tight_layout()
#     plt.savefig("graph2_target_bitwidth.png", dpi=300)
#     plt.close()
#     print("[Done] Generated Target Bitwidth Graph: 'graph2_target_bitwidth.png'")

# if __name__ == "__main__":
#     # Assuming you have the previous scripts saved in the same directory:
#     from step1_model_prep import step1_model_preparation
#     from step2_entropy_profiling import step2_entropy_profiling
#     from step3_adaptive_folding import step3_adaptive_folding_and_estimation
    
#     path, arr = step1_model_preparation()
#     ent, comp_tier, bw = step2_entropy_profiling(path, arr)
#     models = step3_adaptive_folding_and_estimation(bw)
    
#     # Passing the variables from step 2 directly into step 4
#     step4_generate_metrics(models, path, ent, comp_tier, bw)


import os
import matplotlib.pyplot as plt

def step4_generate_metrics(evaluated_models, image_path, entropy, complexity_tier, target_bw, image_num):
    y4 = next(m for m in evaluated_models if "YOLOv4" in m["name"])
    y8 = next(m for m in evaluated_models if "YOLOv8" in m["name"])
    mvit = next(m for m in evaluated_models if "MobileViT" in m["name"])
    temp_c = evaluated_models[0].get("temp_c", 25)
    
    # Calculate Improvements
    y8_baseline_imp = ((y4["base_mj"] - y8["base_mj"]) / y4["base_mj"]) * 100
    mvit_baseline_imp = ((y4["base_mj"] - mvit["base_mj"]) / y4["base_mj"]) * 100
    y8_run_imp = ((y4["run_mj"] - y8["run_mj"]) / y4["run_mj"]) * 100
    mvit_run_imp = ((y4["run_mj"] - mvit["run_mj"]) / y4["run_mj"]) * 100

    print("\n" + "="*88)
    print(f"EARN-AI LIVE WORKLOAD ANALYZER: [{image_path}]")
    print("="*88)
    print(f"  * Measured Shannon Entropy : {entropy:.3f} bits/pixel")
    print(f"  * Visual Complexity Tier   : {complexity_tier}")
    print(f"  * EARN-AI Target Bitwidth  : {target_bw}-bit Adaptive Folded Logic")
    print("="*88 + "\n")

    # --- TABLE 1 ---
    print("========================================================================================")
    print("TABLE 1: 16-BIT BASELINE ENERGY & ARCHITECTURE DEPLOYMENT")
    print("========================================================================================")
    print(f"{'Parameter':<18} | {'YOLOv4':<18} | {'YOLOv8 (Ours)':<18} | {'MobileViT (Ours)'}")
    print("-" * 88)
    print(f"{'Mode':<18} | {'Static':<18} | {'Adaptive':<18} | {'Adaptive'}")
    print(f"{'16-bit energy':<18} | {y4['base_mj']:<15.1f} mJ | {y8['base_mj']:<15.1f} mJ | {mvit['base_mj']:.1f} mJ")
    print(f"{'% Improvement':<18} | {'Baseline':<18} | {y8_baseline_imp:<17.1f}% | {mvit_baseline_imp:.1f}%")
    print("========================================================================================\n")

    # --- TABLE 2 ---
    print("========================================================================================")
    print("TABLE 2: RUN ENERGY COMPARISON UNDER ADAPTIVE BITWIDTH")
    print("========================================================================================")
    print(f"{'Parameter':<18} | {'YOLOv4':<18} | {'YOLOv8 (Ours)':<18} | {'MobileViT (Ours)'}")
    print("-" * 88)
    print(f"{'Bitwidth':<18} | {'16-bit':<18} | {target_bw:<14}-bit | {target_bw}-bit")
    print(f"{'Run Energy':<18} | {y4['run_mj']:<15.1f} mJ | {y8['run_mj']:<15.1f} mJ | {mvit['run_mj']:.1f} mJ")
    print(f"{'% Improvement':<18} | {'Baseline':<18} | {y8_run_imp:<17.1f}% | {mvit_run_imp:.1f}%")
    print("========================================================================================\n")

    # --- TABLE 3 ---
    print("========================================================================================")
    print("TABLE 3: MODEL RUN ENERGY & PRECISION SELECTION TABLE")
    print("========================================================================================")
    print(f"{'Models':<24} | {'Bit Size (Bitwidth)':<26} | {'Energy Consumed'}")
    print("-" * 88)
    for m in evaluated_models:
        print(f"{m['name']:<24} | {m['bitwidth']:<26} | {m['run_mj']:.1f} mJ")
    print("========================================================================================\n")

    # --- TABLE 4 ---
    print("========================================================================================")
    print("TABLE 4: GRAPH 1 DATA - 16-BIT HARDWARE BASELINE ENERGY")
    print("========================================================================================")
    print(f"{'Model Architecture':<24} | {'Execution Precision':<26} | {'Baseline Energy'}")
    print("-" * 88)
    for m in evaluated_models:
        print(f"{m['name']:<24} | {'16-bit (Static)':<26} | {m['base_mj']:.1f} mJ")
    print("========================================================================================\n")

    # --- TABLE 5 (UPDATED WITH FPS AND THERMALS) ---
    print("=====================================================================================================")
    print(f"TABLE 5: FPS, LATENCY & MEMORY OPTIMIZATION (Simulated at {temp_c}°C Ambient)")
    print("=====================================================================================================")
    print(f"{'Model Architecture':<24} | {'Run Latency (ms)':<18} | {'FPS':<10} | {'Run Memory (MB)':<18} | {'Memory Saved'}")
    print("-" * 101)
    for m in evaluated_models:
        print(f"{m['name']:<24} | {m['run_latency_ms']:>8.1f} ms         | {m['run_fps']:>6.1f}     | {m['run_mem_mb']:>8.2f} MB         | {m['mem_saved_pct']:>8.1f}%")
    print("=====================================================================================================\n")

    # --- PLOTTING GRAPHS ---
    models_labels = [m["name"].replace(" (Ours)", "\n(Ours)") for m in evaluated_models]
    
    # 1. Baseline Energy Graph
    plt.figure(figsize=(14, 6))
    bars = plt.bar(models_labels, [m["base_mj"] for m in evaluated_models], color="#e76f51", edgecolor="black", width=0.55)
    plt.ylabel("Baseline Energy (mJ)", fontweight="bold")
    plt.title(f"Hardware Baseline Energy (16-bit) [Input: {image_num}]", fontweight="bold")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(f"graph1_16bit_baseline_img{image_num}.png", dpi=300)
    plt.close()

    # 2. Adaptive Energy Graph
    bar_colors = ["#2a9d8f" if "Ours" in m["name"] else "#e76f51" for m in evaluated_models]
    plt.figure(figsize=(14, 6))
    bars = plt.bar(models_labels, [m["run_mj"] for m in evaluated_models], color=bar_colors, edgecolor="black", width=0.55)
    plt.ylabel("Operational Run Energy (mJ)", fontweight="bold")
    plt.title(f"Run Energy Under Target Bitwidth Scaling [Input: {image_num}]", fontweight="bold")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(f"graph2_target_bitwidth_img{image_num}.png", dpi=300)
    plt.close()

    # 3. Latency Graph
    plt.figure(figsize=(14, 6))
    bars = plt.bar(models_labels, [m["run_latency_ms"] for m in evaluated_models], color="#e9c46a", edgecolor="black", width=0.55)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + (max([m["run_latency_ms"] for m in evaluated_models]) * 0.02), f"{yval:.1f} ms", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    plt.ylabel("Inference Latency (ms)", fontweight="bold")
    plt.title(f"Adaptive Inference Latency at {temp_c}°C [Input: {image_num}]", fontweight="bold")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(f"graph3_latency_img{image_num}.png", dpi=300)
    plt.close()

    # 4. FPS Graph
    plt.figure(figsize=(14, 6))
    bars = plt.bar(models_labels, [m["run_fps"] for m in evaluated_models], color="#219ebc", edgecolor="black", width=0.55)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + (max([m["run_fps"] for m in evaluated_models]) * 0.02), f"{yval:.1f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    plt.ylabel("Frames Per Second (FPS)", fontweight="bold")
    plt.title(f"Inference Throughput (FPS) at {temp_c}°C [Input: {image_num}]", fontweight="bold")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(f"graph4_fps_img{image_num}.png", dpi=300)
    plt.close()

# ==============================================================================
# DRIVER CODE FOR LOCAL/LAPTOP INDIVIDUAL IMAGE EXECUTION
# ==============================================================================
if __name__ == "__main__":
    from step2_entropy_profiling import step2_entropy_profiling
    from step3_adaptive_folding import step3_adaptive_folding_and_estimation
    
    folder_name = "test_images"
    
    if not os.path.exists(folder_name):
        print(f"[Error] Folder '{folder_name}' not found. Please create it and add .jpg images.")
        exit()
        
    image_files = [f for f in os.listdir(folder_name) if f.endswith('.jpg')]
    total_images = len(image_files)
    
    if total_images == 0:
        print(f"[Error] No .jpg images found in '{folder_name}'.")
        exit()
        
    try:
        num_images = int(input(f"Found {total_images} images. How many do you want to test individually? "))
    except ValueError:
        print("Please enter a valid number.")
        exit()
        
    num_images = min(num_images, total_images)

    for i in range(1, num_images + 1):
        img_name = f"{i}.jpg"
        img_path = os.path.join(folder_name, img_name)
        
        if not os.path.exists(img_path):
            print(f"[Warning] '{img_name}' not found. Ensure files are named 1.jpg, 2.jpg, etc.")
            continue
            
        ent, comp_tier, bw = step2_entropy_profiling(img_path)
        
        if ent is not None:
            models = step3_adaptive_folding_and_estimation(bw)
            step4_generate_metrics(models, img_path, ent, comp_tier, bw, image_num=str(i))
            
    print(f"\n[SUCCESS] Generated metrics and graphs for {num_images} individual images.")