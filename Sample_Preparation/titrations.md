# 15N HSQC Titrations

This tutorial will walk you through the steps for performing **15N HSQC titrations** of your protein with a set of chosen ligands.

The titrations are based on **occupancy**, which is defined as the ratio between the protein–ligand complex concentration and the total protein concentration:

```math
\begin{align*}
\text{Occupancy}~(q) &= \frac{[PL]}{[P]_{\text{total}}} \\
[P]_{\text{total}} &= [P] + [PL]
\end{align*}
```

To perform the experiment, you will first define a set of occupancy values you want to study, e.g. `(0.25, 0.5, 0.75)`. To calculate the ligand concentration required for each occupancy point, you must know the **dissociation constant (K<sub>d</sub>)** for each ligand.

This tutorial will guide you through:

- Preparing the starting sample
- Calculating the volumes needed to reach desired occupancies
- Adding the correct volume of ligand stock to the NMR tube between each measurement

## 1 . Preparing the starting sample

This section explains how to prepare the **first sample** for measurement — the reference point with **no ligand added**. To prepare it correctly and ensure reliable occupancy calculations later, you should:

- Accurately measure the **protein concentration**
- Add any **fixed binders** you want present throughout the titration (e.g. AcCoA for NatD), typically at a **1:1 ratio** with the protein
- Add **D<sub>2</sub>O** to reach a final content of **5–10%**

### 🔹 Step 1: Transfering and centrifuging

- Remove **1 protein aliquot (V = 300 μL, c = 150 μM)** from the freezer and thaw it on **ice** for approximately **10–15 minutes**.
- Pipette the contents to the Eppendorf tube.
- Centrifuge briefly if the bubbles are present.

### 🔹 Step 2: Concentration Measurement

Place the Eppendorf tube containing your sample and NMR buffer on ice, then proceed to the NanoDrop station.  
Follow the [NanoDrop tutorial](./Misc/NanoDrop_tutorial.md) to accurately measure the protein concentration and record the value.

> ⚠️ Note: Measuring the concentration will consume approximately **6–8 µL** of your sample.

### 🔹 Step 3: Addition of Fixed Binders

This step guides you in calculating and adding the volume of any additional binders to your sample.  
If you do **not** need any additional binders, you can skip directly to **Step 4**.

To calculate the volume to add, use the following formula:

```math
V_{\text{binder}}~[\mu L] = \frac{\text{binding\_ratio} \times C_{\text{protein}} \times V_{\text{protein}} \times 10^{-3}}{C_{binder}}
```

Where:
- binding_ratio = desired binder:protein ratio (e.g. for 1:2, use `binding_ratio = 2`)
- V<sub>binder</sub> = volume of additional binder to add (in μL)  
- C<sub>protein</sub> = protein concentration (in μM)  
- V<sub>protein</sub> = protein sample volume (in μL)  
- C<sub>binder</sub> = stock concentration of the additional binder (in mM)  

> ⚠️ **Units required for this formula:**
> - Protein concentration in **μM**
> - Protein volume in **μL**
> - AcCoA stock concentration in **mM**
> - Resulting AcCoA volume in **μL**

---

#### 💡 Example Calculation

You are working with **NatD** and want a **1:1 ratio** with **AcCoA**. Your AcCoA stock has a concentration of **8 mM**. Then, you have:

- binding_ratio = 1
- C<sub>protein</sub> = 120 μM  
- V<sub>protein</sub> = 294 μL  
- C<sub>binder</sub> = 8 mM

Plug the values into the formula:

```math
V_{binder}~[μL] = \frac{1\times 120\times 294\times 10^{-3}}{8} = \frac{35.28}{8} = 4.41~μL
```

- After the calculation, pipette the desired amount to the Eppendorf tube with the protein sample.
- Vortex thoroughly to ensure complete mixing.