#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dip Wavelength Analysis Module
Responsible for calculating dip wavelength (wavelength corresponding to minimum power) for each displacement position
"""

import numpy as np
from config import NUM_MEASUREMENTS, get_displacement_array


def find_dip_wavelength(wavelength, power_data):
    """
    Find the wavelength corresponding to minimum power for each displacement position

    Args:
        wavelength: Wavelength array in nm
        power_data: Power data matrix with shape=(number of wavelength points, number of displacement points)

    Returns:
        numpy.ndarray: Dip wavelength array with length equal to number of displacement points, unit: nm

    Physical meaning:
        Dip wavelength is the wavelength corresponding to the minimum power in the spectral curve.
        This is the characteristic wavelength where the sensor responds to displacement changes.
        When the sensor is displaced, the dip wavelength shifts accordingly.
    """
    dip_wavelength = np.zeros(NUM_MEASUREMENTS)

    print("="*60)
    print("Calculating Dip Wavelength...")
    print("="*60)

    for i in range(NUM_MEASUREMENTS):
        # Find index of minimum power
        min_index = np.argmin(power_data[:, i])

        # Get corresponding wavelength
        dip_wavelength[i] = wavelength[min_index]

        # Get minimum power value
        min_power = power_data[min_index, i]

        print(f"Displacement point {i+1}: Dip wavelength = {dip_wavelength[i]:.4f} nm, "
              f"Minimum power = {min_power:.4f} dBm")

    print("="*60)
    print("Dip Wavelength calculation complete!")
    print("="*60)

    return dip_wavelength


def analyze_dip_characteristics(wavelength, power_data, dip_wavelength):
    """
    Analyze dip characteristics including minimum power and wavelength range

    Args:
        wavelength: Wavelength array
        power_data: Power data matrix
        dip_wavelength: Dip wavelength array

    Returns:
        dict: Dictionary containing dip characteristic information
    """
    displacement = get_displacement_array()

    # Get minimum power value for each displacement point
    min_powers = np.zeros(NUM_MEASUREMENTS)
    for i in range(NUM_MEASUREMENTS):
        min_powers[i] = np.min(power_data[:, i])

    # Calculate dip wavelength range
    dip_range = dip_wavelength.max() - dip_wavelength.min()

    characteristics = {
        'displacement': displacement,
        'dip_wavelength': dip_wavelength,
        'min_power': min_powers,
        'dip_wavelength_range': dip_range,
        'dip_wavelength_min': dip_wavelength.min(),
        'dip_wavelength_max': dip_wavelength.max(),
    }

    print("\nDip characteristics analysis:")
    print(f"  Dip wavelength range: {dip_range:.4f} nm")
    print(f"  Minimum dip wavelength: {dip_wavelength.min():.4f} nm (displacement={displacement[dip_wavelength.argmin()]} mm)")
    print(f"  Maximum dip wavelength: {dip_wavelength.max():.4f} nm (displacement={displacement[dip_wavelength.argmax()]} mm)")
    print(f"  Average minimum power: {min_powers.mean():.4f} dBm")

    return characteristics


def check_multiple_minima(wavelength, power_data, tolerance=0.001):
    """
    Check for multiple minimum power points

    Args:
        wavelength: Wavelength array
        power_data: Power data matrix
        tolerance: Tolerance for determining multiple minima (dBm)

    Returns:
        list: List of displacement point indices with multiple minima
    """
    multiple_minima_indices = []

    for i in range(NUM_MEASUREMENTS):
        min_power = np.min(power_data[:, i])
        # Find all points close to minimum
        min_indices = np.where(
            np.abs(power_data[:, i] - min_power) < tolerance
        )[0]

        if len(min_indices) > 1:
            multiple_minima_indices.append(i)
            print(f"Warning: Displacement point {i+1} has {len(min_indices)} points close to minimum")

    return multiple_minima_indices


if __name__ == "__main__":
    # Test dip wavelength calculation
    from data_loader import load_all_data

    wavelength, power_data = load_all_data()
    dip_wavelength = find_dip_wavelength(wavelength, power_data)

    print(f"\nDip wavelength array: {dip_wavelength}")

    # Analyze dip characteristics
    characteristics = analyze_dip_characteristics(wavelength, power_data, dip_wavelength)

    # Check for multiple minima
    multiple_minima = check_multiple_minima(wavelength, power_data)
    if multiple_minima:
        print(f"\nDisplacement points with multiple minima: {multiple_minima}")