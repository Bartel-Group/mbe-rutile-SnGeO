This readme.txt file was generated on 20250128 by Nathan J. Szymanski.

Recommended citation for the data:
Liu, F., Szymanski, N. J., Noordhoek, K., Shin, H., Kim, D., Bartel, C. J., & Jalan, B. "Unraveling the Growth Dynamics of Rutile Sn1−xGexO2 Using Theory and Experiment." Nano Letters, 2025, 25, 299–305. DOI: 10.1021/acs.nanolett.4c05043

-------------------
GENERAL INFORMATION
-------------------

1. Title of dataset
Thermodynamic Free Energy Data for Ge/GeO2 Phase Stability

2. Author Information

Principal Investigator Contact Information

Name: Bharat Jalan
Institution: University of Minnesota
Address: Department of Chemical Engineering and Materials Science, Minneapolis, MN 55455
Email: bjalan@umn.edu
ORCID: 0000-0002-7940-0490
Associate or Co-Investigator Contact Information

Name: Christopher J. Bartel
Institution: University of Minnesota
Address: Department of Chemical Engineering and Materials Science, Minneapolis, MN 55455
Email: cbartel@umn.edu
ORCID: 0000-0002-5198-5036
Associate or Co-Investigator Contact Information

Name: Nathan J. Szymanski
Institution: University of Minnesota
Address: Department of Chemical Engineering and Materials Science, Minneapolis, MN 55455

3. Date published
2025-12-27

4. Date of data collection
2024-10-10 to 2024-12-18

5. Geographic location of data collection
University of Minnesota, Minneapolis, MN

6. Information about funding sources that supported the collection of the data

NSF FuSe Grant (Award #DMR-2328702)
AFOSR Grants (FA9550-21-1-0025, FA9550-23-1-0247)
University of Minnesota MRSEC program (#DMR-2011401)

7. Overview of the data (abstract)
This dataset includes thermodynamic free energy calculations for GeO2 reactions involving GeO and O2. The data provides insights into phase stability and reaction kinetics under varying conditions, supporting experimental findings in GeO2 thin-film synthesis via molecular beam epitaxy (MBE).

--------------------------
SHARING/ACCESS INFORMATION
--------------------------

1. Licenses/restrictions placed on the data
Data is shared under the University of Minnesota's Data Repository (DRUM) Terms of Use.

2. Links to publications that cite or use the data
Liu et al. "Unraveling the Growth Dynamics of Rutile Sn1−xGexO2 Using Theory and Experiment." Nano Letters, 2025.

3. Was data derived from another source?
No.

4. Terms of Use
By using these files, users agree to the DRUM Terms of Use.

---------------------
DATA & FILE OVERVIEW
---------------------

1. File List

dGf_summary.json: Thermodynamic data, including free energy (dGf) calculations for reactions involving GeO, O2, and GeO2 under varying conditions.

2. Relationship between files

All data is contained within the JSON file for free energy calculations.

--------------------------
METHODOLOGICAL INFORMATION
--------------------------

1. Description of methods used for collection/generation of data
Thermodynamic data was calculated using density functional theory (DFT) models, incorporating experimental parameters from molecular beam epitaxy (MBE) experiments.

2. Methods for processing the data
Free energy values were computed for multiple conditions using custom Python scripts and analyzed for reaction trends.

3. Instrument/software-specific information
DFT calculations: Vienna Ab Initio Simulation Package (VASP).

4. Standards and calibration information
Reaction parameters were cross-validated against experimental literature for consistency.

5. Environmental/experimental conditions
Ambient conditions and experimental conditions for MBE synthesis (e.g., substrate temperature, oxygen flux).

6. Quality-assurance procedures
N/A

7. People involved
Kyle Noordhoek and Nathan J. Szymanski

-----------------------------------------------
DATA-SPECIFIC INFORMATION FOR: dGf_summary.json
-----------------------------------------------

1. Number of variables
Three (Reactant conditions, Products, Free energy values)

2. Number of cases/rows
~100, representing different experimental and computational conditions.

3. Missing data codes
N/A

4. Variable List
Reactants: Chemical species (e.g., GeO, O2).
Products: Final products (e.g., GeO2).
Free energy values (dGf): Computed thermodynamic free energy under various conditions.
