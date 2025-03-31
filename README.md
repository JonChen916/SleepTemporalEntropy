# Sleep Temporal Entropy (STE)

This repository provides Python code for computing **Sleep Temporal Entropy (STE)**, a novel metric that quantifies the fragmentation and irregularity of sleep architecture based on time-series sleep stage data.

---

## 🧠 What is STE?

**Sleep Temporal Entropy (STE)** is designed to capture the **temporal irregularity** and **fragmentation** in sleep patterns using entropy-based analysis. Higher STE values indicate more disorganized and fragmented sleep, which may reflect underlying sleep disorders or neurodegenerative risk.

## 🧮 Calculation Process

The Sleep Temporal Entropy (STE) is calculated based on the following steps:

1. **Sleep Stage Extraction**  
   Sleep stage sequences are extracted from polysomnography (PSG) annotations (e.g., NSRR `.xml` files), typically sampled in 30-second epochs.

2. **Preprocessing**  
   Non-sleep epochs (e.g., undefined or artifact epochs) are filtered out. The sequence is encoded numerically (e.g., Wake=0, N1=1, N2=2, N3=3, REM=4).

3. **Sliding Window Segmentation**  
   A moving window of fixed duration (e.g., 30 minutes) slides across the entire night with a predefined step (e.g., 1 epoch). Each window contains a sequence of sleep stages.

4. **Entropy Calculation**  
   Within each window, a histogram of sleep stage transitions is computed. Then, the Shannon entropy of the transition distribution is calculated.

5. **Output**  
   The result is a time-series of entropy values across the night, reflecting the temporal irregularity of sleep architecture.

---

## 📦 Files

- `SleepTemporalEntropy.py`: Core Python script for computing STE from sleep stage sequences.
- `shhs1-200001.edf` and `shhs1-200001-nsrr.xml`: Example EDF and XML annotation files from the SHHS dataset.

---

## 📥 Requirements

- Python 3.6+
- NumPy
- (Optional) Pandas, if you're processing CSV files

Install with:

```bash
pip install numpy pandas
```

---

## ▶️ How to Use

```python
from SleepTemporalEntropy import SleepTemporalEntropy

edf_file_path = './shhs1-200001.edf'
annotation_file_path = './shhs1-200001-nsrr.xml'

time_entropies = calculate_SleepTemporalEntropy(edf_file_path, annotation_file_path)

print(time_entropies)
```

---

## 📄 Citation

If you use this code in your research, please cite the following:

> Sleep Temporal Entropy (STE) — manuscript under review. Citation will be updated upon acceptance. For now, please contact the author (Jon Chen) for more information.

---

## 🤝 Contact

Feel free to open an issue or contact [Jon Chen](mailto:[jonchen@hsc.pku.edu.cn](mailto:jonchen@hsc.pku.edu.cn)) for questions or collaborations.
