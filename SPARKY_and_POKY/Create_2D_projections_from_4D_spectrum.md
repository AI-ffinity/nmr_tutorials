# Creating 2D and 3D Projections from 4D NOESY with POKY/NMRFAM Sparky

This tutorial guides you through creating 2D and 3D projections from a 4D NOESY spectrum using the `ucsfdata` script from NMRFAM Sparky. We'll start by converting the 4D spectrum to UCSF format and proceed with generating and analyzing the projections.

## POKY installation

Sometimes running the POKY/Sparky utility scripts (especially `bruk2ucsf`) outside their directory yields segmentation 
faults. Therefore, add the following functions into your `~/.bashrc` script:

```shell
alias poky="/opt/POKY/poky_linux/bin/poky"

# Helper function: resolves relative paths, changes to /opt/POKY/poky_linux/bin/, executes a command,
# and returns to the original directory.
_run_in_poky_bin() {
    # Arguments:
    #   $1: Command name (e.g. "bruk2ucsf" or "ucsfdata")
    #   $2: Relative path to the input file.
    #   $3: Relative path to the output file.
    if [ "$#" -ne 3 ]; then
        echo "Usage: _run_in_poky_bin <command_name> <relative_input> <relative_output>"
        return 1
    fi

    local cmd="$1"
    local input_rel="$2"
    local output_rel="$3"

    # Resolve absolute paths using realpath.
    local input_full
    input_full=$(realpath "$input_rel") || { echo "Error: Cannot resolve input file path"; return 1; }
    
    local output_dir
    output_dir=$(realpath "$(dirname "$output_rel")") || { echo "Error: Cannot resolve output directory"; return 1; }
    local output_full="${output_dir}/$(basename "$output_rel")"

    # Change directory to /opt/POKY/poky_linux/bin/ using pushd/popd.
    pushd /opt/POKY/poky_linux/bin/ > /dev/null || { echo "Error: Unable to enter /opt/POKY/poky_linux/bin/"; return 1; }

    # Execute the command with full path arguments.
    ./"$cmd" "$input_full" "$output_full"

    # Return to the original directory.
    popd > /dev/null
}

# Function: bruk2ucsf_run
# Usage: bruk2ucsf_run <relative_input> <relative_output>
bruk2ucsf_run() {
    if [ "$#" -ne 2 ]; then
        echo "Usage: bruk2ucsf_run <relative_input> <relative_output>"
        return 1
    fi
    _run_in_poky_bin "bruk2ucsf" "$1" "$2"
}
```

Then do `source ~/.bashrc`.

## Step 1: Convert 4D Spectrum to UCSF

- First, ensure you have the 4D spectrum ready in UCSF format. If not, use NMRFAM Sparky's utility script to convert it (e.g., `bruk2ucsf`).
- Use the following command to create a 3D HN projection from your 4D HCNH NOESY spectrum:

```shell
ucsfdata -a4 HN -p4 -r -o 3D_HN_projection.ucsf 4D_HCNH_NOESY_NUS_reconstructed.ucsf
```

- Next, generate a 2D HC-C projection from the 3D HN projection:

```shell
ucsfdata -a3 N -p3 -r -o 2D_HC-C_projection.ucsf 3D_HN_projection.ucsf
```


## Step 2: Rename Axes for Synchronization

- After the first `ucsfdata` call, the w4 axis of the original spectrum is renamed to HN. To synchronize the 4D spectrum with the 15N HSQC for peak picking, ensure the w2 axis is also named HN:

```shell
ucsfdata -a1 15N -a2 HN -o 15N_HSQC_renamed_axes.ucsf 15N_HSQC.ucsf
```

- Apply the same renaming process for the 13C HSQC to align with the HC-C projection:

```shell
ucsfdata -a1 C -a2 HC -o 13C_HSQC_renamed_axes.ucsf 13C_HSQC.ucsf
```


## Step 3: Compare 2D C-H Projection with 13C HSQC

- Before loading the 13C HSQC, ensure it is properly folded for comparison with the 2D plane from the 4D.
- Load the 13C HSQC and adjust its display:
- Use `vt` to increase the aspect value, making the peaks look wider.
- Use `ol` to overlay the 2D projection onto the 13C HSQC.
- Adjust colors for differentiation between the two spectra with `ct`.

## Step 4: Align the 2D C-H Projection with the 13C HSQC

- Select one peak from the window of the 2D C-H Projection and the equivalent peak from the window of the 13C HSQC 
(not both peaks from the same window where the spectra are overlaid).
- Use `al`, select the right windows and then click `Auto Align`

## Additional Resources

- For those interested in creating 2D projections via the graphical user interface (GUI), refer to the following video 
tutorial: [How to Make 2D Projections of 3D Spectra](https://www.youtube.com/watch?v=KyfyS5inLwI)

**Note:** While the GUI method is available, this tutorial focuses on the command-line approach for its efficiency and precision.


With ucsfdata you can also pull 2D slices from the 4D. You can go back to `-wN` parameter and find the “index” that 
gives your preferred ppm slice.
https://groups.google.com/g/nmr-sparky/c/wb2IJoeNPZc
