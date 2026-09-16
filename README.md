# eutectics-pcr-prediction
Eutectics screening in CALPHAD databases - machine learning for primary crystallization regions prediction

#### License
This code is licensed under the MIT License. You are free to use, modify, and distribute it, provided you cite the original paper [1].

#### Dependencies
The tests were performed with the following versions:
- Python 3.12.7
- Pandas 2.2.2
- NumPy 1.26.4
- Aiphad 1.0.1
- TC-Python 2024.2.32679.198 (Licence for Thermo-Calc [2] required)
 
#### Description


This code implements a multi-step computational methodology developed in [1]:

- Primary crystallization phases are calculated via Thermo-Calc [2] for compositions strategically selected through active learning. <br>
- Phase labels are propagated and primary crystallization regions are determined using AIPHAD [3]. <br>
- Eutectic candidates are identified as intersections where *n* phases meet, with *n* corresponding to the number of elements in the system. <br>
- The identified compositions serve as starting points for Solidus descent [1] to confirm, refine, or refute the eutectic point. <br>



This code emphasizes scientific reproducibility of the method developed in [1] rather than adherence to programming best practices.

##### References
[1] K. Firdová, K. E. Borowski, R. Tamura, J.-M. Joubert, G. Deffrennes; Methods for efficient eutectic screening in CALPHAD databases <br>
[2] The Thermo-Calc Software TCAL09 Al-based Alloy Database https://thermocalc.com/products/databases/aluminum-based-alloys/ <br>
[3] R. Tamura, H. Morito, G. Deffrennes, M. Naito, Y. Nose, T. Abe, K. Terayama; AIPHAD, an active learning web application for visual understanding of phase diagrams, Commun. Mater. 5 (2024) https://doi.org/https://doi.org/10.1038/s43246-024-00580-7
