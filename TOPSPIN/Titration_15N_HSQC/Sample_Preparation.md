# README — Protein–Ligand Mixing Calculator (with DMSO Control)

This tool tells you **how much ligand stock, protein stock, neat DMSO, and buffer** to pipette so your final tube has:
- the **target ligand concentration**
- the **target DMSO fraction** (v/v)
- the **target protein concentration** (standard mode) **or** ignores it (protein-agnostic mode)
- the **final volume** you want

---

## What you provide (inputs)

- **Final volume** (e.g., `300.0` µL)
- **Ligand stock concentration** (e.g., `100000.0` µM for 100 mM)
- **DMSO fraction in ligand stock** *(0–1)* (e.g., `1.0` for 100% DMSO)
- **Target ligand concentration** in the final mix (e.g., `10.0` µM)
- **Target DMSO fraction** in the final mix *(0–1)* (e.g., `0.02` for 2%)
- **Protein stock concentration** (e.g., `150.0` µM)
- **Target protein concentration** in the final mix  
  - **Standard mode:** set to desired value (e.g., `145.0` µM)  
  - **Protein-agnostic mode:** set to `None` or `0` to **ignore** protein target (remaining volume is protein; **no buffer**)

> **Units:** Keep volumes consistent (µL recommended) and concentrations consistent (µM).  
> **Fractions:** DMSO values are fractions (0–1), not percentages.

---

## What you get (outputs)

- **`V_ligand_stock`** — volume of ligand stock to add  
- **`V_protein_stock`** — volume of protein stock to add  
- **`V_neat_DMSO`** — extra neat DMSO needed (may be 0)  
- **`V_buffer`** — buffer volume to reach the final volume

All outputs are in the same volume units as the input final volume.

---

## Example A — Standard mode (hits ligand, DMSO, **and** protein targets)

**Goal:** 300 µL final sample; ligand **10 µM**; protein **145 µM**; DMSO **2%**.  
Stocks: ligand **100 mM in 100% DMSO**; protein **150 µM** (no DMSO).

**Inputs**
- Final volume: `300.0` µL  
- Ligand stock conc: `100000.0` µM  
- DMSO in ligand stock: `1.0`  
- Target ligand conc: `10.0` µM  
- Target DMSO: `0.02`  
- Protein stock: `150.0` µM  
- Target protein: `145.0` µM

**Output**
```

V_ligand_stock  :     0.030 µL
V_protein_stock :   290.000 µL
V_neat_DMSO     :     5.970 µL
V_buffer        :     4.000 µL

```

**Interpretation**
- Add 0.03 µL ligand stock (also 0.03 µL DMSO).
- Add 5.97 µL neat DMSO to reach 2% (total DMSO = 6.00 µL).
- Add 290.00 µL protein stock; top up with 4.00 µL buffer to 300 µL.

> **Sub-µL caution:** 0.03 µL is below reliable pipetting limits. Make a **10 mM working stock** (then ligand volume ≈ 0.3 µL), or prepare a larger batch and aliquot.

---

## Example B — **Protein-agnostic mode** (ignore protein target; no buffer)

**Use when** your protein tube already holds the final volume (e.g., a Shigemi tube needs **300 µL**), and you only want to add **ligand** and **DMSO**.

**Activate:** set **Target protein concentration = `None` or `0`**.

**Goal:** same as above except **ignore** protein target; final volume **300 µL**.  
Stocks: ligand **100 mM in 100% DMSO**; protein stock on hand (no DMSO).

**Inputs**
- Final volume: `300.0` µL  
- Ligand stock conc: `100000.0` µM  
- DMSO in ligand stock: `1.0`  
- Target ligand conc: `10.0` µM  
- Target DMSO: `0.02`  
- Protein stock: `150.0` µM (value unused for calc)  
- Target protein: `None`  *(or `0`)*

**Output**
```

V_ligand_stock  :     0.030 µL
V_neat_DMSO     :     5.970 µL
V_protein_stock :   294.000 µL
V_buffer        :     0.000 µL

```

**Interpretation**
- Add 0.03 µL ligand stock and 5.97 µL neat DMSO.  
- Fill the **remaining volume** (294.00 µL) with **protein stock**.  
- **No buffer** is used in this mode.

---

