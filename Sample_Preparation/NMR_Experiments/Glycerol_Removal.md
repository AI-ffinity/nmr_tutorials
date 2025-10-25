# Removal of Glycerol

This tutorial describes the procedure for removing glycerol from protein samples. Glycerol is often used to stabilize 
proteins but interferes with NMR measurements. The equipment required is listed below:

- Fixed-angle rotor
- Pipettes (ideally 100 μL and 200 μL ranges) 
- 0.5 mL centrifugal filter unit (3–100 kDa MWCO), inserted into a larger Eppendorf tube
- NMR buffer (glycerol-free). E.g. 25 mM Tris, 150 mM NaCl, 1 mM TCEP, pH 7.5
- Protein aliquots
- Ice box
- NanoDrop instrument (for measuring concentration; see separate [tutorial](../Misc/NanoDrop_tutorial.md))
- D<sub>2</sub>O solution
- Shigemi tubes


## 1. Thawing Frozen Protein Aliquots and Spinning them

If your protein aliquots were stored at −80 °C, some protein molecules may become denatured or degraded during thawing. 
This can trigger a domino effect on the remaining protein molecules, leading to rapid aggregation or contamination that 
will hamper NMR data acquisition. To prevent that:

1. **Thaw the samples slowly** in a box filled with ice.
2. Once they are fully liquid, **spin at ≥ 15,000 g and 4 °C for 10 min**, then transfer the supernatant to a new tube.  
  You will probably see a small white pellet left behind (a *good* sign), which is aggregated protein.

**DO NOT OMIT THIS STEP**, otherwise your NMR sample may soon become unsuitable for measurements. Below is what happened 
to us when we skipped the spin at ≥ 15,000 g and 4 °C for 10 min—the protein (25 kDa) completely **aggregated** in just 
3 hours (white part of the NMR tube)!

![aggregated protein](../images/aggregated_protein.jpeg)

## 2. Preparation of Filter Units (Membrane Wetting)

This step pre-washes the filter membrane with NMR buffer.

- a) Pipette 400 μL of NMR buffer into the filter unit.
- b) Place the filter unit into the angle rotor.
- c) Centrifuge at 10g for 40 minutes at 4°C.
- d) Discard the filtrate after centrifugation.

## 3. Buffer Exchange Cycles

This step removes glycerol from the protein samples using the filter’s molecular weight cutoff, which retains proteins while allowing smaller molecules (like glycerol) to pass through. After each cycle, the protein (retentate) remains in the filter, and the glycerol (filtrate) collects in the Eppendorf tube.

**First cycle:**

- a) Thaw all three protein aliquots on ice. Each aliquot contains 100 μL of protein solution.
- b) Transfer all aliquots (300 μL total) into the pre-wet filter unit.
- c) Add 200 μL of NMR buffer to reach the unit’s 500 μL capacity.
- d) Mix gently by pipetting up and down.
- e) Centrifuge at 10g for 40 minutes at 4°C.
- f) Mix the resulting retentate gently.
- g) Record the retentate volume (should be ~120 μL).
- h) If the volume is acceptable (see the NOTE), discard the filtrate.

**Repeat the following steps twice (for cycles 2 and 3):**

- a) Top up the retentate to 500 μL with NMR buffer.
- b) Mix thoroughly by gentle pipetting.
- c) Centrifuge as before.
- d) Mix the retentate gently.
- e) Record the volume (should be ~120 μL).
- f) If volume is acceptable (see the NOTE), discard the filtrate.

After three cycles, the glycerol content should be negligible for NMR analysis.

> **_NOTE:_** Protein loss is expected after each cycle. If the retentate volume drops significantly (e.g., <50 μL), the filter unit may be faulty. In that case, measure both the filtrate and retentate concentrations using the NanoDrop (see separate [tutorial](../Misc/NanoDrop_tutorial.md)) and decide the next steps based on the result.

## 4. Measuring Final Protein Concentration

This step determines the final protein concentration after buffer exchange.

- a) Transfer the retentate to a 1 mL Eppendorf tube.
- b) Dilute to ~300 μL with NMR buffer and mix well.
- c) Keep both the sample and NMR buffer on ice.
- d) Take the box to the NanoDrop station and follow the [NanoDrop tutorial](../Misc/NanoDrop_tutorial.md).
- e) Record the final concentration.

> **_NOTE:_** Compare the final concentration to the starting concentration in the aliquotes. Protein loss should not exceed ~30–40%.

## 5. Transferring the Final Sample to a Shigemi Tube

In this step, the sample is prepared for NMR by adding D<sub>2</sub>O and submitting it to the NMR facility. Most tasks are performed by facility personnel, except for the D<sub>2</sub>O addition.

- a) Once again, check the final sample volume (~300 μL).
- b) Add ~20 μL of D<sub>2</sub>O (5–10% of the total volume) and mix gently.
- c) Submit the sample to the NMR facility personnel.

**The following steps are performed by NMR facility personnel but are included here for completeness:**

- a) Pipette 300 μL of sample into the Shigemi tube.
- b) Insert the plunger so the meniscus is 2–3 mm below the rim.
- c) Cap, clean the exterior, and load the tube into the spectrometer.

## Practical Notes

- Keep all samples/aliquotes that contain protein on ice at all time.
- Do not forget to replenish the ice once it starts to melt down.
- Always try to salvage as much material as possible with the pipette.
- Do not forget to properly discard the used pipette tips.
- Ask the responsible personnel what lab equipment (racks, pipettes...) are you allowed to use.
- After each cycle, always mix the retenate when replenishing with the NMR buffer.