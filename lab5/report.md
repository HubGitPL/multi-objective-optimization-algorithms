# Lab 5 - report


## Setup

3 algorithms x 7 problems x 20 runs. Same N and maxFE for every
algorithm so comparison is fair. Metrics: GD, IGD, HV. Statistical test:
Wilcoxon signed-rank at typical alpha = 0.05.

Algorithms:

- NSGAII_Roul
- NSGAII 
- MOEA/D

Problems: Cylinder, ZDT3, ZDT4, DTLZ3, DTLZ4, WFG3, WFG4.

Symbols in the tables compare each algorithm against NSGAII_Roul:

## Results

### GD

| Problem  | NSGAII_Roul         | NSGAII                  | MOEA/D                  |
|----------|---------------------|-------------------------|-------------------------|
| Cylinder | 4.62e+01 ± 1.5e+01  | 3.96e+01 ± 9.4e+00 (=)  | 7.13e+01 ± 4.4e+01 (=)  |
| ZDT3     | 3.24e-02 ± 8.7e-03  | 2.81e-02 ± 6.1e-03 (=)  | 1.66e-01 ± 5.6e-02 (+)  |
| ZDT4     | 8.46e-01 ± 4.1e-01  | 1.03e+00 ± 4.8e-01 (=)  | 9.18e-01 ± 5.5e-01 (=)  |
| DTLZ3    | 7.59e+00 ± 2.2e+00  | 9.57e+00 ± 2.4e+00 (+)  | 8.11e+00 ± 2.5e+00 (=)  |
| DTLZ4    | 1.64e-03 ± 1.6e-03  | 2.21e-03 ± 1.3e-03 (=)  | 5.90e-04 ± 7.1e-04 (=)  |
| WFG3     | 9.49e-02 ± 1.0e-02  | 9.75e-02 ± 1.3e-02 (=)  | 1.60e-01 ± 1.2e-02 (+)  |
| WFG4     | 2.08e-02 ± 1.9e-03  | 1.80e-02 ± 2.6e-03 (-)  | 2.49e-02 ± 2.9e-03 (+)  |

### IGD

| Problem  | NSGAII_Roul         | NSGAII                  | MOEA/D                  |
|----------|---------------------|-------------------------|-------------------------|
| Cylinder | 1.00e+03 ± 1.3e+02  | 9.86e+02 ± 1.1e+02 (=)  | 1.20e+03 ± 1.3e+02 (+)  |
| ZDT3     | 1.92e-01 ± 4.0e-02  | 1.70e-01 ± 2.8e-02 (=)  | 8.92e-01 ± 2.2e-01 (+)  |
| ZDT4     | 2.32e+00 ± 9.9e-01  | 2.71e+00 ± 9.7e-01 (=)  | 2.82e+00 ± 1.3e+00 (=)  |
| DTLZ3    | 2.32e+01 ± 5.5e+00  | 3.24e+01 ± 9.2e+00 (+)  | 3.83e+01 ± 1.4e+01 (+)  |
| DTLZ4    | 4.48e-01 ± 2.9e-01  | 2.76e-01 ± 2.2e-01 (=)  | 6.07e-01 ± 3.7e-01 (=)  |
| WFG3     | 2.59e-01 ± 4.4e-02  | 2.45e-01 ± 3.6e-02 (=)  | 5.61e-01 ± 1.5e-01 (+)  |
| WFG4     | 4.05e-01 ± 2.0e-02  | 4.01e-01 ± 2.0e-02 (=)  | 4.04e-01 ± 1.8e-02 (=)  |

### HV 

| Problem  | NSGAII_Roul         | NSGAII                  | MOEA/D                  |
|----------|---------------------|-------------------------|-------------------------|
| Cylinder | 5.13e-01 ± 1.0e-03  | 5.13e-01 ± 8.7e-04 (=)  | 5.11e-01 ± 4.0e-03 (=)  |
| ZDT3     | 4.66e-01 ± 5.6e-02  | 4.82e-01 ± 3.6e-02 (=)  | 4.24e-02 ± 4.1e-02 (+)  |
| ZDT4     | 1.23e-02 ± 4.0e-02  | 0.00e+00 ± 0.0e+00 (=)  | 0.00e+00 ± 0.0e+00 (=)  |
| DTLZ3    | 0.00e+00 ± 0.0e+00  | 0.00e+00 ± 0.0e+00 (=)  | 0.00e+00 ± 0.0e+00 (=)  |
| DTLZ4    | 3.55e-01 ± 1.3e-01  | 4.32e-01 ± 8.0e-02 (-)  | 2.71e-01 ± 1.9e-01 (=)  |
| WFG3     | 3.13e-01 ± 2.0e-02  | 3.21e-01 ± 1.7e-02 (=)  | 1.96e-01 ± 5.0e-02 (+)  |
| WFG4     | 4.47e-01 ± 8.6e-03  | 4.59e-01 ± 1.2e-02 (-)  | 4.40e-01 ± 1.0e-02 (=)  |

## Short analysis

Out of 21 cells, my NSGAII_Roul is statistically
the same as the original NSGAII in 16 of them. So switching tournament
selection for roulette wheel and dropping crowding distance from the mating
step doesn't break the algorithm.

HV is zero on ZDT4 and DTLZ3 for everyone, none of the algorithms got close
enough to the true front with only 3000 evaluations.

## Conclusions

- Replacing tournament with roulette wheel and using only FrontNo for the
  mating selection is not as harmful as I expected, in most cases the
  result is the same as the original NSGA-II.
- MOEA/D is the weakest of the three on this benchmark suite.
- HV can collapse to zero on hard problems.


