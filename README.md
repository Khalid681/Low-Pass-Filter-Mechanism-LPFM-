

# LoRa SNR Analysis and Preprocessing

This project contains Python scripts for **cleaning, processing**, and **analyzing Signal-to-Noise Ratio (SNR)** data collected from LoRaWAN communication across different bandwidths and spreading factors. The project aims to help **visualize SNR behavior** over time across two key frequencies **433 MHz** and **915 MHz** and identify **gain points** and **intersections** that indicate performance shifts.

---

## 📁 Project Structure

```
.
├── preprocess_and_split.py       # Cleans and splits the main dataset by BW and SF
├── snr_analysis_plot.py          # Analyzes and visualizes SNR gain/intersections
├── requirements.txt              # List of required Python libraries
├── README.md                     # Project documentation (this file)
├── processed_datasets/           # Output: Cleaned datasets grouped by BW & SF
├── plots/                        # Output: SNR analysis graphs
```

---

## ⚙️ Setup

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## 1️⃣ Dataset Preprocessing

**Script:** `preprocess_and_split.py`
**What it does:**

* Loads the raw dataset (`main_data.csv`)
* Removes missing and outlier values
* Filters the dataset for:

  * **Bandwidths:** 125, 250, 500 kHz
  * **Spreading Factors:** SF10, SF11, SF12
* Outputs **9 cleaned CSV files** into the `processed_datasets/` folder

**How to run:**

Update the path to your dataset inside the script:

```python
main_dataset_path = r'path_to/main_data.csv'
```

Then run:

```bash
python preprocess_and_split.py
```

---

## 2️⃣ SNR Gain & Intersection Analysis

**Script:** `snr_analysis_plot.py`
**What it does:**

* Loads cleaned SNR datasets from both 433 MHz and 915 MHz
* Applies a **Weighted Moving Average (WMA)**
* Detects:

  * **SNR gain shift zones**
  * **Intersections** between the two frequency curves
* Highlights the **top 3 SNR gain shifts**
* Plots and saves annotated graphs

**How to run:**

Update paths in the script:

```python
data_433 = pd.read_csv("processed_datasets/data_433.csv")
data_915 = pd.read_csv("processed_datasets/data_915.csv")
```

Run:

```bash
python snr_analysis_plot.py
```

---

## 📊 Output Example

* **Black Dots:** Intersections between 433 MHz and 915 MHz SNR curves
* **Green Arrows:** Key SNR gain shift zones
* **Annotations:** Average SNR gains at critical shifts

---

## 🧰 Requirements

* Python 3.x
* `pandas`
* `numpy`
* `matplotlib`

Install all dependencies via:

```bash
pip install -r requirements.txt
```

---

## 🙋‍♂️ Author

**Khalid Usman**
If you find this helpful repository, consider starring it or citing it in your research.


