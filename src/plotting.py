#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting Module
Responsible for generating spectra plot, wavelength shift plot, and linear fit plot
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from config import (
    OUTPUT_DIR, PLOT_DPI, PLOT_FORMAT, PLOT_SIZE,
    OUTPUT_SPECTRA_PLOT, OUTPUT_SHIFT_PLOT, OUTPUT_FIT_PLOT,
    SPECTRA_COLORS, get_plot_indices, ensure_output_dir
)

# Set matplotlib font (if needed)
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.unicode_minus'] = False


def plot_spectra(wavelength, power_data, displacement):
    """
    Plot spectra (power vs wavelength) for different displacements

    Args:
        wavelength: Wavelength array in nm
        power_data: Power data matrix with shape=(number of wavelength points, number of displacement points)
        displacement: Displacement array in mm

    Returns:
        str: Image file path

    Plot requirements:
        - Selected displacement points: 0, 4, 8, 12, 16, 20, 24, 28 mm
        - 8 curves total, distinguished by different colors
        - Include legend, axis labels, and title
        - Zoom in on the dip region for better visualization
    """
    ensure_output_dir()

    # Get indices of displacement points to plot
    plot_indices = get_plot_indices()

    # Create figure with wider aspect ratio for better spread
    plt.figure(figsize=(14, 7))

    # Plot each spectra curve
    for idx, color in zip(plot_indices, SPECTRA_COLORS):
        disp_value = displacement[idx]
        plt.plot(
            wavelength,
            power_data[:, idx],
            color=color,
            linewidth=1.5,
            label=f'{disp_value} mm'
        )

    # Set axis labels and title
    plt.xlabel('Wavelength (nm)', fontsize=14)
    plt.ylabel('Power (dBm)', fontsize=14)
    plt.title('Optical Fiber Displacement Sensor Spectra', fontsize=16)

    # Set legend with better positioning
    plt.legend(loc='lower left', fontsize=12)

    # Add grid
    plt.grid(True, alpha=0.3)

    # Zoom in on the dip region (1552-1555 nm) for better visualization
    plt.xlim(1552.0, 1555.0)
    plt.ylim(-47, -31)

    # Adjust layout
    plt.tight_layout()

    # Save image
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_SPECTRA_PLOT)
    plt.savefig(filepath, dpi=PLOT_DPI, format=PLOT_FORMAT)
    plt.close()

    print("="*60)
    print("Spectra plot saved successfully!")
    print("="*60)
    print(f"File path: {filepath}")
    print(f"Displacement points included: {[displacement[i] for i in plot_indices]} mm")

    return filepath


def plot_wavelength_shift(displacement, wavelength_shift):
    """
    Plot scatter plot of wavelength shift vs displacement

    Args:
        displacement: Displacement array in mm
        wavelength_shift: Wavelength shift array in nm

    Returns:
        str: Image file path

    Plot requirements:
        - X-axis: Displacement (mm)
        - Y-axis: Wavelength shift Δλ (nm)
        - Use scatter plot or line plot
    """
    ensure_output_dir()

    # Create figure
    plt.figure(figsize=PLOT_SIZE)

    # Plot scatter points
    plt.scatter(
        displacement,
        wavelength_shift,
        color='blue',
        s=50,
        marker='o',
        label='Data Points',
        zorder=3
    )

    # Plot line connecting data points
    plt.plot(
        displacement,
        wavelength_shift,
        color='blue',
        linewidth=1,
        alpha=0.5,
        zorder=2
    )

    # Set axis labels and title
    plt.xlabel('Displacement (mm)', fontsize=12)
    plt.ylabel('Wavelength Shift Δλ (nm)', fontsize=12)
    plt.title('Wavelength Shift vs Displacement', fontsize=14)

    # Set legend
    plt.legend(loc='best', fontsize=10)

    # Add grid
    plt.grid(True, alpha=0.3)

    # Adjust layout
    plt.tight_layout()

    # Save image
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_SHIFT_PLOT)
    plt.savefig(filepath, dpi=PLOT_DPI, format=PLOT_FORMAT)
    plt.close()

    print("="*60)
    print("Wavelength shift plot saved successfully!")
    print("="*60)
    print(f"File path: {filepath}")

    return filepath


def plot_linear_fit(displacement, wavelength_shift, slope, intercept, r_squared):
    """
    Plot linear fit results

    Args:
        displacement: Displacement array in mm
        wavelength_shift: Wavelength shift array in nm
        slope: Slope of fitted line (sensitivity)
        intercept: Intercept of fitted line
        r_squared: R² value

    Returns:
        str: Image file path

    Plot requirements:
        - Show both original data points and fitted line
        - Label fitting equation
        - Display R² value
    """
    ensure_output_dir()

    # Calculate fitted line
    y_pred = slope * displacement + intercept

    # Create figure
    plt.figure(figsize=PLOT_SIZE)

    # Plot original data points
    plt.scatter(
        displacement,
        wavelength_shift,
        color='blue',
        s=50,
        marker='o',
        label='Data Points',
        zorder=3
    )

    # Plot fitted line
    plt.plot(
        displacement,
        y_pred,
        color='red',
        linewidth=2,
        label=f'Linear Fit: Δλ = {slope:.4f}×d + {intercept:.4f}\nR² = {r_squared:.4f}',
        zorder=2
    )

    # Set axis labels and title
    plt.xlabel('Displacement (mm)', fontsize=12)
    plt.ylabel('Wavelength Shift Δλ (nm)', fontsize=12)
    plt.title('Wavelength Shift vs Displacement with Linear Fit', fontsize=14)

    # Set legend
    plt.legend(loc='best', fontsize=10)

    # Add grid
    plt.grid(True, alpha=0.3)

    # Adjust layout
    plt.tight_layout()

    # Save image
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_FIT_PLOT)
    plt.savefig(filepath, dpi=PLOT_DPI, format=PLOT_FORMAT)
    plt.close()

    print("="*60)
    print("Linear fit plot saved successfully!")
    print("="*60)
    print(f"File path: {filepath}")
    print(f"Fitting equation: Δλ = {slope:.4f}×d + {intercept:.4f}")
    print(f"R² value: {r_squared:.4f}")

    return filepath


def plot_all_spectra_comparison(wavelength, power_data, displacement):
    """
    Plot comparison of all displacement spectra (optional feature)

    Args:
        wavelength: Wavelength array
        power_data: Power data matrix
        displacement: Displacement array

    Returns:
        str: Image file path
    """
    ensure_output_dir()

    # Create figure with wider aspect ratio for better spread
    plt.figure(figsize=(14, 7))

    # Use gradient colors for all spectra
    colors = plt.cm.viridis(np.linspace(0, 1, len(displacement)))

    for i, color in enumerate(colors):
        plt.plot(
            wavelength,
            power_data[:, i],
            color=color,
            linewidth=1.5,
            alpha=0.8,
            label=f'{displacement[i]} mm'
        )

    # Set axis labels and title
    plt.xlabel('Wavelength (nm)', fontsize=14)
    plt.ylabel('Power (dBm)', fontsize=14)
    plt.title('All Spectra Comparison', fontsize=16)

    # Set legend with better positioning
    plt.legend(loc='lower left', fontsize=12, ncol=2)

    # Add grid
    plt.grid(True, alpha=0.3)

    # Zoom in on the dip region (1552-1555 nm) for better visualization
    plt.xlim(1552.0, 1555.0)
    plt.ylim(-47, -31)

    # Adjust layout
    plt.tight_layout()

    filepath = os.path.join(OUTPUT_DIR, 'all_spectra_comparison.png')
    plt.savefig(filepath, dpi=PLOT_DPI, format='png')
    plt.close()

    print(f"\nAll spectra comparison plot saved: {filepath}")

    return filepath


if __name__ == "__main__":
    # Test plotting functionality
    from data_loader import load_all_data
    from dip_analysis import find_dip_wavelength
    from wavelength_shift import calculate_wavelength_shift
    from config import get_displacement_array

    # Load and process data
    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)
    wavelength_shift = calculate_wavelength_shift(dip_wavelength)
    displacement = get_displacement_array()

    # Plot spectra
    spectra_path = plot_spectra(wavelength, power_data, displacement)

    # Plot wavelength shift
    shift_path = plot_wavelength_shift(displacement, wavelength_shift)

    # Simple linear fit for testing
    slope, intercept = np.polyfit(displacement, wavelength_shift, 1)
    y_pred = slope * displacement + intercept
    ss_tot = np.sum((wavelength_shift - np.mean(wavelength_shift)) ** 2)
    ss_res = np.sum((wavelength_shift - y_pred) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # Plot linear fit
    fit_path = plot_linear_fit(displacement, wavelength_shift, slope, intercept, r_squared)

    print("\nAll images generated successfully!")