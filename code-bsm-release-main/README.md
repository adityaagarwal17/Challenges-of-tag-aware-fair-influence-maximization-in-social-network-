# Code and Data for "Balancing Utility and Fairness in Submodular Maximization"

This repository contains the source code and data of our paper "Balancing Utility and Fairness in Submodular Maximization". All algorithms are implemented in Python 3.

## Datasets

This repository provides all datasets used in the experiments except Pokec (from <https://snap.stanford.edu/data/soc-pokec.html>, which is too large to be uploaded). If you need the processed Pokec dataset, feel free to contact [Yanhao Wang](mailto:yhwang@dase.ecnu.edu.cn).

## Instructions

### Prerequisites

The following libraries should be installed properly for the experiments.

1. Python 3.x;
2. Gurobi Optimizer 9.x (<https://www.gurobi.com/products/gurobi-optimizer/>) for BSM-Optimal;
3. NumPy 1.20+ (<https://numpy.org/>);
4. NetworkX 2+ (<https://networkx.org/>);
5. Matplotlib 3+ (<https://matplotlib.org/>).

### Usage

Folders:

- `data/` contains all datasets in the experiments.

- `facility_loc/` contains the code for facility location algorithms.

- `inf_max/` contains the code for influence maximization algorithms.

- `max_cover/` contains the code for maximum coverage algorithms.

- `result/` stores the output of experiments.

Scripts for the experiments:

`python3 run_xx_yy.py`

where `xx` for application and `yy` for dataset specification.

e.g., to run the experiments for facility location on the Adult dataset with gender-based group partitioning (`attr1`):

`python3 run_fl_adult_attr1.py`

## Contact

Please contact [Yanhao Wang](mailto:yhwang@dase.ecnu.edu.cn) for any question on this repository.
