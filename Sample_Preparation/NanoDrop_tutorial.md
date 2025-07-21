# Measurement of Protein Concentration with NanoDrop Spectrophotometer

The NanoDrop spectrophotometer uses **surface tension** to hold small liquid samples in place, eliminating the need for cuvettes or capillaries. It operates based on **UV/Vis spectroscopy**, measuring light absorbance at specific wavelengths.

This tutorial provides step-by-step instructions for measuring protein concentration at **280 nm**. To do so accurately, you must also know the **extinction coefficient** and **molecular weight** of the measured protein, which can be obtained using the **ProtParam** tool.

---

## 📦 Equipment (available at the NanoDrop station)

- NanoDrop spectrophotometer (with NanoDrop GUI)
- Milli-Q detergent (for cleaning)
- Pipettes (1–20 μL range)
- Wiping tissues

## 🧪 User-Provided Materials

- NMR buffer (for blanking)
- Protein sample
- Extinction coefficient and molecular weight (from ProtParam)

---

## 1. Obtaining the Extinction Coefficient via ProtParam

1. Visit [ProtParam](https://web.expasy.org/protparam/)
2. Paste your protein's FASTA sequence
3. Click `Compute Parameters`
4. Locate the **Extinction Coefficient** section
5. ✅ **If your buffer contains reducing agents (e.g., DTT or TCEP)**, choose the value assuming all Cys are **reduced**

---

## 2. Preparation of Samples for Measurement

Before performing NanoDrop measurements, the protein solution must be diluted to ensure that the absorbance at 280 nm (**A280**) falls within the linear range of the Beer–Lambert law, typically **between 0.1 and 1.0**.

Because the stock concentration is often unknown, begin with a test dilution and increase if necessary. Once you determine the correct dilution factor, prepare a triplicate set for accurate measurement.

### 📐 Useful Equations

```txt
Dilution factor = (sample volume + buffer volume) / sample volume  
Total dilution = dilution_1 × dilution_2 × ...
c [μM] = (A × 10⁶ × dilution) / ε  
c [μM] = (mg/mL × 10⁶ × dilution) / MW
```

---

### 🔬 Step 1: Prepare a 20× Test Dilution Sample

- 2 μL protein + 38 μL buffer → total = 40 μL  
- Dilution = **20×**  
- Vortex thoroughly

---

### 🧪 Step 2: Measure A280

- Measure **3 μL** on NanoDrop
- If **A280 < 1.0**, proceed to replicate measurements
- If **A280 > 1.0**, dilute further:

| Final Dilution | Dilution Step | Test Dilution Sample | Buffer | Total Vol |
|----------------|----------------|--------|--------|-----------|
| 30×            | 1.5×           | 6 μL   | 3 μL   | 9 μL      |
| 40×            | 2×             | 5 μL   | 5 μL   | 10 μL     |
| 50×            | 2.5×           | 4 μL   | 6 μL   | 10 μL     |

> 💡 Example: 20× → 2× → 40× total dilution

---

### ✅ Step 3: Prepare Final Replicates

- Once the correct dilution is identified, prepare **3 replicates**
  - Each should yield at least **15 μL** (5 × 3 μL measurements)
- ✅ If the initial 20× test is valid, you can use it as **Replicate 1**

---

## 3. Measurement Procedure

1. Clean both tips:
   - Load 3 μL Milli-Q
   - Close lid briefly
   - Wipe both tips

2. Open NanoDrop software
   - Select **"Protein A280"**

3. Under `Type`, choose:
   - ✅ **"Other protein (E & MW)"**
     - Enter **ε** from ProtParam (in thousands, e.g., 21 for 21,000)
     - Enter **MW** in kDa

4. Blank:
   - Load **3 μL NMR buffer**
   - **Close lid**, click **Blank**

5. Measure sample:
   - Wipe tips
   - Load **3 μL protein sample**
   - **Close lid**, click **Measure**

6. Record results:
   - A280
   - mg/mL value reported by NanoDrop

> 🧼 Only clean with Mili-Q and return to the homescreen **after final replicate**, not between every measurement

---

## 4. Calculating Protein Concentration

After measurement, you can calculate protein concentration using either of the following methods:

> 🧠 Best Practice: Record **both A280 and mg/mL** for cross-checking

---

### 🔹 Method 1: Using Absorbance (A280)

> ℹ️ NanoDrop standardizes all readings to a **1 cm path length**, so `l = 1`

- Calculate the average Absorbance over one replicate, and use:

```math
c [μM] = \frac{(A_{avg} × 10^6 × dilution)}{ε}
```
**Example:**  
- A = 0.750  
- ε = 21,000  
- dilution = 30×

```
c = (0.750 × 10⁶ × 30) / 21,000  
  = 22,500,000 / 21,000  
  = 1,071.4 μM
```

---

### 🔹 Method 2: Using mg/mL from NanoDrop

```txt
c [μM] = (mg/mL × 10⁶ × dilution) / MW
```

**Example:**  
- mg/mL = 0.85  
- MW = 71,000  
- dilution = 30×

```
[μM] = (0.85 × 10⁶ × 30) / 71,000  
     = 25,500,000 / 71,000  
     = 359.2 μM
```

---

### 📊 Final Reporting

- Average the **three replicate concentrations**
- Optionally report **standard deviation**
- Report final result in **μM**

---

## 🧠 Tips & Best Practices

- Always mix dilutions thoroughly
- Do not rely on “1 Abs = 1 mg/mL” mode
- Clean tips carefully — but only do a full reset after the full triplicate
- Use both A280 and mg/mL values when possible
- Never forget to apply the **dilution factor**

---