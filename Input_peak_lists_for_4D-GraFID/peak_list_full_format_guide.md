---
title: "peak list full format guide"
layout: default
---

# Submitting peak lists for 4D-GraFID

## Experiment type reference

4D-GraFID accepts the following experiments and expects that they match the definitions in the table below. 

### Backbone assignments

>  ![Warning]
>  Differentiation between backbone and side chain peaks in the **3D** experiments is currently not supported by 4D-GraFID; please, remove any known sidechain peaks from the peak lists. 



| Name     | Example Bruker pulse sequence | Expected resonances                                          | Intensity                               |
| -------- | ----------------------------- | ------------------------------------------------------------ | --------------------------------------- |
| NH-HSQC  | `hsqcetf3gpsi`                | **Backbone amides:** `H`, `N` <br />**Sidechain amides:** **Asn** `HD21/ND2`, `HD22/ND2`; **Gln** `HE21/NE2`, `HE22/NE2`; **Trp** `HE1/NE1` | BB positive, SC negative                |
| HNCACB   | `hncacbgp3d`                  | `H`/`N`/`CA` and `H/N/CB`                                    | CA positive, CB negative;               |
| CBCAcoNH | `cbcaconhgp3d`                | **Backbone** `H/N/CA(i−1)` and `H/N/CB(i−1)`; <br />**Sidechains**: **Asn** `HD[1,2]/ND/CB`; **Gln** `HE[1,2]/NE/CG` | CB positive or negative (lower than CA) |
| HNCA     | `hncagp3d`                    | `H/N/CA` `(i, i-1)`                                          | same sign                               |
| HNcoCA   | `hncocagp3d`                  | `H/N/CA(i−1)`                                                | same sign                               |
| HNcaCO   | `hncacogp3d`                  | `H/N/CO` `(i, i-1)`                                          | same sign                               |
| HNCO     | `hncogp3d`                    | **Backbone**: `H/N/CO(i−1)`; <br />**Sidechains:** **Asn** `HD2[1,2]/ND2/CG`; **Gln** `HE2[1,2]/NE2/CD` | same sign                               |

### Side chain assignments & structure

> ![Info]
> Coming soon to 4D-GraFID

| Name             | Example Bruker pulse sequence | Expected atoms                                     | Intensity            |
| ---------------- | ----------------------------- | -------------------------------------------------- | -------------------- |
| CH-HSQC          | `hsqcedetgp`                  | Any H/C                                            | negative for `-CH2-` |
| CH-HSQC-CT       | `hsqcctetgp`                  | Any H/C                                            | same sign            |
| 13C-edited NOESY | `noesyhsqcf3gpwg3d`           | Any H to any H/C                                   | Defined by NOE       |
| 15N-edited NOESY | `noesyhsqcf3gpwg3d`           | Any H to any amide                                 | Defined by NOE       |
| HCCH-NOESY       | `hsqcnoesyhsqcccgp4`          | Any H/C to any H/C; mostly of **i** and **i±1**    | Defined by NOE       |
| HCNH-NOESY       | `hsqcnoesyhsqccngp4d`         | BB+SC amides / BB+SC ; mostly of **i** and **i±1** | Defined by NOE       |

## Requirements on sets of spectra

Only **pairs** of complementary spectra are supported:

* HNCACB & CBCAcoNH
* HNCA & HNcoCA
* HNcaCO & HNCO

Non-paired experiments **will not be considered**

## User assignments reference

> ![NOTE]
> Currently *(as of 16. Feb 2026)*, only assignments of 15N-HSQC are considered. 

The assignment must match the format: `<1-letter RESTYPE><RESNUM><ATOM-w1>-<ATOM-w2>`.

User-provided assignments are used only for comparison with the assignments by 4D-GraFID. **Duplicated assignments are excluded from the statistics completely!**
