#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Export Module
Responsible for saving analysis results to CSV files
"""

import os
import numpy as np
from config import OUTPUT_DIR, OUTPUT_CSV, DECIMAL_PLACES, ensure_output_dir


def save_to_csv(displacement, dip_wavelength, wavelength_shift):
    """
    Save displacement, dip wavelength, and wavelength shift data to CSV file

    Args:
        displacement: Displacement array in mm
        dip_wavelength: Dip wavelength array in nm
        wavelength_shift: Wavelength shift array in nm

    Returns:
        str: CSV file path

    CSV file format:
        displacement,dip_wavelength,wavelength_shift
        0,1550.234,0.000
        2,1550.876,0.642
        ...
    """
    # Ensure output directory exists
    ensure_output_dir()

    # CSV file path
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_CSV)

    # Create data matrix
    data = np.column_stack([displacement, dip_wavelength, wavelength_shift])

    # Save to CSV file
    header = 'displacement,dip_wavelength,wavelength_shift'

    # Use numpy.savetxt to save
    np.savetxt(
        filepath,
        data,
        delimiter=',',
        header=header,
        comments='',  # Do not add comment symbol
        fmt=f'%.{DECIMAL_PLACES}f'  # Format decimal places
    )

    print("="*60)
    print("CSV file saved successfully!")
    print("="*60)
    print(f"File path: {filepath}")
    print(f"Number of data rows: {len(displacement)}")
    print(f"Number of data columns: 3")

    # Show CSV file content example
    print("\nCSV file content example:")
    print(header)
    for i in range(min(5, len(displacement))):
        print(f"{displacement[i]:.{DECIMAL_PLACES}f},"
              f"{dip_wavelength[i]:.{DECIMAL_PLACES}f},"
              f"{wavelength_shift[i]:.{DECIMAL_PLACES}f}")
    print("...")

    return filepath


def save_analysis_summary(displacement, dip_wavelength, wavelength_shift,
                          sensitivity, r_squared):
    """
    Save analysis summary to text file

    Args:
        displacement: Displacement array
        dip_wavelength: Dip wavelength array
        wavelength_shift: Wavelength shift array
        sensitivity: Sensor sensitivity (nm/mm)
        r_squared: R² value of linear fit

    Returns:
        str: Summary file path
    """
    ensure_output_dir()

    filepath = os.path.join(OUTPUT_DIR, 'analysis_summary.txt')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("Optical Fiber Displacement Sensor Performance Analysis Summary\n")
        f.write("="*60 + "\n\n")

        f.write("1. Data Overview\n")
        f.write(f"  Number of measurement points: {len(displacement)}\n")
        f.write(f"  Displacement range: {displacement.min()} - {displacement.max()} mm\n")
        f.write(f"  Dip wavelength range: {dip_wavelength.min():.4f} - {dip_wavelength.max():.4f} nm\n")
        f.write(f"  Wavelength shift range: {wavelength_shift.min():.4f} - {wavelength_shift.max():.4f} nm\n\n")

        f.write("2. Sensor Performance\n")
        f.write(f"  Sensitivity: {sensitivity:.4f} nm/mm\n")
        f.write(f"  Linear fit R² value: {r_squared:.4f}\n\n")

        f.write("3. Detailed Data\n")
        f.write("Displacement(mm) | Dip Wavelength(nm) | Wavelength Shift(nm)\n")
        f.write("-"*50 + "\n")
        for d, wl, ws in zip(displacement, dip_wavelength, wavelength_shift):
            f.write(f"{d:6.2f} | {wl:14.4f} | {ws:16.4f}\n")

    print(f"\nAnalysis summary saved: {filepath}")

    return filepath


def verify_csv_file(filepath):
    """
    Verify correctness of CSV file

    Args:
        filepath: CSV file path

    Returns:
        bool: Whether file is valid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    # Read CSV file
    data = np.loadtxt(filepath, delimiter=',', skiprows=1)

    # Check data dimensions
    if data.shape[1] != 3:
        raise ValueError(f"CSV file has incorrect number of columns: {data.shape[1]} != 3")

    print(f"\nCSV file verification passed!")
    print(f"  Data dimensions: {data.shape}")

    return True


if __name__ == "__main__":
    # Test CSV saving functionality
    from data_loader import load_all_data
    from dip_analysis import find_dip_wavelength
    from wavelength_shift import calculate_wavelength_shift
    from config import get_displacement_array

    # Load and process data
    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)
    wavelength_shift = calculate_wavelength_shift(dip_wavelength)
    displacement = get_displacement_array()

    # Save CSV file
    csv_path = save_to_csv(displacement, dip_wavelength, wavelength_shift)

    # Verify CSV file
    verify_csv_file(csv_path)