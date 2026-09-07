# Ab initio modeling of GaN: phonon-limited carrier mobility with Quantum ESPRESSO and EPW

First-principles calculation of the electronic structure, phonon dispersion and phonon-limited
electron and hole mobility of bulk wurtzite GaN. The workflow runs through Quantum ESPRESSO:
variable-cell relaxation, self-consistent DFT, density-functional perturbation theory for the
phonons and the electron–phonon matrix elements on coarse grids, Wannier interpolation of both
to fine grids with the EPW module, and an iterative solution of the Boltzmann transport equation
for the temperature-dependent mobility. The complete set of input files, job scripts and
pseudopotentials for the LDA calculation and for a later PBE rerun is included, together with
the interpolated band and phonon data, the converged mobility output and the figures. The
write-up is in [`docs/report.pdf`](docs/report.pdf).

![GaN band structure, LDA](results/lda/band_structure.png)

## Background

GaN is a wide-bandgap III–V semiconductor with a direct gap of about 3.4 eV [1] and the
material of choice for high-power and high-frequency devices, whose switching characteristics
are governed by carrier mobility. Phonon scattering sets the intrinsic upper limit of that
mobility, and computing it from first principles requires the electron–phonon coupling across
the whole Brillouin zone, far beyond what DFPT can afford directly. The EPW method [2, 3]
solves this by transforming the matrix elements computed on a coarse grid into a basis of
maximally localised Wannier functions, where they are short-ranged in real space, and
interpolating them to arbitrarily fine grids. The mobility then follows from the Boltzmann
transport equation [4]. Such intrinsic mobilities are the kind of input parameter that
technology computer-aided design of devices relies on.

## What is in the repository

| path | purpose |
|---|---|
| `relax/` | variable-cell relaxation of the wurtzite cell (`varicell.in`, job script, ONCV LDA pseudopotentials). |
| `lda/` | the LDA workflow: `scf.in`, `ph.in`, `nscf.in`, the EPW post-processing script `pp.py` that collects the phonon output into `save/`, the three EPW inputs (`epw1.in` Wannierization and band/phonon interpolation, `epw2.in` hole mobility, `epw3.in` electron mobility), the M–Γ–A path `MGA.txt`, the Slurm job scripts and the ONCV LDA pseudopotentials. |
| `pbe/` | the same workflow rerun with ONCV PBE pseudopotentials and denser coarse grids. |
| `results/lda/` | Wannier-interpolated bands along Γ–M, Γ–K, Γ–A (`gan_band.dat`, `.kpt`, `.labelinfo.dat`, `.gnu`), EPW bands and phonons along M–Γ–A (`band.eig`, `phband.freq`), the converged hole-mobility output (`epw_hole_mobility.out`) and the figures. |
| `results/pbe/` | interpolated bands and phonons from the PBE rerun and its band-structure figure. |
| `plot_phonon_dispersion.py` | plots `phband.freq` along the path. |
| `docs/report.pdf` | the report: theory, implementation, results and discussion. |

The input files are the working copies as left on the cluster after the last runs. Large
run-time output (wavefunctions, charge density, `dvscf` files, roughly 130 MB per run) is not
included; everything needed to regenerate it is.

## Method

Wannier functions are Fourier transforms of the Bloch states over the Brillouin zone [3],

|w_nR⟩ = (V_cell / (2π)³) ∫_BZ e^{−ik·R} |ψ_nk⟩ d³k,

localised at the lattice vectors R, so that Hamiltonian and electron–phonon matrix elements
expressed in this basis decay with |R| and can be interpolated. The coupling of an electron in
band n at k to band m at k + q through phonon mode ν is

g_mnν(k, q) = ⟨ψ_mk+q | ∂_qν V | ψ_nk⟩,

with ∂_qν V the DFPT perturbing potential. EPW computes g on the coarse grids, rotates it into
the Wannier basis, Fourier transforms it in both k and q, and interpolates it back onto fine
grids [2]. The electron–phonon scattering rate follows from Fermi's golden rule with phonon
emission and absorption,

1/τ_nk = (2π/ħ) Σ_mqν |g_mnν(k, q)|² [(1 − f_mk+q)(n_qν + 1) δ(ε_nk − ε_mk+q − ħω_qν) + …],

and the mobility from the Boltzmann transport equation, which EPW solves iteratively beyond
the relaxation-time approximation [4]. For a polar crystal the long-range (Fröhlich) part of
the coupling and the LO–TO splitting at Γ are treated separately through the dielectric tensor
and Born effective charges (`epsil` in `ph.x`, `lpolar` in EPW). Electron–phonon calculations
in EPW require norm-conserving pseudopotentials [5]; ONCV pseudopotentials are used throughout.

## Computational details

- **Cell.** Wurtzite GaN (`ibrav = 4`, four atoms), relaxed with `vc-relax` at 100 Ry cutoff on
  an 8 × 8 × 8 k-grid: a = 6.02 bohr, c/a = 1.625 against the experimental 6.026 bohr and
  1.626 [6]. These lattice parameters are used in all subsequent inputs.
- **LDA workflow** (`lda/`): SCF with 80 Ry cutoff, DFPT with `epsil = .true.` and
  `ldisp = .true.`, `pp.py` to assemble the `save/` directory, NSCF on the coarse k-grid of EPW.
  Wannierization onto 14 bands from Ga sp³ and N p projections with the 12 Ga d bands excluded
  (`bands_skipped`), band and phonon interpolation along M–Γ–A and a Wannier90 band plot along
  Γ–M, Γ–K, Γ–A. Mobility by the iterative BTE with `lpolar`, a carrier density of 10¹³ cm⁻³,
  20 × 20 × 20 fine k- and q-grids and a 0.4 eV window for holes (`epw2.in`), 30 × 30 × 30 grids
  and a 0.3 eV window for electrons (`epw3.in`).
- **PBE rerun** (`pbe/`): 8 × 8 × 8 SCF, 4 × 4 × 4 q-grid with `tr2_ph = 2 × 10⁻¹⁴`, explicit
  4 × 4 × 4 NSCF grid, 4 × 4 × 4 coarse EPW grids, thirteen temperatures from 200 to 500 K.
- Runs on a Slurm cluster with a Spack build of Quantum ESPRESSO 7.3.1 and EPW 5.8.1; the job
  scripts give the resources used for each step.

## Results

**Band structure.** The LDA calculation gives a direct gap of 2.11 eV at Γ, within 1.4 % of the
published LDA value of 2.14 eV [7] and, as expected for LDA, well below the experimental 3.4 eV.
The PBE rerun gave 1.96 eV, further from experiment; the report attributes this to the set-up
of that run and keeps it for transparency. Interpolated band energies are in
`results/lda/gan_band.dat` and `results/pbe/gan_band.dat`.

![GaN band structure, PBE rerun](results/pbe/band_structure.png)

**Phonon dispersion.** Twelve branches along M–Γ–A from the EPW interpolation, with the
LO–TO splitting at Γ from the polar correction (`results/lda/phband.freq`, frequencies as
written by EPW). The branch ordering and the gap between the acoustic and optical manifolds
follow the measured dispersion of hexagonal GaN [8].

![GaN phonon dispersion, LDA](results/lda/phonon_dispersion.png)

**Hole mobility.** Drift mobility from the iterative BTE, converged in 100 iterations to
10⁻⁶ cm²/Vs, in-plane (xx) and along c (zz):

| T (K) | μ_h in-plane (cm²/Vs) | μ_h along c (cm²/Vs) |
|---|---|---|
| 200 | 108.0 | 128.8 |
| 250 | 91.3 | 89.0 |
| 300 | 73.4 | 63.0 |
| 350 | 59.1 | 46.2 |
| 400 | 48.4 | 35.3 |
| 450 | 40.4 | 27.9 |
| 500 | 34.4 | 22.8 |

The full table in 25 K steps is at the end of `results/lda/epw_hole_mobility.out`.

![hole mobility](results/lda/hole_mobility.png)

**Electron mobility.** The in-plane electron mobility at 300 K is 841 cm²/Vs, about 32 % below
the reference experimental value of roughly 1240 cm²/Vs [9]. Both carriers show the
temperature dependence reported for GaN from the same method [10]: the electron mobility falls
from about 1500 cm²/Vs at 200 K to about 250 cm²/Vs at 500 K, and the hole mobility from
108 to 34 cm²/Vs. The agreement in functional form indicates that the electron–phonon coupling
is captured; the underestimate is attributed in the report to the sampling density of the
coarse grids and to the pseudopotential approximation.

![electron mobility](results/lda/electron_mobility.png)

## Reproducing

Each step is a Slurm job; the scripts load Quantum ESPRESSO through Spack and run the named
input. In `lda/`:

```bash
sbatch Self-consistent.sh       # pw.x  scf.in
sbatch Phonons.sh               # ph.x  ph.in  (DFPT, dielectric tensor, dvscf on the q-grid)
python pp.py < pp.in            # collect dyn and dvscf files into save/
sbatch Non-self-consistent.sh   # pw.x  nscf.in on the coarse k-grid
sbatch EPW.sh                   # epw.x with epw1.in, then epw2.in and epw3.in
```

`EPW.sh` reads `epw.in`; copy the required stage to that name before submitting. The
relaxation in `relax/` is run the same way with `Lattice_constant.sh`. The PBE rerun in `pbe/`
uses the identical sequence.

## References

[1] B. Monemar, Phys. Rev. B 10, 676 (1974).

[2] S. Poncé, E. R. Margine, C. Verdi and F. Giustino, Comput. Phys. Commun. 209, 116 (2016).

[3] F. Giustino, M. L. Cohen and S. G. Louie, Phys. Rev. B 76, 165108 (2007).

[4] S. Poncé, W. Li, S. Reichardt and F. Giustino, Rep. Prog. Phys. 83, 036501 (2020).

[5] H. Lee et al., npj Comput. Mater. 9, 156 (2023).

[6] H. Qin, X. Luan, C. Feng, D. Yang and G. Zhang, Materials 10, 1419 (2017).

[7] S. Poncé, D. Jena and F. Giustino, Phys. Rev. B 100, 085204 (2019).

[8] V. Yu. Davydov et al., Phys. Rev. B 58, 12899 (1998).

[9] M. Shur, B. Gelmont and M. Asif Khan, J. Electron. Mater. 25, 777 (1996).

[10] S. Poncé, D. Jena and F. Giustino, Phys. Rev. Lett. 123, 096602 (2019).
