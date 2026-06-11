#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wavelength Shift Calculation Module
Responsible for calculating wavelength change relative to zero displacement for each position
"""

import numpy as np
from config import get_displacement_array


def calculate_wavelength_shift(dip_wavelength):
    """
    Calculate wavelength shift (Δλ)

    Args:
        dip_wavelength: Dip wavelength array in nm

    Returns:
        numpy.ndarray: Wavelength shift array in nm

    Calculation formula:
        Δλ[n] = λ[n] - λ[0]

    Parameter explanation:
        Δλ[n]: Wavelength shift at displacement position n
        λ[n]: Dip wavelength at displacement position n
        λ[0]: Dip wavelength at zero displacement (reference)

    Physical meaning:
        Wavelength shift reflects the sensor's response sensitivity to displacement.
        Positive shift means wavelength increases with displacement,
        Negative shift means wavelength decreases with displacement.
    """
    # Dip wavelength at zero displacement as reference
    reference_wavelength = dip_wavelength[0]

    # Calculate wavelength shift
    wavelength_shift = dip_wavelength - reference_wavelength

    print("="*60)
    print("Wavelength Shift Calculation Results:")
    print("="*60)

    displacement = get_displacement_array()

    for i, (disp, shift) in enumerate(zip(displacement, wavelength_shift)):
        print(f"Displacement {disp} mm: Wavelength shift Δλ = {shift:.4f} nm")

    print("="*60)
    print(f"Reference wavelength (zero displacement): {reference_wavelength:.4f} nm")
    print(f"Wavelength shift range: {wavelength_shift.min():.4f} - {wavelength_shift.max():.4f} nm")
    print("="*60)

    return wavelength_shift


def validate_wavelength_shift(wavelength_shift):
    """
    Validate correctness of wavelength shift calculation

    Args:
        wavelength_shift: Wavelength shift array

    Returns:
        bool: Whether calculation is correct

    Check items:
        1. Wavelength shift at zero displacement must be 0
        2. Wavelength shift values should be within reasonable range (typically a few nanometers)
    """
    # Check if shift at zero displacement is 0
    if wavelength_shift[0] != 0:
        raise ValueError(
            f"Wavelength shift at zero displacement is not 0: {wavelength_shift[0]}"
        )

    # Check if wavelength shift range is reasonable (typically within a few nanometers)
    max_shift = np.abs(wavelength_shift).max()
    if max_shift > 10:  # If exceeds 10nm, there may be an issue
        print(f"Warning: Large wavelength shift value ({max_shift:.2f} nm), please check data")

    print("\nWavelength shift validation passed!")
    return True


def calculate_shift_statistics(wavelength_shift):
    """
    Calculate statistical characteristics of wavelength shift

    Args:
        wavelength_shift: Wavelength shift array

    Returns:
        dict: Statistics dictionary
    """
    displacement = get_displacement_array()

    statistics = {
        'mean_shift': np.mean(wavelength_shift),
        'std_shift': np.std(wavelength_shift),
        'max_shift': wavelength_shift.max(),
        'min_shift': wavelength_shift.min(),
        'shift_range': wavelength_shift.max() - wavelength_shift.min(),
    }

    print("\nWavelength Shift Statistics:")
    print(f"  Mean shift: {statistics['mean_shift']:.4f} nm")
    print(f"  Standard deviation: {statistics['std_shift']:.4f} nm")
    print(f"  Maximum shift: {statistics['max_shift']:.4f} nm")
    print(f"  Minimum shift: {statistics['min_shift']:.4f} nm")
    print(f"  Shift range: {statistics['shift_range']:.4f} nm")

    return statistics


def create_shift_data_dict(displacement, dip_wavelength, wavelength_shift):
    """
    Create data dictionary containing displacement, dip wavelength, and wavelength shift

    Args:
        displacement: Displacement array
        dip_wavelength: Dip wavelength array
        wavelength_shift: Wavelength shift array

    Returns:
        dict: Data dictionary
    """
    data_dict = {
        'displacement': displacement,
        'dip_wavelength': dip_wavelength,
        'wavelength_shift': wavelength_shift,
    }

    return data_dict


if __name__ == "__main__":
    # Test wavelength shift calculation
    from data_loader import load_all_data
    from dip_analysis import find_dip_wavelength

    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)

    wavelength_shift = calculate_wavelength_shift(dip_wavelength)

    # Validate calculation results
    validate_wavelength_shift(wavelength_shift)

    # Calculate statistics
    statistics = calculate_shift_statistics(wavelength_shift)

    # Create data dictionary
    displacement = get_displacement_array()
    data_dict = create_shift_data_dict(displacement, dip_wavelength, wavelength_shift)

    print(f"\nData dictionary example:")
    print(f"  Displacement: {data_dict['displacement'][:5]}")
    print(f"  Dip wavelength: {data_dict['dip_wavelength'][:5]}")
    print(f"  Wavelength shift: {data_dict['wavelength_shift'][:5]}")