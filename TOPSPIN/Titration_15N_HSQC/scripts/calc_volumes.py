#!/usr/bin/env python

import math
from typing import Dict


def calc_volumes_for_sample(
    V_final: float,                     # total target volume
    # ---------- ligand ----------
    C_ligand_stock: float,              # ligand conc. in stock
    DMSO_stock_pct: float,              # DMSO fraction in ligand stock (0-1)
    C_ligand_target: float,             # ligand conc. required in sample
    DMSO_target_pct: float,             # total DMSO fraction wanted in sample (0-1)
    # ---------- protein ----------
    C_protein_stock: float,             # protein conc. in stock
    C_protein_target: float,            # protein conc. required in sample
    *,
    eps: float = 1e-9,
) -> Dict[str, float]:
    """
    Compute pipetting volumes that satisfy *simultaneously*:

      • requested ligand concentration **and** DMSO percentage  
      • requested protein concentration  

    Assumptions
    -----------
    • Ligand stock is the only DMSO-containing liquid (fraction *DMSO_stock_pct*).  
    • Protein stock contains **no** DMSO (buffer only).  
    • Extra neat DMSO may be added *if* the ligand stock alone does not reach
      the target percentage.  
    • Remaining volume is filled with buffer.

    Returns
    -------
    dict with the four volumes (same units as *V_final*):

        {
            "V_ligand_stock" : …,
            "V_protein_stock": …,
            "V_neat_DMSO"    : …,
            "V_buffer"       : …,
        }

    Raises
    ------
    ValueError on any impossible or inconsistent request.
    """
    
    # ----------------------------------------------------------------- checks
    if not (0 <= DMSO_stock_pct <= 1 and 0 <= DMSO_target_pct <= 1):
        raise ValueError("DMSO fractions must be in the interval [0, 1].")

    for name, val in {
        "V_final": V_final,
        "C_ligand_stock": C_ligand_stock,
        "C_protein_stock": C_protein_stock,
    }.items():
        if val <= 0:
            raise ValueError(f"{name} must be positive.")

    if C_ligand_target < 0 or C_protein_target < 0:
        raise ValueError("Target concentrations must be non-negative.")

    # ----------------------------------------------------------------- ligand
    V_ligand_stock = (C_ligand_target / C_ligand_stock) * V_final
    if V_ligand_stock > V_final + eps:
        raise ValueError(
            f"Ligand stock volume {V_ligand_stock:.4g} exceeds total volume {V_final:.4g}"
        )

    V_DMSO_target   = DMSO_target_pct * V_final
    V_DMSO_from_lig = V_ligand_stock * DMSO_stock_pct

    if V_DMSO_from_lig > V_DMSO_target + eps:
        raise ValueError(
            f"Ligand stock already supplies {V_DMSO_from_lig:.4g} of DMSO "
            f"> target {V_DMSO_target:.4g}.  Use a weaker DMSO stock or raise "
            f"the target percentage."
        )

    V_neat_DMSO = max(0.0, V_DMSO_target - V_DMSO_from_lig)

    # ----------------------------------------------------------------- protein
    V_protein_stock = (C_protein_target / C_protein_stock) * V_final
    if V_protein_stock > V_final + eps:
        raise ValueError(
            f"Protein stock volume {V_protein_stock:.4g} exceeds total volume {V_final:.4g}"
        )

    # ----------------------------------------------------------------- buffer
    V_buffer = V_final - (V_ligand_stock + V_protein_stock + V_neat_DMSO)
    if V_buffer < -eps:
        raise ValueError(
            "Combined volumes of ligand stock, protein stock and neat DMSO "
            f"({V_ligand_stock + V_protein_stock + V_neat_DMSO:.4g}) exceed "
            f"total target volume {V_final:.4g}."
        )
    V_buffer = max(0.0, V_buffer)

    return {
        "V_ligand_stock": V_ligand_stock,
        "V_protein_stock": V_protein_stock,
        "V_neat_DMSO": V_neat_DMSO,
        "V_buffer": V_buffer,
    }


############################################################################################################

V_final=300.0              # µL
C_ligand_stock=100000.0    # μΜ
DMSO_stock_pct=1.0         # %
C_ligand_target=10      # μΜ
DMSO_target_pct=0.02       # %
C_protein_stock=150.0    # μΜ
C_protein_target=145.0     # μΜ
example = calc_volumes_for_sample(V_final, C_ligand_stock, DMSO_stock_pct, C_ligand_target, DMSO_target_pct, C_protein_stock, C_protein_target)
print("\nVolumes to add (µL)")
for k, v in example.items():
    print(f"{k:<15} : {v:9.3f}")
        
        

