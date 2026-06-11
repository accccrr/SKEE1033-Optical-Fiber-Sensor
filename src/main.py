#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Program Module
Integrates all functional modules to complete optical fiber displacement sensor performance analysis
"""

import os
import sys
from datetime import datetime

# Import functional modules
from config import (
    ensure_output_dir, OUTPUT_DIR, get_displacement_array,
    NUM_MEASUREMENTS
)
from data_loader import load_all_data
from dip_analysis import find_dip_wavelength, analyze_dip_characteristics
from wavelength_shift import (
    calculate_wavelength_shift, validate_wavelength_shift,
    calculate_shift_statistics
)
from linear_fit import (
    perform_linear_fit, calculate_sensitivity,
    analyze_residuals, evaluate_sensor_performance
)
from data_exporter import save_to_csv, save_analysis_summary, verify_csv_file
from plotting import (
    plot_spectra, plot_wavelength_shift, plot_linear_fit,
    plot_all_spectra_comparison
)


def print_header():
    """Print program header"""
    print("\n" + "="*70)
    print(" "*15 + "Optical Fiber Displacement Sensor Performance Analysis")
    print(" "*20 + "Scientific Programming Project")
    print("="*70)
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*70 + "\n")


def print_summary(displacement, dip_wavelength, wavelength_shift,
                  sensitivity, r_squared, performance):
    """
    Print analysis results summary

    Args:
        displacement: Displacement array
        dip_wavelength: Dip wavelength array
        wavelength_shift: Wavelength shift array
        sensitivity: Sensor sensitivity
        r_squared: R² value
        performance: Performance evaluation results
    """
    print("\n" + "="*70)
    print(" "*25 + "Analysis Results Summary")
    print("="*70)

    print("\n1. Basic Data Statistics")
    print(f"  Number of measurement points: {len(displacement)}")
    print(f"  Displacement range: {displacement.min()} - {displacement.max()} mm")
    print(f"  Dip wavelength range: {dip_wavelength.min():.4f} - {dip_wavelength.max():.4f} nm")
    print(f"  Wavelength shift range: {wavelength_shift.min():.4f} - {wavelength_shift.max():.4f} nm")

    print("\n2. Sensor Performance Metrics")
    print(f"  Sensitivity: {sensitivity:.4f} nm/mm")
    print(f"  Linear fit R² value: {r_squared:.4f}")
    print(f"  Sensitivity evaluation: {performance['sensitivity_level']}")
    print(f"  Linearity evaluation: {performance['linearity_level']}")
    print(f"  Overall evaluation: {performance['overall_score']}")

    print("\n3. Detailed Data Table")
    print("Displacement(mm) | Dip Wavelength(nm) | Wavelength Shift(nm)")
    print("-"*50)
    for d, wl, ws in zip(displacement, dip_wavelength, wavelength_shift):
        print(f"{d:6.2f}   | {wl:14.4f}  | {ws:16.4f}")

    print("="*70)


def main():
    """
    Main function: Execute complete analysis workflow

    Analysis workflow:
        1. Load raw data
        2. Calculate dip wavelength
        3. Calculate wavelength shift
        4. Perform linear fitting
        5. Calculate sensor sensitivity
        6. Save data to CSV
        7. Generate analysis plots
        8. Save analysis summary
    """
    try:
        # Print program header
        print_header()

        # Ensure output directory exists
        ensure_output_dir()

        # Step 1: Load raw data
        print("\n【Step 1】Loading Raw Data")
        wavelength, power_data = load_all_data()

        # Step 2: Calculate dip wavelength
        print("\n【Step 2】Calculating Dip Wavelength")
        dip_wavelength = find_dip_wavelength(wavelength, power_data)

        # Analyze dip characteristics
        dip_characteristics = analyze_dip_characteristics(
            wavelength, power_data, dip_wavelength
        )

        # Step 3: Calculate wavelength shift
        print("\n【Step 3】Calculating Wavelength Shift")
        wavelength_shift = calculate_wavelength_shift(dip_wavelength)

        # Validate wavelength shift calculation
        validate_wavelength_shift(wavelength_shift)

        # Calculate wavelength shift statistics
        shift_statistics = calculate_shift_statistics(wavelength_shift)

        # Get displacement array
        displacement = get_displacement_array()

        # Step 4: Perform linear fitting
        print("\n【Step 4】Performing Linear Fitting")
        fit_results = perform_linear_fit(displacement, wavelength_shift)

        # Analyze residuals
        residual_analysis = analyze_residuals(
            fit_results['residuals'], displacement
        )

        # Step 5: Calculate sensor sensitivity
        print("\n【Step 5】Calculating Sensor Sensitivity")
        sensitivity = calculate_sensitivity(fit_results['slope'])

        # Evaluate sensor performance
        performance = evaluate_sensor_performance(
            sensitivity, fit_results['r_squared']
        )

        # Step 6: Save data to CSV
        print("\n【Step 6】Saving Data to CSV")
        csv_path = save_to_csv(displacement, dip_wavelength, wavelength_shift)

        # Verify CSV file
        verify_csv_file(csv_path)

        # Step 7: Generate analysis plots
        print("\n【Step 7】Generating Analysis Plots")

        # Plot spectra
        spectra_path = plot_spectra(wavelength, power_data, displacement)

        # Plot wavelength shift
        shift_path = plot_wavelength_shift(displacement, wavelength_shift)

        # Plot linear fit
        fit_path = plot_linear_fit(
            displacement, wavelength_shift,
            fit_results['slope'], fit_results['intercept'],
            fit_results['r_squared']
        )

        # Plot all spectra comparison (optional)
        all_spectra_path = plot_all_spectra_comparison(
            wavelength, power_data, displacement
        )

        # Step 8: Save analysis summary
        print("\n【Step 8】Saving Analysis Summary")
        summary_path = save_analysis_summary(
            displacement, dip_wavelength, wavelength_shift,
            sensitivity, fit_results['r_squared']
        )

        # Print analysis results summary
        print_summary(
            displacement, dip_wavelength, wavelength_shift,
            sensitivity, fit_results['r_squared'], performance
        )

        # Print completion message
        print("\n" + "="*70)
        print(" "*25 + "Analysis Complete!")
        print("="*70)
        print(f"\nOutput files:")
        print(f"  CSV data: {csv_path}")
        print(f"  Spectra plot: {spectra_path}")
        print(f"  Wavelength shift plot: {shift_path}")
        print(f"  Linear fit plot: {fit_path}")
        print(f"  All spectra comparison: {all_spectra_path}")
        print(f"  Analysis summary: {summary_path}")
        print("="*70 + "\n")

        return True

    except Exception as e:
        print("\n" + "="*70)
        print("Error: Exception occurred during analysis")
        print("="*70)
        print(f"Error message: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print("="*70)

        # Print detailed error traceback
        import traceback
        traceback.print_exc()

        return False


if __name__ == "__main__":
    # Run main program
    success = main()

    # Set exit code based on execution result
    if success:
        sys.exit(0)
    else:
        sys.exit(1)