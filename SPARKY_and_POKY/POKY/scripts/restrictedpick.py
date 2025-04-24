import string
import tkinter
import re

import axes
import pyutil
import poky
import sputil
import tkutil

class restricted_pick_dialog(tkutil.Dialog, tkutil.Stoppable):

  def __init__(self, session):
    self.session = session
    self.grid_widgets = []
    tkutil.Dialog.__init__(self, session.tk, 'Restricted Peak Pick')

    m = sputil.view_combo_menu(session, self.top, 'Find peaks in ')
    m.frame.pack(side='top', anchor='w')
    m.add_callback(self.chose_spectrum_cb)
    self.pick_menu = m

    m = sputil.spectrum_combo_menu(session, self.top, 'Using peaks in ')
    m.frame.pack(side='top', anchor='w')
    m.add_callback(self.chose_spectrum_cb)
    self.ref_menu = m

    # Existing checkbutton: Use selected peaks only
    b = tkutil.checkbutton(self.top, 'Use selected peaks only?', 0)
    b.button.pack(side='top', anchor='w')
    self.selected_only = b

    # NEW checkbutton: Use peak tolerance from Note
    b2 = tkutil.checkbutton(self.top, 'Use tolerance values from "Note"? (Example "Note" text: N=0.2, HN=0.025)', 0)
    b2.button.configure(command=self._use_note_tolerances_cb)
    b2.button.pack(side='top', anchor='w')
    self.use_note_tolerances = b2

    lbl = tkinter.Label(self.top, text='Axis match tolerances (ppm)')
    lbl.pack(side='top', anchor='w')
    self.axis_table_heading = lbl

    f = tkinter.Frame(self.top)
    f.pack(side='top', anchor='w')
    self.axis_table = f
    self.range_entries = []

    self.setup_axis_table()

    progress_label = tkinter.Label(self.top, anchor='nw')
    progress_label.pack(side='top', anchor='w')

    br = tkutil.button_row(self.top,
                           ('Pick peaks', self.pick_cb),
                           ('Select peaks', self.select_cb),
                           ('Stop', self.stop_cb),
                           ('Close', self.close_cb),
                           ('Help', sputil.help_cb(session, 'RestrictedPick')),
                           )
    br.frame.pack(side='top', anchor='w')

    tkutil.Stoppable.__init__(self, progress_label, br.buttons[2])

  def chose_spectrum_cb(self, _):
    """When the user changes the spectra in the menus, rebuild the tolerance table."""
    self.setup_axis_table()

  def setup_axis_table(self):
    # Clear old widgets
    for w in self.grid_widgets:
      w.destroy()
    self.grid_widgets.clear()

    ref_spectrum = self.ref_menu.spectrum()
    pick_view = self.pick_menu.view()
    if ref_spectrum is None or pick_view is None:
      return

    heading = (f"\nAxis match tolerances (ppm)\n"
               f"{ref_spectrum.name} \\ {pick_view.name}")
    self.axis_table_heading['text'] = heading

    # Column headings for pick_spectrum nuclei
    pick_nuclei = pick_view.spectrum.nuclei
    row_offset = 2
    for col_idx, nucleus in enumerate(pick_nuclei, start=1):
      lbl = tkinter.Label(self.axis_table, text=nucleus)
      lbl.grid(row=1, column=col_idx)
      self.grid_widgets.append(lbl)

    # Row headings for ref_spectrum nuclei
    ref_nuclei = ref_spectrum.nuclei
    for row_idx, nucleus in enumerate(ref_nuclei, start=row_offset):
      lbl = tkinter.Label(self.axis_table, text=nucleus)
      lbl.grid(row=row_idx, column=0, sticky='w')
      self.grid_widgets.append(lbl)

    # Create an entry field wherever ref_nuclei[r] == pick_nuclei[p]
    self.range_entries = []
    for r, r_nuc in enumerate(ref_nuclei):
      for p, p_nuc in enumerate(pick_nuclei):
        if r_nuc == p_nuc:
          # Provide a default
          default_val = '0.02' if 'H' in r_nuc else '0.2'
          e = tkutil.entry_field(self.axis_table, '', default_val, 4)
          e.frame.grid(row=(r + row_offset), column=(p + 1), sticky='w')
          self.range_entries.append((r, p, e))
          self.grid_widgets.append(e.frame)

    # Update the enabled/disabled state of the entries based on the toggle
    self._update_range_fields_state()

  def get_settings(self):
    settings = pyutil.generic_class()

    settings.ref_spectrum = self.ref_menu.spectrum()
    if settings.ref_spectrum is None:
      self.progress_report(f"Spectrum {self.ref_menu.get()} not found")
      return None

    settings.pick_view = self.pick_menu.view()
    if settings.pick_view is None:
      self.progress_report(f"View {self.pick_menu.get()} not found")
      return None

    settings.selected_only = self.selected_only.state()
    settings.use_note_tolerances = self.use_note_tolerances.state()

    # The user-chosen reference vs. pick-axis matches and "default" ranges
    settings.ranges = []
    for (ref_axis, pick_axis, ef) in self.range_entries:
      rtext = ef.variable.get()
      r_val = pyutil.string_to_float(rtext)
      if r_val is None:
        r_val = 0.0
      settings.ranges.append((ref_axis, pick_axis, r_val))

    return settings

  def pick_cb(self):
    settings = self.get_settings()
    if not settings:
      return
    if settings.selected_only:
      ref_peaks = settings.ref_spectrum.selected_peaks()
    else:
      ref_peaks = settings.ref_spectrum.peak_list()

    self.stoppable_call(self.pick_peaks,
                        settings.pick_view,
                        ref_peaks,
                        settings.ranges,
                        settings.use_note_tolerances)
    msg = f"Picked {self.picked} peaks in {self.region_count} regions"
    self.progress_report(msg)

  def pick_peaks(self, pick_view, ref_peaks, default_ranges, use_note_tols):
    pick_spectrum = pick_view.spectrum
    height_thresholds = self.picking_thresholds(pick_view)
    min_linewidth = pick_spectrum.pick_minimum_linewidth
    min_dropoff = pick_spectrum.pick_minimum_drop_factor

    self.region_count = 0
    self.picked = 0
    picked_peaks = []

    for ref_peak in ref_peaks:
      self.region_count += 1
      # Attempt to parse per-peak note if enabled
      tol_dict = {}
      try:
        if use_note_tols and ref_peak.note:
          tol_dict = self.parse_tolerance_from_note(ref_peak.note)
      except ValueError as ex:
        # If format is incorrect, print the error and skip
        self.progress_report(str(ex))  # Show the user an error in console/log
        continue

      region = self.pick_region(ref_peak, pick_spectrum, default_ranges, tol_dict)
      region_peaks = pick_spectrum.pick_peaks(region, height_thresholds,
                                              min_linewidth, min_dropoff)

      alias = self.pick_alias(ref_peak, pick_spectrum, default_ranges, tol_dict)
      for p in region_peaks:
        p.alias = alias
        p.selected = 1

      picked_peaks.extend(region_peaks)
      self.picked = len(picked_peaks)
      msg = (f"{self.picked} peaks in {self.region_count} of {len(ref_peaks)} regions")
      self.progress_report(msg)

  def picking_thresholds(self, pick_view):
    # Use the higher of the pick threshold or the lowest displayed contour level
    return (pick_view.negative_levels.lowest, pick_view.positive_levels.lowest)

  def pick_alias(self, ref_peak, pick_spectrum, default_ranges, tol_dict):
    # If Note-based tolerance is used, we may want an alias if freq is out of bounds
    alias = [0]*pick_spectrum.dimension
    pick_nuclei = pick_spectrum.nuclei

    for (ref_axis, pick_axis, default_range) in default_ranges:
      freq = ref_peak.frequency[ref_axis]
      # Overwrite range if Note-tolerance is found:
      nucleus = pick_nuclei[pick_axis]
      use_range = tol_dict.get(nucleus, default_range)

      pos = sputil.alias_axis_onto_spectrum(freq, pick_axis, pick_spectrum)
      # We only do the alias if freq is truly outside the data region.
      # Implementation can vary; for now we just keep the standard approach:
      if pos != freq:
        alias[pick_axis] = freq - pos

    return alias

  def pick_region(self, ref_peak, pick_spectrum, default_ranges, tol_dict):
    """Return (region_min, region_max) around ref_peak for pick_spectrum."""
    rmin = list(pick_spectrum.region[0])
    rmax = list(pick_spectrum.region[1])

    pick_nuclei = pick_spectrum.nuclei

    for (ref_axis, pick_axis, default_range) in default_ranges:
      freq = ref_peak.frequency[ref_axis]
      # If using per-peak Note, see if there's a custom tolerance:
      nucleus = pick_nuclei[pick_axis]
      use_range = tol_dict.get(nucleus, default_range)

      pos = sputil.alias_axis_onto_spectrum(freq, pick_axis, pick_spectrum)
      rmin[pick_axis] = max(rmin[pick_axis], pos - use_range)
      rmax[pick_axis] = min(rmax[pick_axis], pos + use_range)

    return (tuple(rmin), tuple(rmax))

  def select_cb(self):
    settings = self.get_settings()
    if not settings:
      return

    if settings.selected_only:
      ref_peaks = settings.ref_spectrum.selected_peaks()
    else:
      ref_peaks = settings.ref_spectrum.peak_list()

    pick_spectrum = settings.pick_view.spectrum
    self.stoppable_call(self.select_peaks,
                        pick_spectrum,
                        ref_peaks,
                        settings.ranges,
                        settings.use_note_tolerances)

    msg = f"Selected {self.selected} peaks in {self.region_count} regions"
    self.progress_report(msg)

  def select_peaks(self, pick_spectrum, ref_peaks, default_ranges, use_note_tols):
    target_peaks = pick_spectrum.peak_list()
    selected_peaks = {}
    self.region_count = 0
    self.selected = 0

    for rp in ref_peaks:
      self.region_count += 1
      # parse per-peak note if toggled
      tol_dict = {}
      try:
        if use_note_tols and rp.note:
          tol_dict = self.parse_tolerance_from_note(rp.note)
      except ValueError as ex:
        self.progress_report(str(ex))
        continue

      for tp in target_peaks:
        if self.close_peaks(rp, tp, default_ranges, pick_spectrum, tol_dict):
          selected_peaks[tp] = 1

      self.selected = len(selected_peaks)
      msg = (f"{self.selected} peaks selected in {self.region_count} of {len(ref_peaks)} regions")
      self.progress_report(msg)

    selected_peaks_list = list(selected_peaks.keys())
    if selected_peaks_list:
      self.session.unselect_all_ornaments()
    for p in selected_peaks_list:
      p.selected = 1

  def close_peaks(self, ref_peak, target_peak, default_ranges, pick_spectrum, tol_dict):
    """Return True if target_peak is within tolerance of ref_peak."""
    pick_nuclei = pick_spectrum.nuclei
    for (ref_axis, pick_axis, default_range) in default_ranges:
      dist = abs(ref_peak.frequency[ref_axis] - target_peak.frequency[pick_axis])
      nucleus = pick_nuclei[pick_axis]
      use_range = tol_dict.get(nucleus, default_range)
      if dist > use_range:
        return False
    return True

  def parse_tolerance_from_note(self, note_text):
    """
    Parse the note text for patterns like:  X=0.2, HN=0.025
    If the format is incorrect or missing, raise ValueError with an explanatory message.
    """
    pattern = r'([A-Za-z0-9]+)=([0-9.]+)'
    matches = re.findall(pattern, note_text)
    if not matches:
      raise ValueError(
        f"Note format invalid: \"{note_text}\". "
        "Expected comma-separated pairs like: N=0.2, HN=0.025"
      )
    tol_dict = {}
    for nuc, val_str in matches:
      try:
        tol_dict[nuc] = float(val_str)
      except ValueError:
        raise ValueError(
          f"Note format invalid: cannot convert \"{val_str}\" to float. "
          "Expected something like N=0.2, HN=0.025"
        )
    return tol_dict

  def _use_note_tolerances_cb(self):
    """
    Called when the user toggles 'Use peak tolerance from Note?'.
    Enable/disable the tolerance text entries accordingly.
    """
    self._update_range_fields_state()

  def _update_range_fields_state(self):
    """Enable or disable the tolerance entries based on use_note_tolerances."""
    use_note = self.use_note_tolerances.state()
    state_val = ('disabled' if use_note else 'normal')
    bg_color = ('lightgray' if use_note else 'white')
    for (_, _, ef) in self.range_entries:
      ef.entry.configure(state=state_val, disabledforeground='gray', bg=bg_color)

def show_dialog(session):
  sputil.the_dialog(restricted_pick_dialog, session).show_window(1)
