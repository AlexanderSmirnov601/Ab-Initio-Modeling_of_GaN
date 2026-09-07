# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 08:35:42 2025

@author: user
"""

# -*- coding: utf-8 -*-
"""
Revised on Thu Dec  4 08:55:00 2025

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt

# Set global scientific style parameters
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 14,
    'axes.linewidth': 1.2,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,
    'ytick.right': True,
})

def process_band_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Skip the header line
    lines = lines[1:]
    
    coordinates = []
    bands_data = []
    
    # --- Data Parsing ---
    i = 0
    while i < len(lines):
        if lines[i].strip():  # Skip empty lines
            # Read coordinate
            coords = list(map(float, lines[i].split()))
            coordinates.append(coords)
            
            # Read 12 band values
            if i + 1 < len(lines):
                i += 1
                band_values = list(map(float, lines[i].split()))
                bands_data.append(band_values)
        i += 1
    
    coordinates = np.array(coordinates)
    bands_data = np.array(bands_data)
    
    # --- Scientific Path Calculation ---
    # Calculate cumulative distance along the k-path (Euclidean distance between points)
    # This is more accurate than distance from origin for complex paths
    x_coords = [0.0]
    for i in range(1, len(coordinates)):
        dist = np.linalg.norm(coordinates[i] - coordinates[i-1])
        x_coords.append(x_coords[-1] + dist)
    
    x_coords = np.array(x_coords)
    
    # --- Identify High Symmetry Points for Ticks ---
    tick_locs = []
    tick_labels = []
    
    # Find points where coordinate is [0, 0, 0] (Gamma)
    # You can add elif blocks here to detect other points like X, M, K if needed
    for i, coord in enumerate(coordinates):
        if np.allclose(coord, [0, 0, 0]):
            tick_locs.append(x_coords[i])
            tick_labels.append(r'$\Gamma$') # LaTeX formatting for Gamma
            
    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot the 12 bands
    for band_idx in range(12):
        ax.plot(x_coords, bands_data[:, band_idx], 
                color='black', 
                linewidth=0.8, 
                alpha=0.9)
    
    # Configure X-Axis Ticks (The "Scientific" way)
    # This replaces the numerical x-axis with the Symmetry labels
    if tick_locs:
        ax.set_xticks(tick_locs)
        ax.set_xticklabels(tick_labels)
        
        # Add vertical grid lines exactly at the symmetry points
        for tick in tick_locs:
            ax.axvline(x=tick, color='gray', linestyle='--', linewidth=0.6, alpha=0.5)

    # Labels and Limits
    ax.set_xlabel(r'Wave vector along path ($2\pi/a$)') # LaTeX formatted
    ax.set_ylabel(r'Frequency (cm$^{-1}$)')
    
    ax.set_xlim(min(x_coords), max(x_coords))
    
    plt.tight_layout()
    plt.show()
    
    return x_coords, bands_data

# Usage
x_coords, bands = process_band_data('C:/Users/user/Desktop/phband.freq')