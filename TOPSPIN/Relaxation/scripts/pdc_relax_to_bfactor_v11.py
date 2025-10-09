#!/usr/bin/env python3

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    import pandas as pd
    import numpy as np
except Exception as e:  # pragma: no cover
    print("[ERROR] This script needs pandas and numpy. Try: pip install pandas numpy", file=sys.stderr)
    raise

# -------------------- utils --------------------

def die(msg: str, code: int = 2):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(code)


def _smart_float(x: str) -> Optional[float]:
    try:
        return float(x)
    except Exception:
        return None


_RE_SECTION = re.compile(r"^SECTION:\s+results", re.IGNORECASE)
_RE_HEADER_SPLIT = re.compile(r"\s{2,}|\t+")
# Matches "123 ALAN / 123 ALAH" and similar
_RE_PEAK_NAME = re.compile(r"^\s*(\d+)\s*([A-Z]{3})N\s*/\s*(\d+)\s*[A-Z]{3}H", re.IGNORECASE)
# Also support names like "S9N-H", "Y108N-H" (one-letter AA followed by resid)
_RE_PEAK_ONELETTER = re.compile(r"^\s*([A-Z])\s*(\d+)\s*N-?H", re.IGNORECASE)
_AA1TO3 = {
    'A':'ALA','C':'CYS','D':'ASP','E':'GLU','F':'PHE','G':'GLY','H':'HIS','I':'ILE','K':'LYS',
    'L':'LEU','M':'MET','N':'ASN','P':'PRO','Q':'GLN','R':'ARG','S':'SER','T':'THR','V':'VAL',
    'W':'TRP','Y':'TYR'
}



def parse_pdc_results(txt_path: Path) -> "pd.DataFrame":
    """
    Parse 'SECTION: results' from a PDC TXT report.
    Returns columns:
      resid, resname, peak_name, F2_ppm, F3_ppm, T_s, T_err_s, R_rate, R_err, kind ('T1' or 'T2')
    """
    text = Path(txt_path).read_text(errors="ignore")

    # locate results section
    start = None
    lines_full = text.splitlines()
    for i, line in enumerate(lines_full):
        if _RE_SECTION.search(line):
            start = i
            break
    if start is None:
        die(f"Could not find 'SECTION: results' in {txt_path}")

    lines = lines_full[start + 1 :]
    # header
    header_idx = None
    for j, line in enumerate(lines):
        if line.strip():
            header_idx = j
            break
    if header_idx is None:
        die(f"No header after results section in {txt_path}")

    header = _RE_HEADER_SPLIT.split(lines[header_idx].strip())
    rows = []
    for line in lines[header_idx + 1 :]:
        if not line.strip() or line.startswith("SECTION:"):
            break
        parts = _RE_HEADER_SPLIT.split(line.rstrip())
        if len(parts) < len(header):
            parts += [""] * (len(header) - len(parts))
        record = dict(zip(header, parts))

        peak_name = record.get("Peak name", "") or record.get("Peak", "") or record.get("name", "") or parts[0].strip()
        peak_name = peak_name.strip()

        # residue parsing
        resid, resname = (None, None)
        m = _RE_PEAK_NAME.match(peak_name)
        if m:
            resid = int(m.group(1)); resname = m.group(2).upper()
        else:
            # Try one-letter form like "S9N-H" / "Y108N-H"
            m1 = _RE_PEAK_ONELETTER.match(peak_name)
            if m1:
                aa1 = m1.group(1).upper()
                resid = int(m1.group(2))
                resname = _AA1TO3.get(aa1, aa1*3)  # fallback e.g., 'X' -> 'XXX'
            else:
                # Try looser fallback "123 ALA" somewhere in the string
                m2 = re.search(r"(\d+)\s*([A-Z]{3})", peak_name.upper())
                if m2:
                    resid = int(m2.group(1)); resname = m2.group(2)
                else:
                    # Accept patterns like "A110N-H" even if AA letter isn't recognized
                    m3 = re.search(r"([A-Z])\s*(\d+)", peak_name.upper())
                    if m3:
                        resid = int(m3.group(2)); resname = _AA1TO3.get(m3.group(1), m3.group(1)*3)
        # Ensure a non-null residue name for grouping
        if resname is None:
            resname = "UNK"

        F2_ppm = _smart_float(record.get("F2 [ppm]", ""))
        F3_ppm = _smart_float(record.get("F3 [ppm]", ""))

        T_s = None; T_err = None; kind = None
        if "T1 [s]" in record:
            T_s = _smart_float(record.get("T1 [s]", ""))
            T_err = _smart_float(record.get("error", "")) or _smart_float(record.get("sd", ""))
            kind = "T1"
        if "T2 [s]" in record:
            T_s = _smart_float(record.get("T2 [s]", ""))
            T_err = _smart_float(record.get("error", "")) or _smart_float(record.get("sd", ""))
            kind = "T2"

        R_calc = (1.0 / T_s) if (T_s not in (None, 0)) else None
        R_err = (T_err / (T_s**2)) if (T_err is not None and T_s not in (None, 0)) else None

        # fallback to explicit rate columns if present
        R_from_table = None
        for candidate in ["R2 [rad/s]", "R2 [1/s]", "R2 [Hz]", "R1 [rad/s]", "R1 [1/s]"]:
            if candidate in record:
                R_from_table = _smart_float(record[candidate])
                break
        if R_calc is None and R_from_table is not None:
            R_calc = R_from_table
            R_err = None  # no error info available from rate column

        rows.append({
            "resid": resid,
            "resname": resname,
            "peak_name": peak_name,
            "F2_ppm": F2_ppm,
            "F3_ppm": F3_ppm,
            "T_s": T_s,
            "T_err_s": T_err,
            "R_rate": R_calc,
            "R_err": R_err,
            "kind": kind
        })

    df = pd.DataFrame(rows)
    df = df.dropna(subset=["resid"]).copy()
    df["resid"] = df["resid"].astype(int)
    return df


def _group_median_with_err(df: "pd.DataFrame", value_col: str, err_col: str, keys: List[str]) -> "pd.DataFrame":
    """Group by keys and compute median of value and a conservative error estimate (median of per-peak errors)."""
    val = df.groupby(keys, as_index=False)[value_col].median()
    if err_col in df.columns:
        err_med = df.groupby(keys, as_index=False)[err_col].median().rename(columns={err_col: value_col+"_err"})
        out = pd.merge(val, err_med, on=keys, how="left")
    else:
        out = val
        out[value_col+"_err"] = np.nan
    return out


def pick_metric_single_day(df_t1: "pd.DataFrame", df_t2: "pd.DataFrame", prefer_ratio: bool = True) -> "pd.DataFrame":
    """
    Merge per-residue R1 and R2 (and their errors), compute ratio (and its propagated error) if requested.
    Returns: resid, resname, R1, R1_err, R2, R2_err, R2_over_R1, R2_over_R1_err
    """
    # Ensure R and R_err available
    for df in (df_t1, df_t2):
        if df is not None:
            if "R_rate" not in df or df["R_rate"].isna().all():
                df["R_rate"] = pd.to_numeric(df["T_s"], errors="coerce").apply(lambda x: (1.0 / x) if (x and x != 0) else np.nan)
            if "R_err" not in df or df["R_err"].isna().all():
                def _r_err(row):
                    t = row.get("T_s", None); te = row.get("T_err_s", None)
                    if t in (None, 0) or te in (None,):
                        return np.nan
                    try: return te / (t*t)
                    except Exception: return np.nan
                df["R_err"] = df.apply(_r_err, axis=1)

    keys = ["resid", "resname"]
    t1 = _group_median_with_err(df_t1.loc[df_t1["kind"] == "T1"], "R_rate", "R_err", keys) if df_t1 is not None else None
    t2 = _group_median_with_err(df_t2.loc[df_t2["kind"] == "T2"], "R_rate", "R_err", keys) if df_t2 is not None else None

    if t1 is not None and t2 is not None:
        merged = pd.merge(t1.rename(columns={"R_rate": "R1", "R_rate_err": "R1_err"}),
                          t2.rename(columns={"R_rate": "R2", "R_rate_err": "R2_err"}),
                          on=keys, how="outer")
    elif t1 is not None:
        merged = t1.rename(columns={"R_rate": "R1", "R_rate_err": "R1_err"}); merged["R2"] = np.nan; merged["R2_err"] = np.nan
    elif t2 is not None:
        merged = t2.rename(columns={"R_rate": "R2", "R_rate_err": "R2_err"}); merged["R1"] = np.nan; merged["R1_err"] = np.nan
    else:
        die("Neither T1 nor T2 data found")

    # ratio and propagated error
    merged["R2_over_R1"] = pd.to_numeric(merged["R2"], errors="coerce") / pd.to_numeric(merged["R1"], errors="coerce")
    with np.errstate(divide='ignore', invalid='ignore'):
        term1 = (merged["R2_err"] / merged["R2"]) ** 2
        term2 = (merged["R1_err"] / merged["R1"]) ** 2
        merged["R2_over_R1_err"] = np.abs(merged["R2_over_R1"]) * np.sqrt(term1 + term2)

    return merged


def compute_state_score_multi(days_data: Dict[str, "pd.DataFrame"]) -> "pd.DataFrame":
    """
    Multi-day: make wide table of R2_dayX (+ R2err_dayX) and compute state_score.
    state_score = robust z-score (median/MAD) of Theil–Sen slope of R2 vs day index.
    """
    frames = []
    labels = list(days_data.keys())
    for label, df in days_data.items():
        df2 = df.copy()
        if ("R_rate" not in df2) or df2["R_rate"].isna().all():
            df2["R_rate"] = pd.to_numeric(df2["T_s"], errors="coerce").apply(lambda x: (1.0 / x) if (x and x != 0) else np.nan)
        if "R_err" not in df2 or df2["R_err"].isna().all():
            df2["R_err"] = df2.apply(lambda row: (row["T_err_s"] / (row["T_s"]**2)) if (pd.notna(row["T_err_s"]) and pd.notna(row["T_s"]) and row["T_s"]!=0) else np.nan, axis=1)

        keys = ["resid", "resname"]
        r2 = df2.loc[df2["kind"] == "T2"]
        r2v = r2.groupby(keys, as_index=False)["R_rate"].median().rename(columns={"R_rate": f"R2_{label}"})
        r2e = r2.groupby(keys, as_index=False)["R_err"].median().rename(columns={"R_err": f"R2err_{label}"})
        frames.append(pd.merge(r2v, r2e, on=keys, how="outer"))

    if not frames:
        die("No T2 data across days to compute multi-day state score")

    from functools import reduce
    wide = reduce(lambda a, b: pd.merge(a, b, on=["resid", "resname"], how="outer"), frames)
    wide = wide.sort_values(["resid", "resname"]).reset_index(drop=True)

    # prepare Theil–Sen slope
    xs = np.arange(len(labels), dtype=float)

    def theil_sen(values: List[float]) -> float:
        arr = np.array(values, dtype=float)
        mask = np.isfinite(arr)
        arr = arr[mask]; xs2 = xs[mask]
        if arr.size < 2:
            return np.nan
        slopes = []
        for i in range(arr.size):
            for j in range(i + 1, arr.size):
                if xs2[j] != xs2[i] and np.isfinite(arr[i]) and np.isfinite(arr[j]):
                    slopes.append((arr[j] - arr[i]) / (xs2[j] - xs2[i]))
        return float(np.median(slopes)) if slopes else np.nan

    ycols = [c for c in wide.columns if c.startswith("R2_") and not c.startswith("R2err_")]
    wide["R2_slope"] = wide[ycols].apply(lambda row: theil_sen([row[c] for c in ycols]), axis=1)

    med = np.nanmedian(wide["R2_slope"].values)
    mad = np.nanmedian(np.abs(wide["R2_slope"].values - med))
    if not np.isfinite(mad) or mad == 0:
        zrobust = (wide["R2_slope"].values - med)
    else:
        zrobust = (wide["R2_slope"].values - med) / (1.4826 * mad)
    wide["state_score"] = zrobust
    return wide

# -------------------- normalization & IO --------------------

def normalize_series(vals: "pd.Series", mode: str, out_min: float, out_max: float,
                     clip_low_pct: float = 0.0, clip_high_pct: float = 100.0) -> "pd.Series":
    """Robust normalization on finite values; safe fallback when range collapses."""
    if mode == "none":
        return pd.to_numeric(vals, errors="coerce")

    x = pd.to_numeric(vals, errors="coerce").astype(float)
    mask = np.isfinite(x.values)
    if mask.sum() == 0:
        return pd.Series(np.full(len(x), (out_min + out_max) / 2.0), index=vals.index, dtype=float)

    xa = x.values[mask]

    if mode == "minmax":
        lo = np.nanpercentile(xa, clip_low_pct) if clip_low_pct is not None else np.nanmin(xa)
        hi = np.nanpercentile(xa, clip_high_pct) if clip_high_pct is not None else np.nanmax(xa)
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            lo, hi = np.nanmin(xa), np.nanmax(xa)
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            return pd.Series(np.full(len(x), (out_min + out_max) / 2.0), index=vals.index, dtype=float)

        x_clipped = x.copy().values
        x_clipped[mask] = np.clip(xa, lo, hi)
        scaled = (x_clipped - lo) / (hi - lo)
        out = out_min + scaled * (out_max - out_min)
        return pd.Series(out, index=vals.index, dtype=float)

    if mode == "zscore":
        mu = np.nanmean(xa); sd = np.nanstd(xa)
        if not np.isfinite(sd) or sd == 0:
            z = np.zeros_like(x.values, dtype=float)
        else:
            z = (x.values - mu) / sd
        z = np.clip(z, -3.0, 3.0)
        out = out_min + (z + 3.0) * (out_max - out_min) / 6.0
        return pd.Series(out, index=vals.index, dtype=float)

    return pd.to_numeric(vals, errors="coerce")


def write_bvalues_txt(path: Path, resids, bvals, metric_name: str, raw_vals=None):
    """Write a tab-separated file: resid  B_written  metric  raw_metric"""
    lines = ["resid\tB_written\tmetric\traw_metric"]
    raw_vals = raw_vals if raw_vals is not None else bvals
    for r, b, raw in zip(resids, bvals, raw_vals):
        if r is None:
            continue
        try:
            r_i = int(r)
        except Exception:
            continue
        try:
            b_out = float(b)
            if not math.isfinite(b_out):
                b_out = 0.0
        except Exception:
            b_out = 0.0
        raw_out = ""
        try:
            raw_f = float(raw)
            if math.isfinite(raw_f):
                raw_out = f"{raw_f:.6g}"
        except Exception:
            raw_out = ""
        lines.append(f"{r_i}\t{b_out:.6g}\t{metric_name}\t{raw_out}")
    Path(path).write_text("\n".join(lines) + "\n")


def write_pdb_with_bfactors(pdb_in: Path, pdb_out: Path, resid2b: Dict[int, float]) -> Tuple[float, float]:
    min_b, max_b = float("inf"), float("-inf")
    out_lines = []
    with open(pdb_in, "r", errors="ignore") as fh:
        for line in fh:
            if line.startswith(("ATOM  ", "HETATM")):
                try:
                    resid = int(line[22:26].strip())
                except Exception:
                    out_lines.append(line); continue
                bval = resid2b.get(resid, None)
                if bval is not None and math.isfinite(bval):
                    min_b = min(min_b, bval); max_b = max(max_b, bval)
                    out_lines.append(f"{line[:60]}{bval:6.2f}{line[66:]}")
                else:
                    out_lines.append(line)
            else:
                out_lines.append(line)
    with open(pdb_out, "w") as oh:
        oh.writelines(out_lines)
    if min_b == float("inf"):
        min_b, max_b = (0.0, 0.0)
    return min_b, max_b


def emit_pymol_script_apply_btxt(out_pml: Path, pdb_to_load: str, btxt_name: str, object_name: str = "prot",
                                 spectrum_min: Optional[float] = None, spectrum_max: Optional[float] = None,
                                 b_column: str = "B_written", palette: str = "blue_white_red"):
    """
    Write a PyMOL .pml that loads the PDB, applies B from TXT (B_written or raw_metric), colors & putty.
    """
    min_line = f", minimum={spectrum_min:.2f}" if spectrum_min is not None else ""
    max_line = f", maximum={spectrum_max:.2f}" if spectrum_max is not None else ""
    pml = f"""# Auto-generated: apply {{b_column}} from TXT and visualize
load {pdb_to_load}, {object_name}

# Apply B-factors from tab file: resid  B_written  metric  raw_metric
python
import csv, math
obj = "{object_name}"
bcol = "{b_column}"
bmap = {{}}
with open("{btxt_name}") as fh:
    rd = csv.DictReader(fh, delimiter='\\t')
    for row in rd:
        try:
            resid = int(row['resid'])
            val = row.get(bcol, '')
            if val is None or val=='':
                continue
            b = float(val)
            if not math.isfinite(b):
                continue
            bmap[resid] = b
        except Exception:
            pass
for resid, b in bmap.items():
    cmd.alter(f"{{obj}} and resi {{resid}}".format(obj=obj, resid=resid), f"b={{b}}".format(b=b))
cmd.rebuild()
python end

# Color & putty
hide everything, {object_name}
show cartoon, {object_name}
spectrum b, {palette}, {object_name}{min_line}{max_line}
cartoon putty, {object_name}
"""
    Path(out_pml).write_text(pml)


# ---------- plotting helpers ----------

def _resid_axis_from_pdb(pdb_path: Path) -> List[int]:
    """Return sorted unique residue numbers from the PDB (backbone ATOM lines)."""
    resids = []
    try:
        with open(pdb_path, "r", errors="ignore") as fh:
            for line in fh:
                if line.startswith(("ATOM  ", "HETATM")):
                    try:
                        resids.append(int(line[22:26].strip()))
                    except Exception:
                        pass
    except Exception:
        return []
    resids = sorted(set(resids))
    return resids


def _make_full_axis_from_data_or_pdb(data_resids: List[int], pdb_path: Path, chunk_size: int = 50) -> List[List[int]]:
    """Build a full residue axis from PDB if available; otherwise use min..max of the observed resids.
       Return a list of chunks (each a list of residue numbers)."""
    pdb_resids = _resid_axis_from_pdb(pdb_path)
    if pdb_resids:
        full = pdb_resids
    else:
        if not data_resids:
            return []
        full = list(range(min(data_resids), max(data_resids) + 1))
    chunks = [full[i:i+chunk_size] for i in range(0, len(full), chunk_size)]
    return chunks


def _compute_global_ylim_for_series(series_df: "pd.DataFrame", value_col: str) -> Tuple[float, float]:
    """Compute global y-limits across all residues for a given series (include error bars if available)."""
    vals = pd.to_numeric(series_df[value_col], errors="coerce").astype(float).values
    err_col = value_col + "_err"
    errs = pd.to_numeric(series_df[err_col], errors="coerce").astype(float).values if err_col in series_df.columns else None

    if errs is not None:
        y_low = vals - errs
        y_high = vals + errs
    else:
        y_low = vals
        y_high = vals

    y_low = y_low[np.isfinite(y_low)]
    y_high = y_high[np.isfinite(y_high)]
    if y_low.size == 0 or y_high.size == 0:
        return (0.0, 1.0)

    ymin = float(np.nanmin(y_low))
    ymax = float(np.nanmax(y_high))
    if not np.isfinite(ymin) or not np.isfinite(ymax) or ymax <= ymin:
        ymin, ymax = 0.0, 1.0

    # R2 and ratios are non-negative typically; clamp floor at 0 if everything above 0
    if ymin > 0:
        ymin = 0.0
    # small padding
    pad = 0.05 * (ymax - ymin) if ymax > ymin else 0.5
    return (ymin - pad*0.2, ymax + pad)


def plot_bar_chunks(series_df: "pd.DataFrame", value_col: str, out_prefix: Path,
                    pdb_path: Path, ylabel: str = "", title_prefix: str = "",
                    chunk_size: int = 50):
    """Plot a single bar (optionally with yerr if present) for a metric over the *full* residue axis in 50-res chunks.
       Missing residues appear as tick labels with no bar (NaN). **All chunks share the same y-axis.**"""
    try:
        import matplotlib.pyplot as plt
        import numpy as _np
    except Exception:
        print("[WARN] matplotlib not installed; skipping plot export")
        return

    resids_present = series_df["resid"].astype(int).tolist()
    chunks = _make_full_axis_from_data_or_pdb(resids_present, pdb_path, chunk_size=chunk_size)
    if not chunks:
        print("[WARN] No residues to plot in chunks")
        return

    # global y-limits for this metric
    y_global_min, y_global_max = _compute_global_ylim_for_series(series_df, value_col)

    # make lookup
    val_map = {int(r): v for r, v in zip(series_df["resid"], pd.to_numeric(series_df[value_col], errors="coerce"))}
    err_col = value_col + "_err" if (value_col + "_err") in series_df.columns else None
    err_map = {int(r): e for r, e in zip(series_df["resid"], pd.to_numeric(series_df[err_col], errors="coerce"))} if err_col else {}

    for idx, chunk in enumerate(chunks, 1):
        xs = _np.arange(len(chunk))
        y = _np.array([val_map.get(r, _np.nan) for r in chunk], dtype=float)
        yerr = _np.array([err_map.get(r, _np.nan) for r in chunk], dtype=float) if err_col else None

        plt.figure(figsize=(14, 4))
        if yerr is not None:
            plt.bar(xs, y, yerr=yerr, capsize=2)
        else:
            plt.bar(xs, y)
        plt.xticks(xs, chunk, rotation=90)
        plt.xlabel("Residue")
        plt.ylabel(ylabel if ylabel else value_col)
        if title_prefix:
            plt.title(f"{title_prefix}: residues {chunk[0]}–{chunk[-1]}")
        else:
            plt.title(f"{value_col} by residue: residues {chunk[0]}–{chunk[-1]}")
        plt.ylim(y_global_min, y_global_max)
        plt.tight_layout()
        plt.savefig(out_prefix.with_suffix(f".{value_col}_chunk{idx:02d}.png"))
        plt.close()


def plot_multi_R2_by_day_chunks(wide_df: "pd.DataFrame", out_prefix: Path, labels: List[str],
                                pdb_path: Path, chunk_size: int = 50):
    """Chunked multi‑bar plot for R2 by day with error bars. **All chunks share the same y-axis.**"""
    try:
        import matplotlib.pyplot as plt
        import numpy as _np
    except Exception:
        print("[WARN] matplotlib not installed; skipping plot export")
        return

    # figure axis
    resids_present = wide_df["resid"].astype(int).tolist()
    chunks = _make_full_axis_from_data_or_pdb(resids_present, pdb_path, chunk_size=chunk_size)
    if not chunks:
        print("[WARN] No residues to plot in chunks")
        return

    ycols = [f"R2_{lb}" for lb in labels if f"R2_{lb}" in wide_df.columns]
    ecols = [f"R2err_{lb}" for lb in labels if f"R2err_{lb}" in wide_df.columns]

    # Compute global y-limits across all days (include error bars)
    y_min_list, y_max_list = [], []
    for i, col in enumerate(ycols):
        vals = pd.to_numeric(wide_df[col], errors="coerce").astype(float).values
        errs = pd.to_numeric(wide_df[ecols[i]], errors="coerce").astype(float).values if i < len(ecols) else None
        low = vals - errs if errs is not None else vals
        high = vals + errs if errs is not None else vals
        low = low[np.isfinite(low)]; high = high[np.isfinite(high)]
        if low.size:
            y_min_list.append(np.nanmin(low))
            y_max_list.append(np.nanmax(high))
    if y_min_list and y_max_list:
        ymin = float(np.nanmin(y_min_list))
        ymax = float(np.nanmax(y_max_list))
    else:
        ymin, ymax = 0.0, 1.0
    if ymin > 0:
        ymin = 0.0
    pad = 0.05 * (ymax - ymin) if ymax > ymin else 0.5
    ymin, ymax = (ymin - pad*0.2, ymax + pad)

    # Make lookups per day
    lookups = []
    for i, col in enumerate(ycols):
        val_map = {int(r): v for r, v in zip(wide_df["resid"], pd.to_numeric(wide_df[col], errors="coerce"))}
        err_map = {int(r): v for r, v in zip(wide_df["resid"], pd.to_numeric(wide_df[ecols[i]], errors="coerce"))} if i < len(ecols) else {}
        lookups.append((val_map, err_map, col))

    for idx, chunk in enumerate(chunks, 1):
        plt.figure(figsize=(14, 6))
        n = len(ycols)
        width = 0.8 / n if n > 0 else 0.6
        xs = np.arange(len(chunk))
        for k, (vmap, emap, col) in enumerate(lookups):
            y = np.array([vmap.get(r, np.nan) for r in chunk], dtype=float)
            e = np.array([emap.get(r, np.nan) for r in chunk], dtype=float) if emap else None
            plt.bar(xs + (k - (n-1)/2) * width, y, width=width, yerr=e, capsize=2, label=col)
        plt.xticks(xs, chunk, rotation=90)
        plt.xlabel("Residue"); plt.ylabel("R2 (1/s)")
        plt.title(f"R2 by residue and day (± error): residues {chunk[0]}–{chunk[-1]}")
        plt.ylim(ymin, ymax)
        plt.legend(); plt.tight_layout()
        plt.savefig(out_prefix.with_suffix(f".R2_by_day.chunk{idx:02d}.png")); plt.close()

# -------------------- main --------------------

def main():
    ap = argparse.ArgumentParser(
        description="Convert Bruker PDC T1/T2 reports into a B‑factor TXT table (± plots with error bars; optional PDB/PyMOL)."
    )
    ap.add_argument("--t1", nargs="+", default=[], help="T1 report TXT(s). One per day, in order.")
    ap.add_argument("--t2", nargs="+", default=[], help="T2 report TXT(s). One per day, in order.")
    ap.add_argument("--labels", nargs="+", help="Optional labels for days (defaults: day1, day2, ...)")
    ap.add_argument("--pdb-in", required=True, help="Template PDB with residue numbers matching the reports.")
    ap.add_argument("--out-prefix", required=True, help="Output prefix.")
    ap.add_argument("--metric", choices=["auto","r2_over_r1","r2","state_score"], default="auto",
                    help="Single-day: R2/R1 or R2. Multi-day: state_score (R2 trend) unless overridden.")
    ap.add_argument("--bf-norm", choices=["none","minmax","zscore"], default="none",
                    help="Normalize values before exporting to B.")
    ap.add_argument("--norm-range", nargs=2, type=float, default=[10.0,80.0],
                    help="Range used for normalization (e.g., 10 80).")
    ap.add_argument("--clip-percentiles", nargs=2, type=float, default=[0.0,100.0],
                    help="Percentile clip before normalization, e.g. 5 95.")
    ap.add_argument("--save-plots", action="store_true", help="Also dump summary PNG plots with error bars.")
    ap.add_argument("--no-pdb", action="store_true", help="Do not write a PDB; rely on TXT + PyMOL loader.")
    ap.add_argument("--emit-pml", action="store_true", help="Emit a helper .pml that applies TXT B-values in PyMOL.")
    ap.add_argument("--pml-column", choices=["B_written","raw_metric"], default="B_written",
                    help="Which column the emitted .pml should apply in PyMOL.")
    ap.add_argument("--palette", default="blue_white_red", help="PyMOL palette name for the emitted .pml.")
    args = ap.parse_args()

    if not args.t1 and not args.t2:
        die("Provide at least one T1 or T2 TXT via --t1/--t2")
    if args.t1 and args.t2 and len(args.t1) != len(args.t2):
        print("[WARN] Different counts of T1 and T2; will use whatever exists per day.", file=sys.stderr)

    n_days = max(len(args.t1), len(args.t2))
    labels = args.labels if args.labels else [f"day{i+1}" for i in range(n_days)]
    out_prefix = Path(args.out_prefix)
    pdb_in = Path(args.pdb_in)
    if not pdb_in.exists():
        print(f"[WARN] PDB not found: {pdb_in}. Proceeding (plots will use data-derived residue axis; PDB export disabled)", file=sys.stderr)
        args.no_pdb = True

    # -------- single-day --------
    if n_days <= 1:
        df_t1 = parse_pdc_results(Path(args.t1[0])) if args.t1 else None
        df_t2 = parse_pdc_results(Path(args.t2[0])) if args.t2 else None
        merged = pick_metric_single_day(df_t1, df_t2, prefer_ratio=(args.metric in ("auto","r2_over_r1")))

        # choose metric series
        if args.metric in ("auto","r2_over_r1"):
            metric_name = "R2_over_R1"; vals = merged["R2_over_R1"]; errs = merged["R2_over_R1_err"]
            if pd.isna(vals).all():
                print("[WARN] R2/R1 not available; using R2", file=sys.stderr)
                metric_name = "R2"; vals = merged["R2"]; errs = merged["R2_err"]
        elif args.metric == "r2":
            metric_name = "R2"; vals = merged["R2"]; errs = merged["R2_err"]
        else:
            metric_name = "R2_over_R1"; vals = merged["R2_over_R1"]; errs = merged["R2_over_R1_err"]

        # normalize for B-writing
        bvals = normalize_series(vals, args.bf_norm, args.norm_range[0], args.norm_range[1],
                                 args.clip_percentiles[0], args.clip_percentiles[1])

        # CSV and TXT
        df_out = merged[["resid","resname"]].copy()
        df_out[metric_name] = pd.to_numeric(vals, errors="coerce")
        df_out[metric_name+"_err"] = pd.to_numeric(errs, errors="coerce")
        df_out["B_written"] = pd.to_numeric(bvals, errors="coerce")
        df_out.to_csv(out_prefix.with_suffix(".metrics.csv"), index=False)

        btxt = out_prefix.with_suffix(".bvals.txt")
        write_bvalues_txt(btxt, df_out["resid"].tolist(), df_out["B_written"].tolist(),
                          metric_name, raw_vals=df_out[metric_name].tolist())
        print(f"[OK] Wrote B-table: {btxt.name}")

        # optional PDB
        pdb_to_load = pdb_in.name
        if not args.no_pdb:
            resid2b = {int(r): (float(b) if (isinstance(b,float) or isinstance(b,int)) and math.isfinite(float(b)) else 0.0)
                       for r, b in zip(df_out["resid"].tolist(), df_out["B_written"].tolist())}
            pdb_out = out_prefix.with_suffix(".pdb")
            bmin, bmax = write_pdb_with_bfactors(pdb_in, pdb_out, resid2b)
            print(f"[OK] Wrote PDB: {pdb_out.name}  (range {bmin:.2f}..{bmax:.2f})")
            pdb_to_load = pdb_out.name

        if args.emit_pml:
            smin = args.norm_range[0] if args.pml_column == "B_written" and args.bf_norm != "none" else None
            smax = args.norm_range[1] if args.pml_column == "B_written" and args.bf_norm != "none" else None
            pml_path = out_prefix.with_suffix(".apply_b_from_txt.pml")
            emit_pymol_script_apply_btxt(pml_path, pdb_to_load, btxt.name,
                                         b_column=args.pml_column, palette=args.palette,
                                         spectrum_min=smin, spectrum_max=smax)
            print(f"[OK] Wrote PyMOL loader: {pml_path.name}")

        if args.save_plots:
            plot_bar_chunks(df_out, metric_name, out_prefix, pdb_in,
                            ylabel=metric_name, title_prefix=metric_name + " per residue (± error)", chunk_size=50)

        return

    # -------- multi-day --------
    # Parse day-wise
    days_data: Dict[str, pd.DataFrame] = {}
    for i in range(n_days):
        t1 = parse_pdc_results(Path(args.t1[i])) if i < len(args.t1) else None
        t2 = parse_pdc_results(Path(args.t2[i])) if i < len(args.t2) else None
        if t1 is None and t2 is None:
            continue
        df_d = pd.concat([x for x in (t1, t2) if x is not None], ignore_index=True)
        if "kind" not in df_d.columns:
            df_d["kind"] = np.where(pd.notna(df_d.get("T2 [s]", np.nan)), "T2", "T1")
        days_data[labels[i]] = df_d

    if not days_data:
        die("No data found for any day")

    wide = compute_state_score_multi(days_data)

    # choose metric for B
    if args.metric in ("auto","state_score"):
        metric_name = "state_score"
        chosen_metric = wide[metric_name]
    elif args.metric == "r2":
        r2cols = [c for c in wide.columns if c.startswith("R2_") and not c.startswith("R2err_")]
        metric_name = "R2_mean"
        chosen_metric = wide[r2cols].astype(float).mean(axis=1, skipna=True)
        wide[metric_name] = chosen_metric
    elif args.metric == "r2_over_r1":
        die("Multi-day R2/R1 is not computed across days. Use --metric state_score (default) or --metric r2.")
    else:
        metric_name = "state_score"; chosen_metric = wide["state_score"]

    # normalize & write outputs
    bvals = normalize_series(chosen_metric, args.bf_norm, args.norm_range[0], args.norm_range[1],
                             args.clip_percentiles[0], args.clip_percentiles[1])
    wide["B_written"] = pd.to_numeric(bvals, errors="coerce")

    wide_out = wide[["resid"] + [c for c in wide.columns if c != "resid"]].copy()
    wide_out.to_csv(out_prefix.with_suffix(".multi.csv"), index=False)

    btxt = out_prefix.with_suffix(".bvals.txt")
    write_bvalues_txt(btxt, wide["resid"].tolist(), wide["B_written"].tolist(),
                      metric_name, raw_vals=chosen_metric.tolist())
    print(f"[OK] Wrote B-table: {btxt.name}")

    # optional PDB
    pdb_to_load = pdb_in.name
    if not args.no_pdb:
        resid2b = {int(r): (float(b) if (isinstance(b,float) or isinstance(b,int)) and math.isfinite(float(b)) else 0.0)
                   for r, b in zip(wide["resid"].tolist(), wide["B_written"].tolist())}
        pdb_out = out_prefix.with_suffix(".pdb")
        bmin, bmax = write_pdb_with_bfactors(pdb_in, pdb_out, resid2b)
        print(f"[OK] Wrote PDB: {pdb_out.name}  (range {bmin:.2f}..{bmax:.2f})")
        pdb_to_load = pdb_out.name

    if args.emit_pml:
        smin = args.norm_range[0] if args.pml_column == "B_written" and args.bf_norm != "none" else None
        smax = args.norm_range[1] if args.pml_column == "B_written" and args.bf_norm != "none" else None
        pml_path = out_prefix.with_suffix(".apply_b_from_txt.pml")
        emit_pymol_script_apply_btxt(pml_path, pdb_to_load, btxt.name,
                                     b_column=args.pml_column, palette=args.palette,
                                     spectrum_min=smin, spectrum_max=smax)
        print(f"[OK] Wrote PyMOL loader: {pml_path.name}")

    if args.save_plots:
        # 1) R2 by day (chunked, with error bars) — consistent y-axis
        plot_multi_R2_by_day_chunks(wide, out_prefix, labels, pdb_in, chunk_size=50)

        # 2) Histogram for state_score
        try:
            import matplotlib.pyplot as plt
            vals = pd.to_numeric(wide.get("state_score", pd.Series([], dtype=float)), errors="coerce").values.astype(float)
            vals = vals[np.isfinite(vals)]
            if vals.size:
                plt.figure(figsize=(6,4))
                plt.hist(vals, bins=30)
                plt.xlabel("state_score (robust z of R2 slope)"); plt.ylabel("count")
                plt.title("Distribution of state_score"); plt.tight_layout()
                plt.savefig(out_prefix.with_suffix(".state_score_hist.png")); plt.close()
        except Exception:
            pass

        # 3) Chunked plots for the **chosen metric** (state_score or R2_mean) — consistent y-axis
        metric_df = wide[["resid"]].copy()
        metric_df[metric_name] = pd.to_numeric(chosen_metric, errors="coerce")
        plot_bar_chunks(metric_df, metric_name, out_prefix, pdb_in,
                        ylabel=metric_name, title_prefix=f"{metric_name} by residue",
                        chunk_size=50)


if __name__ == "__main__":
    main()
