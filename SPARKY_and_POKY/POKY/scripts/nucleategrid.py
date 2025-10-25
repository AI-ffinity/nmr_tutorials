"""
Nucleate Grid — GUI plugin for POKY/Sparky
Author: Thomas Evangelidis

Description
----------
Create a lattice of 2D grid points around seed peaks and add them to the same
spectrum. You can use these artificial peaks along with the seed (real) peaks for
more accurate restricted peak picking, particularly where the target spectrum in NOESY-type.

Seeds are taken from the spectrum chosen in “Using seeds in”
(optionally only the currently selected peaks). Each seed is marked by appending
the word 'seed' to its Note. For each seed at (w1,w2), candidate lattice points
spaced by (w1_step, w2_step) are generated, and only those inside the ellipse

    (Δw1 / r1)^2 + (Δw2 / r2)^2 ≤ 1

are accepted (set r1=r2 for a circle). A step-sized "padding" (w1_step, w2_step)
prevents placing new points too close to any seed, and a proximity index
de-duplicates new points among themselves.

If “Generated label” is provided, that text is attached as a user-visible label
(or Note fallback when user labels are unsupported) to each *generated* peak
(never to seeds). If the field is left blank, **no label is attached** to
generated peaks. Defaults: w1_step=0.05, w2_step=0.005, r1=0.4, r2=0.05; precision=3.
"""

import tkinter as tk
from math import floor

try:
  from poky import sputil, tkutil, pyutil
except Exception:
  from sparky import sputil, tkutil, pyutil


# ---------- Proximity index (seed moat & generated de-dup) --------------------
class ProximityIndex:
  def __init__(self, w1_step, w2_step):
    if w1_step <= 0 or w2_step <= 0:
      raise ValueError("w1-step and w2-step must be positive.")
    self.s1 = float(w1_step)
    self.s2 = float(w2_step)
    self._bins = {}
    self._eps = 1e-12

  def _bin_of(self, x, y):
    return int(floor(x / self.s1)), int(floor(y / self.s2))

  def _neighbors(self, bx, by):
    for dx in (-1, 0, 1):
      for dy in (-1, 0, 1):
        yield (bx + dx, by + dy)

  def is_far(self, x, y):
    bx, by = self._bin_of(x, y)
    for nb in self._neighbors(bx, by):
      for (px, py) in self._bins.get(nb, ()):
        if abs(x - px) <= self.s1 + self._eps and abs(y - py) <= self.s2 + self._eps:
          return False
    return True

  def add(self, x, y):
    bx, by = self._bin_of(x, y)
    self._bins.setdefault((bx, by), []).append((x, y))


def nucleate_around_peak(w1, w2, w1_step, w2_step, r1, r2):
  """Yield all lattice points in the surrounding rectangle; ellipse filter is applied later."""
  n1 = int(floor(max(0.0, r1) / w1_step))
  n2 = int(floor(max(0.0, r2) / w2_step))
  for i in range(-n1, n1 + 1):
    for j in range(-n2, n2 + 1):
      yield (w1 + i * w1_step, w2 + j * w2_step, i, j)


def _inside_ellipse(dx, dy, r1, r2):
  """True if (dx,dy) lies within the ellipse (dx/r1)^2 + (dy/r2)^2 ≤ 1."""
  r1e = max(float(r1), 1e-12)
  r2e = max(float(r2), 1e-12)
  return (dx*dx)/(r1e*r1e) + (dy*dy)/(r2e*r2e) <= 1.0 + 1e-12


# ---------- Dialog ------------------------------------------------------------
class nucleategrid_dialog(tkutil.Dialog, tkutil.Stoppable):

  def __init__(self, session):
    self.session = session
    tkutil.Dialog.__init__(self, session.tk, 'Nucleate Grid')

    # Seed spectrum (same style as other Poky dialogs like restrictedpick)
    m = sputil.spectrum_combo_menu(session, self.top, 'Using seeds in ')
    m.frame.pack(side='top', anchor='w')
    self.ref_menu = m

    b = tkutil.checkbutton(self.top, 'Use selected peaks only?', 1)
    b.button.pack(side='top', anchor='w')
    self.selected_only = b

    # Parameters (defaults as requested)
    row1 = tk.Frame(self.top); row1.pack(side='top', anchor='w', padx=6, pady=(6, 0))
    self.w1_step = tkutil.entry_field(row1, "w1 step (ppm): ", width=8, initial="0.05")
    self.w1_step.frame.pack(side='left')
    self.w2_step = tkutil.entry_field(row1, "w2 step (ppm): ", width=8, initial="0.005")
    self.w2_step.frame.pack(side='left', padx=(10, 0))

    row2 = tk.Frame(self.top); row2.pack(side='top', anchor='w', padx=6, pady=(4, 0))
    self.r1 = tkutil.entry_field(row2, "r1 (ppm): ", width=8, initial="0.4")
    self.r1.frame.pack(side='left')
    self.r2 = tkutil.entry_field(row2, "r2 (ppm): ", width=8, initial="0.05")
    self.r2.frame.pack(side='left', padx=(10, 0))

    row3 = tk.Frame(self.top); row3.pack(side='top', anchor='w', padx=6, pady=(4, 0))
    self.precision = tkutil.entry_field(row3, "precision (decimals): ", width=6, initial="3")
    self.precision.frame.pack(side='left')

    g = tk.Frame(self.top); g.pack(side='top', anchor='w', padx=6, pady=(4, 0))
    self.gen_label = tkutil.entry_field(g, "Generated label (user label on peak, optional): ",
                                        width=24, initial="")
    self.gen_label.frame.pack(side='left', anchor='w')

    # Progress + buttons
    progress_label = tk.Label(self.top, anchor='w', justify='left')
    progress_label.pack(side='top', anchor='w', padx=6, pady=(6, 2))
    self.progress_label = progress_label

    br = tkutil.button_row(
      self.top,
      ('Generate', self.run_cb),
      ('Preview', self.preview_cb),
      ('Stop', self.stop_cb),
      ('Close', self.close_cb),
      ('Help', sputil.help_cb(session, 'nucleategrid')),
    )
    br.frame.pack(side='top', anchor='w', padx=6, pady=(2, 8))

    tkutil.Stoppable.__init__(self, progress_label, br.buttons[2])

  # ---- Settings / seeds ------------------------------------------------------

  def _read_settings(self):
    s = pyutil.generic_class()
    s.ref_spectrum = self.ref_menu.spectrum()
    if s.ref_spectrum is None:
      raise ValueError(f"Spectrum {self.ref_menu.get()} not found")
    if getattr(s.ref_spectrum, 'dimension', 2) != 2:
      raise ValueError("Nucleate Grid currently supports 2D spectra only.")

    s.selected_only = self.selected_only.state()
    s.w1_step = pyutil.string_to_float(self.w1_step.variable.get())
    s.w2_step = pyutil.string_to_float(self.w2_step.variable.get())
    s.r1      = pyutil.string_to_float(self.r1.variable.get())
    s.r2      = pyutil.string_to_float(self.r2.variable.get())
    ptxt = self.precision.variable.get().strip()
    s.precision = int(ptxt) if ptxt != "" else 3
    gl = self.gen_label.variable.get().strip()
    s.gen_label = gl if gl != "" else None  # None => attach no label to generated peaks
    return s

  def _gather_seeds(self, spectrum, selected_only, fallback_label='?-?'):
    """Return (seed_peak_objects, seed_data) where seed_data = [(label, w1, w2), ...]."""
    peaks = spectrum.selected_peaks() if selected_only else spectrum.peak_list()
    if not peaks:
      raise ValueError("No seeds found. Select peaks or uncheck 'Use selected peaks only?'.")
    seeds = []
    for p in peaks:
      try:
        w1, w2 = p.frequency[0], p.frequency[1]
      except Exception:
        continue
      # Best-effort human-readable seed label for logging only
      label = None
      if hasattr(p, 'assignment'):
        lab = getattr(p, 'assignment')
        if isinstance(lab, str) and lab.strip():
          label = lab.strip()
        elif isinstance(lab, (tuple, list)):
          try:
            label = "-".join(str(x) for x in lab if x is not None)
          except Exception:
            pass
      if (not label) and hasattr(p, 'note') and isinstance(p.note, str) and p.note.strip():
        label = p.note.strip()
      seeds.append((label if label else fallback_label, w1, w2))
    if not seeds:
      raise ValueError("Could not read w1/w2 from selected peaks.")
    return peaks, seeds

  def _mark_seeds(self, peak_list):
    """Append the word 'seed' to each seed peak's Note (idempotent)."""
    for p in peak_list:
      try:
        txt = getattr(p, 'note', '') or ''
        if 'seed' not in txt.split():
          sep = '' if (txt == '' or txt.endswith(' ')) else ' '
          p.note = (txt + sep + 'seed').strip()
      except Exception:
        pass

  # ---- Buttons ---------------------------------------------------------------

  def preview_cb(self):
    try:
      s = self._read_settings()
      seed_objs, seeds = self._gather_seeds(s.ref_spectrum, s.selected_only)
    except Exception as e:
      self.progress_report(str(e)); return

    seed_index = ProximityIndex(s.w1_step, s.w2_step)
    for _, w1s, w2s in seeds:
      seed_index.add(w1s, w2s)
    gen_index = ProximityIndex(s.w1_step, s.w2_step)

    generated = 0
    for (_, w1c, w2c) in seeds:
      self.check_for_stop()
      for (x, y, i, j) in nucleate_around_peak(w1c, w2c, s.w1_step, s.w2_step, s.r1, s.r2):
        if i == 0 and j == 0:
          continue
        dx = i * s.w1_step
        dy = j * s.w2_step
        if not _inside_ellipse(dx, dy, s.r1, s.r2):
          continue
        if not seed_index.is_far(x, y):
          continue
        if not gen_index.is_far(x, y):
          continue
        gen_index.add(x, y)
        generated += 1

    self.progress_report(f"Preview: {len(seeds)} seeds; would generate {generated} additional peaks (elliptical region).")

  def run_cb(self):
    try:
      s = self._read_settings()
      seed_objs, seeds = self._gather_seeds(s.ref_spectrum, s.selected_only)
    except Exception as e:
      self.progress_report(str(e)); return
    # tag seeds before creating grid points
    self._mark_seeds(seed_objs)
    self.stoppable_call(self._run_impl, s, seeds)

  # ---- Main work -------------------------------------------------------------

  def _run_impl(self, s, seeds):
    seed_index = ProximityIndex(s.w1_step, s.w2_step)
    for _, w1s, w2s in seeds:
      seed_index.add(w1s, w2s)
    gen_index = ProximityIndex(s.w1_step, s.w2_step)

    out_gen_points = []
    total = len(seeds)
    for si, (seed_label, w1c, w2c) in enumerate(seeds, start=1):
      self.check_for_stop()
      self.progress_report(f"Generating around seed {si} / {total}…")

      # IMPORTANT: no fallback to seed label — None means "attach no label".
      label_for_gen = s.gen_label if s.gen_label is not None else None

      for (x, y, i, j) in nucleate_around_peak(w1c, w2c, s.w1_step, s.w2_step, s.r1, s.r2):
        if i == 0 and j == 0:
          continue
        dx = i * s.w1_step
        dy = j * s.w2_step
        if not _inside_ellipse(dx, dy, s.r1, s.r2):
          continue
        if not seed_index.is_far(x, y):
          continue
        if not gen_index.is_far(x, y):
          continue
        gen_index.add(x, y)
        out_gen_points.append((label_for_gen, x, y))

    # Fixed sort: w1-slowest (then w2)
    out_gen_points.sort(key=lambda t: (t[1], t[2]))

    # Create peaks in the same spectrum; attach user labels only if provided
    created = 0
    for (label, x, y) in out_gen_points:
      self.check_for_stop()
      try:
        p = self._safe_new_peak(s.ref_spectrum, (x, y))
        if label:                    # <-- attach nothing if label is None / empty
          self._set_user_label_on_peak(p, label)
        try:
          p.selected = 1
        except Exception:
          pass
        created += 1
      except Exception as ex:
        self.progress_report(f"Failed to create peak at ({x:.3f}, {y:.3f}): {ex}")

    self.progress_report(f"Done: {len(seeds)} seeds; created {created} peaks in {s.ref_spectrum.name} (elliptical region).")

  # Robust creation across Sparky/POKY builds
  def _safe_new_peak(self, spectrum, xy):
    for meth in ('new_peak', 'place_peak', 'peak'):
      if hasattr(spectrum, meth):
        try:
          return getattr(spectrum, meth)(xy)
        except Exception:
          pass
    raise RuntimeError("Spectrum API lacks new_peak/place_peak/peak")

  # Attach a visible user label if supported; otherwise fall back to Note.
  def _set_user_label_on_peak(self, peak, text):
    for attr in ('user_label', 'label_text'):
      if hasattr(peak, attr):
        try:
          setattr(peak, attr, text)
          for meth in ('show_user_label', 'show_label'):
            if hasattr(peak, meth):
              try: getattr(peak, meth)()
              except Exception: pass
          return
        except Exception:
          pass
    if hasattr(peak, 'label'):
      try:
        lbl = peak.label
        if hasattr(lbl, 'text'):
          lbl.text = text
          if hasattr(peak, 'show_label'):
            try: peak.show_label()
            except Exception: pass
          return
      except Exception:
        pass
    for helper in ('label_peak', 'user_label_peak', 'set_user_label'):
      if hasattr(sputil, helper):
        try:
          getattr(sputil, helper)(peak, text)
          return
        except Exception:
          pass
    # Fallback: store where you can see it in tables
    try:
      peak.note = text
    except Exception:
      pass


# ---------- Entry point -------------------------------------------------------
def show_dialog(session):
  sputil.the_dialog(nucleategrid_dialog, session).show_window(1)
