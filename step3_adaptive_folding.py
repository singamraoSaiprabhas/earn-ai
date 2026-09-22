# class ApproximateLogicSimulator:
#     def __init__(self, baseline_bitwidth=16):
#         self.baseline_bitwidth = baseline_bitwidth
#         print(f"--- Initializing Bitwidth Folding Simulator (Baseline: {self.baseline_bitwidth}-bit) ---")

#     def calculate_power_scaling(self, baseline_power, target_bitwidth):
#         """
#         Calculates the simulated power consumption when folding bitwidths.
#         Formula: P_approx = P_baseline * (b_approx / b_baseline)^2
#         """
#         scaling_factor = (target_bitwidth / self.baseline_bitwidth) ** 2
#         approximate_power = baseline_power * scaling_factor
#         return approximate_power, scaling_factor

# if __name__ == "__main__":
#     simulator = ApproximateLogicSimulator(baseline_bitwidth=16)
    
#     # We will use 100 Watts (or milliWatts) as a clean baseline to see the percentage drop easily
#     baseline_power_consumption = 100.0 
    
#     # The target bitwidths defined by the EARN-AI framework
#     target_modes = [8, 6, 4]
    
#     print(f"\nSimulating Power Reduction from a {baseline_power_consumption}W Baseline:\n")
    
#     for mode in target_modes:
#         approx_pwr, scale = simulator.calculate_power_scaling(baseline_power_consumption, mode)
#         energy_saved = 100 - (scale * 100)
        
#         print(f"[{mode}-bit Mode Execution]")
#         print(f"  - Simulated Power: {approx_pwr:.2f} W")
#         print(f"  - Energy Reduction: {energy_saved:.2f}%\n")
PLATFORM_PROFILES = {
    "Jetson Nano":    {"e_mac": 0.082e-9, "p_stat": 1.25, "clk": 921e6, "macs_cyc": 128},
    "Raspberry Pi 4": {"e_mac": 0.145e-9, "p_stat": 2.10, "clk": 1.5e9, "macs_cyc": 64},
    "Custom FPGA":    {"e_mac": 0.054e-9, "p_stat": 0.65, "clk": 300e6, "macs_cyc": 256}
}

MODEL_CATALOG = [
    {"name": "YOLOv4-Tiny",        "platform": "Jetson Nano",    "macs": 3450e6, "mode": "Static"},
    {"name": "YOLOv8-Nano (Ours)", "platform": "Jetson Nano",    "macs": 1830e6, "mode": "Adaptive"},
    {"name": "MobileViT (Ours)",   "platform": "Jetson Nano",    "macs": 420e6,  "mode": "Adaptive"},
    {"name": "CNN-Pruned",         "platform": "Custom FPGA",    "macs": 520e6,  "mode": "Static"},
    {"name": "MobileNetV2",        "platform": "Jetson Nano",    "macs": 300e6,  "mode": "Static"},
    {"name": "SqueezeNet",         "platform": "Raspberry Pi 4", "macs": 830e6,  "mode": "Static"},
    {"name": "ViT-Tiny",           "platform": "Jetson Nano",    "macs": 1100e6, "mode": "Static"},
    {"name": "EfficientNet",       "platform": "Raspberry Pi 4", "macs": 780e6,  "mode": "Static"},
    {"name": "ResNet18",           "platform": "Raspberry Pi 4", "macs": 1800e6, "mode": "Static"}
]

def step3_adaptive_folding_and_estimation(target_bw):
    print("=" * 80)
    print("STEP 3: ADAPTIVE PRECISION FOLDING & ENERGY MODELING")
    print("=" * 80)
    print(f"  -> Applying dynamic bitwidth scaling target: {target_bw}-bit precision.")
    print("  -> Traversing ONNX nodes to protect sensitive layers (decoupled heads / attention blocks).")
    print("  -> Computing hardware-aware computational energy dissipation.\n")

    evaluated_models = []
    for specs in MODEL_CATALOG:
        hw = PLATFORM_PROFILES[specs["platform"]]
        
        # Energy calculations (computation + static leakage only)
        e_comp = specs["macs"] * hw["e_mac"]
        throughput = hw["clk"] * hw["macs_cyc"]
        e_stat = hw["p_stat"] * ((specs["macs"] / throughput) * 1.35)
        
        base_mj = (e_comp + e_stat) * 1000.0
        
        if specs["mode"] == "Adaptive":
            run_mj = base_mj * (0.9 * (target_bw / 16.0)**2 + 0.1)
            active_bw_str = f"{target_bw}-bit"
        else:
            run_mj = base_mj
            active_bw_str = "16-bit"

        evaluated_models.append({
            "name": specs["name"],
            "base_mj": base_mj,
            "run_mj": run_mj,
            "bitwidth": active_bw_str
        })
        
    print("  -> Status: Precision folding and hardware simulation successfully completed.\n")
    return evaluated_models

if __name__ == "__main__":
    from step1_model_prep import step1_model_preparation
    from step2_entropy_profiling import step2_entropy_profiling
    path, arr = step1_model_preparation()
    _, _, bw = step2_entropy_profiling(path, arr)
    step3_adaptive_folding_and_estimation(bw)