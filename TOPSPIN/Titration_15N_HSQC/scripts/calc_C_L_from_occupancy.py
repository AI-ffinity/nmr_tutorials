#!/usr/bin/env python

import numpy as np

def ligand_conc_for_occupancy(occupancy: float, Kd: float, cp: float) -> float:
    """
    Return the *ligand concentration* [L] (same units as *cp* and *Kd*)
    required to reach a desired fractional occupancy
        q = [PL]/c_p    (0 < q ≤ 1)
    for a 1:1 binding equilibrium with dissociation constant *Kd*.

    Analytic inversion of

        q = 2 / ( 1 + ((Kd/cp)+1)/x + sqrt((1+((Kd/cp)+1)/x)**2 - 4/x) )
        where x = [L]/c_p,

    gives

        x = q * (q - 1 - Kd/cp) / (q - 1)         (for q ≠ 1)
        [L] = x * c_p

    Parameters
    ----------
    occupancy : float
        Target fraction of bound protein (0 < occupancy ≤ 1).
    Kd : float
        Dissociation constant (same concentration units as *cp*).
    cp : float
        Total protein concentration (> 0).

    Returns
    -------
    L : float
        Ligand concentration required to achieve the given occupancy.
        Returns np.inf if occupancy == 1 (requires infinite ligand excess).

    Raises
    ------
    ValueError
        If *occupancy* is outside (0, 1] or *cp* ≤ 0.
    """
    if cp <= 0:
        raise ValueError(f"Total protein concentration cp must be > 0 (got cp={cp}).")
    if not (0.0 < occupancy <= 1.0):
        raise ValueError(f"Occupancy must be in (0, 1], got occupancy={occupancy}.")

    # 100 % occupancy → asymptotically infinite ligand concentration
    if np.isclose(occupancy, 1.0):
        return np.inf

    beta = (Kd / cp) + 1.0                             # shorthand
    x = occupancy * (occupancy - beta) / (occupancy - 1.0)  # [L]/c_p
    return x * cp                                      # absolute [L]


cp = 120           # µM total protein
Kd = 291          # µM dissociation constant

for qd in np.arange(0.3, 0.9, 0.05): # [0.3, 0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9]:	# desired occupancy
    qd = round(qd, 2)
    ligand_needed = ligand_conc_for_occupancy(qd, Kd, cp)
    print(f"occupancy {qd} -> Ligand concentration required: {ligand_needed:.2f} µM")

