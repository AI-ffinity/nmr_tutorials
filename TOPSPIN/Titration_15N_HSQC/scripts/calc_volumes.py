#!/usr/bin/env python

import math
from typing import Dict, Optional


def calc_volumes_for_sample(
    V_final: float,                     # total target volume
    # ---------- ligand ----------
    C_ligand_stock: float,              # ligand conc. in stock (e.g., µM)
    DMSO_stock_pct: float,              # DMSO fraction in ligand stock (0-1)
    C_ligand_target: float,             # ligand conc. required in sample
    DMSO_target_pct: float,             # total DMSO fraction wanted in sample (0-1)
    # ---------- protein ----------
    C_protein_stock: float,             # protein conc. in stock (ignored in protein-agnostic mode)
    C_protein_target: Optional[float],  # protein conc. required in sample; if None or 0 -> protein-agnostic mode
    *,
    eps: float = 1e-9,
) -> Dict[str, float]:
    """
    Compute pipetting volumes that satisfy *simultaneously*:

      • requested ligand concentration **and** DMSO percentage
      • requested protein concentration  (standard mode)

    Special mode (protein-agnostic)
    -------------------------------
    If C_protein_target is None or 0:
      • Ignore target protein concentration.
      • No buffer is used.
      • Remaining volume after ligand + neat DMSO is filled with protein stock.

    Assumptions
    -----------
    • Ligand stock is the only DMSO-containing liquid (fraction *DMSO_stock_pct*).
    • Protein stock contains **no** DMSO (buffer only).
    • Extra neat DMSO may be added *if* the ligand stock alone does not reach the target percentage.
    • In standard mode, remaining volume is filled with buffer.

    Returns
    -------
    dict with volumes (same units as *V_final*):
        {
            "V_ligand_stock": ...,
            "V_protein_stock": ...,
            "V_neat_DMSO": ...,
            "V_buffer": ...
        }

    Raises
    ------
    ValueError on any impossible or inconsistent request.
    """

    # --------------------------------------------------------------- checks
    if not (0 <= DMSO_stock_pct <= 1 and 0 <= DMSO_target_pct <= 1):
        raise ValueError("DMSO fractions must be in the interval [0, 1].")

    if V_final <= 0 or C_ligand_stock <= 0:
        raise ValueError("V_final and C_ligand_stock must be positive.")

    protein_agnostic = (C_protein_target is None) or (abs(C_protein_target) < eps)

    # Only require a positive protein stock concentration in standard mode
    if not protein_agnostic and C_protein_stock <= 0:
        raise ValueError("C_protein_stock must be positive in standard mode.")

    if C_ligand_target < 0:
        raise ValueError("C_ligand_target must be non-negative.")
    if not protein_agnostic and C_protein_target is not None and C_protein_target < 0:
        raise ValueError("C_protein_target must be non-negative.")

    # ---------------------------------------------------------------- ligand
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

    # --------------------------------------------------------------- protein/buffer
    if protein_agnostic:
        # Fill remaining volume with protein stock; no buffer
        V_protein_stock = V_final - (V_ligand_stock + V_neat_DMSO)
        if V_protein_stock < -eps:
            raise ValueError(
                "Ligand stock + neat DMSO exceed the total target volume. "
                "Lower C_ligand_target and/or DMSO_target_pct."
            )
        V_protein_stock = max(0.0, V_protein_stock)
        V_buffer = 0.0
    else:
        # Standard mode: hit target protein concentration and top up with buffer
        V_protein_stock = (C_protein_target / C_protein_stock) * V_final
        if V_protein_stock > V_final + eps:
            raise ValueError(
                f"Protein stock volume {V_protein_stock:.4g} exceeds total volume {V_final:.4g}"
            )
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
# EXAMPLES

if __name__ == "__main__":
    # A) Standard mode (match ligand, DMSO, and protein targets)
    V_final=300.0              # µL
    C_ligand_stock=100000.0    # µM  (100 mM)
    DMSO_stock_pct=1.0         # 100% DMSO
    C_ligand_target=10.0       # µM
    DMSO_target_pct=0.02       # 2% v/v
    C_protein_stock=150.0      # µM
    C_protein_target=145.0     # µM

    example_std = calc_volumes_for_sample(
        V_final, C_ligand_stock, DMSO_stock_pct,
        C_ligand_target, DMSO_target_pct,
        C_protein_stock, C_protein_target
    )
    print("\nStandard mode — Volumes to add (µL)")
    for k, v in example_std.items():
        print(f"{k:<15} : {v:9.3f}")

    # B) Protein-agnostic mode (ignore protein target; no buffer; fill remainder with protein)
    V_final=300.0
    C_ligand_stock=100000.0
    DMSO_stock_pct=1.0
    C_ligand_target=10.0
    DMSO_target_pct=0.02
    C_protein_stock=150.0
    C_protein_target=None      # <-- activate protein-agnostic mode (None or 0)

    example_agnostic = calc_volumes_for_sample(
        V_final, C_ligand_stock, DMSO_stock_pct,
        C_ligand_target, DMSO_target_pct,
        C_protein_stock, C_protein_target
    )
    print("\nProtein-agnostic mode — Volumes to add (µL)")
    for k, v in example_agnostic.items():
        print(f"{k:<15} : {v:9.3f}")
