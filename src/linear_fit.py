#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linear Fitting Module
Responsible for performing linear fitting on wavelength shift-displacement data and calculating sensor sensitivity
"""

import numpy as np
from config import get_displacement_array


def perform_linear_fit(displacement, wavelength_shift):
    """
    Perform linear fitting on wavelength shift-displacement data

    Args:
        displacement: Displacement array in mm
        wavelength_shift: Wavelength shift array in nm

    Returns:
        dict: Dictionary containing fitting results
            - slope: Slope (sensitivity)
            - intercept: Intercept
            - r_squared: R² value
            - y_pred: Fitted values
            - residuals: Residuals

    Fitting method:
        First-order polynomial fitting using least squares
        Python implementation: np.polyfit(displacement, wavelength_shift, 1)

    Fitting parameters:
        Slope (m): polyfit result[0]
        Intercept (b): polyfit result[1]
        Fitting equation: Δλ = m × d + b
    """
    print("="*60)
    print("Performing Linear Fitting...")
    print("="*60)

    # First-order polynomial fitting
    coefficients = np.polyfit(displacement, wavelength_shift, 1)
    slope = coefficients[0]
    intercept = coefficients[1]

    # Calculate fitted values
    y_pred = slope * displacement + intercept

    # Calculate R² value
    ss_tot = np.sum((wavelength_shift - np.mean(wavelength_shift)) ** 2)
    ss_res = np.sum((wavelength_shift - y_pred) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # Calculate residuals
    residuals = wavelength_shift - y_pred

    # Print fitting results
    print(f"Fitting equation: Δλ = {slope:.4f} × d + {intercept:.4f}")
    print(f"Slope (Sensitivity): {slope:.4f} nm/mm")
    print(f"Intercept: {intercept:.4f} nm")
    print(f"R² value: {r_squared:.4f}")

    # Evaluate fitting quality
    if r_squared > 0.95:
        print("Fitting quality: Excellent (R² > 0.95)")
    elif r_squared > 0.90:
        print("Fitting quality: Good (R² > 0.90)")
    elif r_squared > 0.80:
        print("Fitting quality: Fair (R² > 0.80)")
    else:
        print("Fitting quality: Poor (R² < 0.80), possible non-linear relationship")

    print("="*60)

    fit_results = {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'y_pred': y_pred,
        'residuals': residuals,
        'equation': f'Δλ = {slope:.4f} × d + {intercept:.4f}',
    }

    return fit_results


def calculate_sensitivity(slope):
    """
    Calculate sensor sensitivity

    Args:
        slope: Slope of linear fit

    Returns:
        float: Sensor sensitivity in nm/mm

    Physical meaning:
        Sensitivity represents the amount of wavelength change per millimeter displacement.
        Higher sensitivity means the sensor is more sensitive to small displacements.
        This is a key indicator for evaluating sensor performance.
    """
    sensitivity = slope

    print("="*60)
    print("Sensor Sensitivity Calculation Results:")
    print("="*60)
    print(f"Sensitivity: {sensitivity:.4f} nm/mm")
    print(f"Physical meaning: {sensitivity:.4f} nm wavelength change per mm displacement")
    print("="*60)

    return sensitivity


def analyze_residuals(residuals, displacement):
    """
    Analyze fitting residuals to check for non-linearity or outliers

    Args:
        residuals: Fitting residuals array
        displacement: Displacement array

    Returns:
        dict: Residual analysis results
    """
    # Calculate residual statistics
    mean_residual = np.mean(residuals)
    std_residual = np.std(residuals)
    max_residual = np.abs(residuals).max()

    # Find point with maximum residual (potential outlier)
    max_residual_idx = np.argmax(np.abs(residuals))
    max_residual_disp = displacement[max_residual_idx]

    print("\nResidual Analysis:")
    print(f"  Mean residual: {mean_residual:.4f} nm")
    print(f"  Residual standard deviation: {std_residual:.4f} nm")
    print(f"  Maximum residual: {max_residual:.4f} nm (displacement {max_residual_disp} mm)")

    # Check if residuals are randomly distributed
    if np.abs(mean_residual) < 0.001:
        print("  Residual distribution: Random (mean residual close to 0)")
    else:
        print("  Residual distribution: Possible systematic bias")

    # Check for non-linear trend
    # Check trend by examining relationship between residuals and displacement
    if len(residuals) > 5:
        # Simple check: do residuals show a clear trend?
        residual_trend = np.polyfit(displacement, residuals, 1)[0]
        if np.abs(residual_trend) > 0.01:
            print("  Warning: Residuals show trend, possible non-linear relationship")
        else:
            print("  Residual trend: No obvious trend, linear fitting is reasonable")

    analysis = {
        'mean_residual': mean_residual,
        'std_residual': std_residual,
        'max_residual': max_residual,
        'max_residual_idx': max_residual_idx,
        'max_residual_disp': max_residual_disp,
    }

    return analysis


def evaluate_sensor_performance(sensitivity, r_squared):
    """
    Evaluate sensor performance

    Args:
        sensitivity: Sensor sensitivity (nm/mm)
        r_squared: R² value of linear fit

    Returns:
        dict: Performance evaluation results
    """
    print("\nSensor Performance Evaluation:")
    print("="*60)

    # Sensitivity evaluation
    if sensitivity > 0.5:
        sensitivity_level = "High sensitivity"
        sensitivity_score = "Excellent"
    elif sensitivity > 0.1:
        sensitivity_level = "Medium sensitivity"
        sensitivity_score = "Good"
    else:
        sensitivity_level = "Low sensitivity"
        sensitivity_score = "Fair"

    print(f"Sensitivity evaluation: {sensitivity_level} ({sensitivity_score})")

    # Linearity evaluation
    if r_squared > 0.98:
        linearity_level = "Excellent linearity"
        linearity_score = "Excellent"
    elif r_squared > 0.95:
        linearity_level = "Good linearity"
        linearity_score = "Good"
    elif r_squared > 0.90:
        linearity_level = "Fair linearity"
        linearity_score = "Fair"
    else:
        linearity_level = "Poor linearity"
        linearity_score = "Poor"

    print(f"Linearity evaluation: {linearity_level} ({linearity_score})")

    # Overall evaluation
    if sensitivity_score == "Excellent" and linearity_score == "Excellent":
        overall_score = "Excellent"
    elif sensitivity_score in ["Excellent", "Good"] and linearity_score in ["Excellent", "Good"]:
        overall_score = "Good"
    else:
        overall_score = "Fair"

    print(f"Overall evaluation: {overall_score}")
    print("="*60)

    performance = {
        'sensitivity_level': sensitivity_level,
        'sensitivity_score': sensitivity_score,
        'linearity_level': linearity_level,
        'linearity_score': linearity_score,
        'overall_score': overall_score,
    }

    return performance


if __name__ == "__main__":
    # Test linear fitting functionality
    from data_loader import load_all_data
    from dip_analysis import find_dip_wavelength
    from wavelength_shift import calculate_wavelength_shift

    # Load and process data
    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)
    wavelength_shift = calculate_wavelength_shift(dip_wavelength)
    displacement = get_displacement_array()

    # Perform linear fitting
    fit_results = perform_linear_fit(displacement, wavelength_shift)

    # Calculate sensitivity
    sensitivity = calculate_sensitivity(fit_results['slope'])

    # Analyze residuals
    residual_analysis = analyze_residuals(fit_results['residuals'], displacement)

    # Evaluate sensor performance
    performance = evaluate_sensor_performance(sensitivity, fit_results['r_squared'])