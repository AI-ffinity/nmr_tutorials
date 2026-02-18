---
title: "4D-GraFID input data format guide"
layout: default
---

# Submitting NMR peak lists for 4D-GraFID

1. Upload your peak lists via the upload interface's left panel. Currently, we only support peak lists in NMRFAM SPARKY / POKY format; files must have the `.list` extension.
2. Select the experiment type.

The dimensions of the peak lists will be automatically inferred based on the distribution of chemical shift values.

<div class="video-container">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/ljX-bOdQsjU?si=yWYThM2b4LpYtd7N" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

[Watch this video on YouTube](https://www.youtube.com/watch?v=ljX-bOdQsjU)


## Example peak lists
The following peak lists are from a small protein (**1YEZ**) from the **ARTINA benchmark set**:

* [2D NH-HSQC](https://raw.githubusercontent.com/AI-ffinity/ARTINA_benchmark_set/blob/FULL_DATASET/1YEZ/input_files/1YEZ_HSQC_hsqcedetf3gpsi2.list.curated)
* [3D HNCACB](https://raw.githubusercontent.com/AI-ffinity/ARTINA_benchmark_set/blob/FULL_DATASET/1YEZ/input_files/1YEZ_HNCACB.list.curated)
* [4D HCNH-NOESY](https://raw.githubusercontent.com/AI-ffinity/ARTINA_benchmark_set/blob/FULL_DATASET/1YEZ/input_files/1YEZ_HCNH.list.curated)


## Experiment type reference

4D-GraFID accepts the following experiments and expects that they match the definitions in the table below. 

### Backbone assignments

> **Warning:** Differentiation between backbone and side chain peaks in the **3D** experiments is currently not supported by 4D-GraFID; please, remove any known sidechain peaks from the peak lists.
{: .admonition .warning}



| Name     | Example Bruker pulse sequence | Expected resonances                                          | Intensity                               |
| -------- | ----------------------------- | ------------------------------------------------------------ | --------------------------------------- |
| NH-HSQC  | `hsqcetf3gpsi`                | **Backbone amides:** `H`, `N` <br />**Sidechain amides:** **Asn** `HD21/ND2`, `HD22/ND2`; **Gln** `HE21/NE2`, `HE22/NE2`; **Trp** `HE1/NE1` | BB positive, SC negative                |
| HNCACB   | `hncacbgp3d`                  | `H`/`N`/`CA` and `H/N/CB`                                    | CA positive, CB negative;               |
| CBCAcoNH | `cbcaconhgp3d`                | **Backbone** `H/N/CA(i−1)` and `H/N/CB(i−1)`; <br />**Sidechains**: **Asn** `HD[1,2]/ND/CB`; **Gln** `HE[1,2]/NE/CG` | CB positive or negative (lower than CA) |
| HNCA     | `hncagp3d`                    | `H/N/CA` `(i, i-1)`                                          | same sign                               |
| HNcoCA   | `hncocagp3d`                  | `H/N/CA(i−1)`                                                | same sign                               |
| HNcaCO   | `hncacogp3d`                  | `H/N/CO` `(i, i-1)`                                          | same sign                               |
| HNCO     | `hncogp3d`                    | **Backbone**: `H/N/CO(i−1)`; <br />**Sidechains:** **Asn** `HD2[1,2]/ND2/CG`; **Gln** `HE2[1,2]/NE2/CD` | same sign                               |



> **Important:** Only **pairs** of complementary spectra are supported:
> * HNCACB & CBCAcoNH
> * HNCA & HNcoCA
> * HNcaCO & HNCO
> Non-paired experiments **will not be considered**
{: .admonition .important}



### Side chain assignments & structure

> **Coming soon to 4D-GraFID!**
{: .admonition .info}

| Name             | Example Bruker pulse sequence | Expected atoms                                     | Intensity            |
| ---------------- | ----------------------------- | -------------------------------------------------- | -------------------- |
| CH-HSQC          | `hsqcedetgp`                  | Any H/C                                            | negative for `-CH2-` |
| CH-HSQC-CT       | `hsqcctetgp`                  | Any H/C                                            | same sign            |
| 13C-edited NOESY | `noesyhsqcf3gpwg3d`           | Any H to any H/C                                   | Defined by NOE       |
| 15N-edited NOESY | `noesyhsqcf3gpwg3d`           | Any H to any amide                                 | Defined by NOE       |
| HCCH-NOESY       | `hsqcnoesyhsqcccgp4`          | Any H/C to any H/C; mostly of **i** and **i±1**    | Defined by NOE       |
| HCNH-NOESY       | `hsqcnoesyhsqccngp4d`         | BB+SC amides / BB+SC ; mostly of **i** and **i±1** | Defined by NOE       |

## Format reference for user-provided atom assignments

> **Important:** Currently *(as of 16. Feb 2026)*, only assignments of 15N-HSQC are considered.
{: .admonition .important}

The assignment must match the format: `<1-letter RESTYPE><RESNUM><ATOM-w1>-<ATOM-w2>`.

User-provided assignments are used only for comparison with the assignments by 4D-GraFID. **Duplicated assignments are excluded from the statistics completely!**
