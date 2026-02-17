---
title: "Protein NMR workflow"
layout: default
---

### Tips for Resonance Assignment

**Preparation:**
- Print molecular structures of all 20 amino acids for reference.

**Strategies for Identifying Spin Systems:**
- Start assignments with unique or easily identifiable spin systems like Glycine, Alanine, Threonine, and Valine.
- Identify Asp by its 2 HB at ~2.7 ppm.
- Recognize Proline by the absence of HN in the TOCSY fingerprint region and strong NOEs from Pro-Hδ to the Hα proton of the preceding residue due to the trans conformation of the X-Pro peptide bond.

**Assignment Techniques:**
- Combine sequential assignment (Wuthrich method) with the MCD approach. Start with TOCSY fingerprints, proceed to identify the NAB unit, then link them using NOESY data.
- Look for characteristic NOEs indicative of regular secondary structures.

**Handling Overlapping Peaks:**
- To clarify overlapping peaks (e.g., HN and CA), integrate the peak of a known HN in 1D. If the volume doubles, this indicates overlapping peaks.

**Discriminating False Peaks:**
- Distinguish false amino acid peaks in 1D by their singlet separation and in 2D by absence of NOE peaks vertically aligned with their HN peak.

**Extending Assignments When Stuck:**
- If assignments stall, begin with NOEs between HAi and HNi+1. If necessary, continue with HNi and HNi+1 NOEs, then HBi and HNi+1 NOEs.

### Procedure Outline

**Spectral Overlay and Integration:**
- Overlay TOCSY and NOESY spectra in Sparky, and TOCSY with 1D proton spectra in Topspin. Refer to [TOCSY patterns here](http://www.bp.uni-bayreuth.de/NMR/nmr_alltocsy.html).
- Integrate a confirmed single HN peak in 1D, then other peaks to determine their multiplicity (singlets, doublets, etc.).
- Mark and identify as many HN peaks as possible using integrals from 1D and the overlaid 1D+2D TOCSY spectra.

> **Note:** Ignore peaks exactly below HA peaks around 4.8 ppm as correspond to water absorption - ignore them!
{: .admonition .note}

**Peak Assignments**
- Assign as many H?-HN, H?-HA, H?-HB, etc., peaks as possible. Note that the first residue's HN does not appear in the spectrum; the second residue's HN is the most leftward.
- Use the HA(i)-HN(i+1) NOEs to assign as many peaks as you can to atoms/residues. Sparky identifies the closest atom resonance when you try to add labels.
- Use the HN(i)-HN(i+1) NOEs to assign as many peaks as you can to atoms/residues. Sparky identifies the closest atom resonance when you try to add labels.

> **Note:** Strong HN(i)-HN(i+1) NOEs are characteristic of alpha- and 3/10-helical structures (~2.8 A, ~2.6 A) and turn I (~2.6 A).
{: .admonition .note}

- Use the HB(i)-HN(i+1) NOEs to assign as many peaks as you can to atoms/residues. Sparky identifies the closest atom resonance when you try to add labels.
- Use the rest of the NOEs to assign as many more atoms as you can. Sparky identifies the closest atom resonance when you try to add labels.
- Find the HE of Arg, Gln, Asn, Lys, His,Trp
- Search for alpha- or 3/10 helices by identifyings strong HN(i)-HN(i+1) (~2.8 A, ~2.6 A) and HA(i)-HN(i+3) NOES (~3.5 A), HA(i)-HB(i+3).
