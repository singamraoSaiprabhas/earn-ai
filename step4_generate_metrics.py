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
import matplotlib.pyplot as plt

def step4_generate_metrics(evaluated_models, image_path, entropy, complexity_tier, target_bw):
    # --- LIVE WORKLOAD ANALYZER HEADER (From Slide Image) ---
    print("=======================================================================================")
    print(f"EARN-AI LIVE WORKLOAD ANALYZER: [{image_path}]")
    print("=======================================================================================")
    print(f"  * Measured Shannon Entropy : {entropy:.3f} bits/pixel")
    print(f"  * Visual Complexity Tier   : {complexity_tier}")
    print(f"  * EARN-AI Target Bitwidth  : {target_bw}-bit Adaptive Folded Logic")
    print("=======================================================================================\n")

    print("=" * 80)
    print("STEP 4: OPTIMIZED EVALUATION & PERFORMANCE METRICS OUTPUT")
    print("=" * 80)
    print("  -> Rendering benchmark tables and generating dual-axis visualization plots...\n")

    y4 = next(m for m in evaluated_models if "YOLOv4" in m["name"])
    y8 = next(m for m in evaluated_models if "YOLOv8" in m["name"])
    mvit = next(m for m in evaluated_models if "MobileViT" in m["name"])
    
    y8_base_improvement = ((y4["base_mj"] - y8["base_mj"]) / y4["base_mj"]) * 100
    y8_run_improvement = ((y4["run_mj"] - y8["run_mj"]) / y4["run_mj"]) * 100
    mvit_run_improvement = ((y4["run_mj"] - mvit["run_mj"]) / y4["run_mj"]) * 100

    # --- TABLE 1 ---
    print("=" * 80)
    print("TABLE 1: 16-BIT BASELINE ENERGY & ARCHITECTURAL IMPROVEMENT")
    print("=" * 80)
    print(f"{'Parameter':<22} | {'YOLOv4':<16} | {'YOLOv8 (Ours)':<16} | {'MobileViT (Ours)'}")
    print("-" * 80)
    print(f"{'Mode':<22} | {'Static':<16} | {'Adaptive':<16} | {'Adaptive'}")
    print(f"{'16-bit energy':<22} | {f'{y4.get("base_mj"):.1f} mJ':<16} | {f'{y8.get("base_mj"):.1f} mJ':<16} | {f'{mvit.get("base_mj"):.1f} mJ'}")
    print(f"{'% improvement':<22} | {'Baseline':<16} | {f'{y8_base_improvement:.1f}%':<16} | {'N/A'}")
    print("=" * 80)

    # --- TABLE 2 ---
    print("\n" + "=" * 80)
    print("TABLE 2: RUN ENERGY SAVINGS UNDER ADAPTIVE BITWIDTH")
    print("=" * 80)
    print(f"{'Parameter':<22} | {'YOLOv4':<16} | {'YOLOv8 (Ours)':<16} | {'MobileViT (Ours)'}")
    print("-" * 80)
    print(f"{'Bitwidth':<22} | {y4['bitwidth']:<16} | {y8['bitwidth']:<16} | {mvit['bitwidth']}")
    print(f"{'Run Energy':<22} | {f'{y4.get("run_mj"):.1f} mJ':<16} | {f'{y8.get("run_mj"):.1f} mJ':<16} | {f'{mvit.get("run_mj"):.1f} mJ'}")
    print(f"{'% energy saved':<22} | {'Baseline':<16} | {f'{y8_run_improvement:.1f}%':<16} | {f'{mvit_run_improvement:.1f}%'}")
    print("=" * 80)

    # --- TABLE 3 ---
    print("\n" + "=" * 70)
    print("TABLE 3: MODEL RUN ENERGY & PRECISION SELECTION TABLE")
    print("=" * 70)
    print(f"{'Models':<24} | {'Bit Size (Bitwidth)':<20} | {'Run Energy'}")
    print("-" * 70)
    for m in evaluated_models:
        print(f"{m['name']:<24} | {m['bitwidth']:<20} | {m['run_mj']:>8.1f} mJ")
    print("=" * 70)

    # --- TABLE 4 ---
    print("\n" + "=" * 76)
    print("TABLE 4: GRAPH 1 DATA - 16-BIT HARDWARE BASELINE ENERGY")
    print("=" * 76)
    print(f"{'Model Architecture':<24} | {'Execution Precision':<22} | {'Baseline Energy'}")
    print("-" * 76)
    for m in evaluated_models:
        precision_label = "16-bit Baseline" if "Ours" in m["name"] else "16-bit Static"
        print(f"{m['name']:<24} | {precision_label:<22} | {m['base_mj']:>10.1f} mJ")
    print("=" * 76 + "\n")

    # Plotting Graphs
    models = [m["name"].replace(" (Ours)", "\n(Ours)") for m in evaluated_models]
    base_energies = [m["base_mj"] for m in evaluated_models]
    
    plt.figure(figsize=(14, 6))
    bars = plt.bar(models, base_energies, color="#e76f51", edgecolor="black", width=0.55)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + (max(base_energies) * 0.02), f"{yval:.1f} mJ\n(16-bit)",
                 ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    plt.ylabel("Baseline Energy (mJ)", fontsize=12, fontweight="bold")
    plt.xlabel("Model", fontsize=12, fontweight="bold")
    plt.title(f"Hardware Baseline Energy (16-bit) [Input: {image_path}]", fontsize=14, fontweight="bold")
    plt.xticks(rotation=25, ha="right", fontweight="bold")
    plt.ylim(0, max(base_energies) * 1.2)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("graph1_16bit_baseline.png", dpi=300)
    plt.close()
    print("[Done] Generated 16-bit Baseline Graph: 'graph1_16bit_baseline.png'")

    run_energies = [m["run_mj"] for m in evaluated_models]
    bar_colors = ["#2a9d8f" if "Ours" in m["name"] else "#e76f51" for m in evaluated_models]
    
    plt.figure(figsize=(14, 6))
    bars = plt.bar(models, run_energies, color=bar_colors, edgecolor="black", width=0.55)
    for i, bar in enumerate(bars):
        bw_label = evaluated_models[i]["bitwidth"]
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + (max(run_energies) * 0.02), f"{yval:.1f} mJ\n({bw_label})",
                 ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    plt.ylabel("Operational Run Energy (mJ)", fontsize=12, fontweight="bold")
    plt.xlabel("Model", fontsize=12, fontweight="bold")
    plt.title(f"Run Energy Under EARN-AI Target Bitwidth Scaling [Input: {image_path}]", fontsize=14, fontweight="bold")
    plt.xticks(rotation=25, ha="right", fontweight="bold")
    plt.ylim(0, max(run_energies) * 1.2)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("graph2_target_bitwidth.png", dpi=300)
    plt.close()
    print("[Done] Generated Target Bitwidth Graph: 'graph2_target_bitwidth.png'")

if __name__ == "__main__":
    # Assuming you have the previous scripts saved in the same directory:
    from step1_model_prep import step1_model_preparation
    from step2_entropy_profiling import step2_entropy_profiling
    from step3_adaptive_folding import step3_adaptive_folding_and_estimation
    
    path, arr = step1_model_preparation()
    ent, comp_tier, bw = step2_entropy_profiling(path, arr)
    models = step3_adaptive_folding_and_estimation(bw)
    
    # Passing the variables from step 2 directly into step 4
    step4_generate_metrics(models, path, ent, comp_tier, bw)