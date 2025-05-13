# R and Python project for Master’s internship 
_____________
# Actimetry and use of the paretic upper limb in post-stroke patients

## 1. Scientific problem
### 1.1. Context
A stroke is an acquired brain injury caused by either the obstruction or hemorrhage of a blood vessel. It is the leading cause of acquired disability in France. Depending on the location and extent of the damage, the consequences of a stroke vary. One of the main consequences is upper limb motor impairment, known as paresis. Approximately 80% of hemiparetic individuals experience difficulties in performing daily life activities (Dusfour, 2023).  
According to Kleim and Jones (2008), motor recovery of the paretic upper limb improves with use, whereas non-use leads to loss of functional capacity: “Use it and improve it, or lose it.” After returning home, it is crucial for patients to use the paretic arm as much as possible. However, due to motor limitations, using the paretic arm requires greater effort and is often associated with failures and harmful compensatory movements. This fosters a phenomenon known as learned non-use (Taub et al., 2006).  

What we are looking for: Quantify the use of the paretic arm and assess nonuse at home with a reproducible and reliable measure.  

### 1.2. Aim
The aim of this study is to examine the intrapersonal variability of the FuncUseRatio, a metric that quantifies the functional use of the paretic upper limb based on accelerometric measurements in an ecological setting, over a six-month period in chronic post-stroke individuals to validate his reliability.

### 1.3. Method
Each participant wore an AX3 accelerometer (Axivity, Newcastle Helix, England, https://axivity.com/product/ax3) on each wrist at home for 7 consecutive days per month over six months. During these periods, participants were required to complete an activity journal, recording the start and end times of each activity performed. The wristbands containing the accelerometers were not removed during the 7-day recording period.

### 1.4. Participants
Five hemiparetic chronic-phase post-stroke patients participated in this study.

### 1.5. Outcome measure

$\text{FuncUseRatio} = \frac{\text{FuncUse of paretic UL}}{\text{paretic and non-paretic UL FuncUse}}$

*where FuncUse is the number of functional movements made with the arms. A functional movement of the upper limb satisfies two conditions: the arm elevation angle must be greater than 30°, and the movement must occur within a range of -30° to +30° around the horizontal plane (Leuenberger, 2017).*  

## 2. Python project  

### 2.1. Aim  
The objective of this project is to check that all actimetric files are present, and calculate the FuncUse of the paretic and non-paretic arm and the FuncUseRatio for each patient across six months.  

### 2.2. Data organization

#### 2.2.1. Participants data
`participants_X.csv` :   
- `X` is the ID of the month of record (from `1` = first month to `6` = sixth month)
- The file contains, for each patient: 
    - `folder_name` : Patient ID (e.g., C1P30 corresponding to investigation center 1 and the 30th patient included in the study)
    - `is_patient` : Patient (True) or healthy subject (False)
    - `parent_folder` : Actimetric data folder name
    - `paretic_side` : Right or left paretic side
    - `start_day`, `start_month`, `start_year` : Start date of recording
    - `end_day`, `end_month`, `end_year` : End date of recording
    - `age` : Subject's age on the day of inclusion
    - `FMScore` : The Fugl-Meyer score (upper-limb function, /66)
    - `freq` : Sampling frequency
    - `time_stroke` : Number of months post-stroke
    - `laterality` : Laterality
    - `barthel` : Barthel score (autonomy index, /100)
    - `bbt_paretic` and `bbt_non_paretic` : Box and Block test scores (gross motor function)

#### 2.2.2. Actimetry data 
For each patient and each month:
- `left.csv` and `right.csv` : 7-day actimetric data from each patient's arm
    - Column 0: time stamp (YYYY-MM-DD HH:MM:SS.SSS)
    - Column 1, 2 and 3: acceleration of x, y and z axes
      - Sampling frequency: 50 Hz
      - Amplitude range: - 8 g, + 8 g
      - Acceleration unit: g  

The data is not available on GitHub because the files are too large. To obtain the data, please click on this link grosfi.ch/AmHAFsek8cb (the link expires on May 29, 2025) or contact marion.granier02@etu.umontpellier.fr

### 2.3. Notebooks organization  
In this Jupyter notebook, we check if all actimetrics data csv files are present and we calculate the FuncUse of the paretic and non-paretic arms, along with their ratio for each day, for all patients and all months.  

`check_data.ipynb` :     
- **Aim**: Checks that the actimetric data csv file is present. 
- **Input**: 
    - `participants_X.csv` in `data` folder
    - `right.csv` and `left.csv` in `data` → `data_actimetry` → `CXPXX_MX` folder
- **Output**: Present or not present.

`analysis_all_patients.ipynb` :
- This script is inspired by Victor Fernando Lopes De Souza's script.
- **Aim**: Calculate FuncUseRatio for each patient and each wearing day.
- **Input**: 
    - `participants_X.csv` in `data` folder
    - `right.csv` and `left.csv` in `data` → `data_actimetry` → `CXPXX_MX` folder
- **Output**:
    - `results_FuncUsePerDay_all_patients.csv` saved in `results`: FuncUse and FuncUseRatio per day for all patients
    - `results_FuncUsePerDay_all_patients_filtered.csv` saved in `results`: FuncUse and FuncUseRatio per day of enough wearing for all patients

## 3. RStudio Project

### 3.1. Aim 
The objective of this project is to analyze the temporal variability of the FuncUseRatio metric for each patient across six months. The analysis includes visualization, reliability assessment via the Intraclass Correlation Coefficient (ICC), and variability quantification via the Coefficient of Variation (CV).

### 3.2. Data organization
**File:** `results_FuncUsePerDay_all_patients_filtered.csv`  
**Columns:**  
- `ID` : Patient ID (e.g., C1P30 corresponding to investigation center 1 and the 30th patient included in the study)  
- `month` : Month of recording (from 1 = first month to 6 = sixth month)  
- `day` : Day of recording (from 1 = first day to 8 = eighth day)  
- `FuncUse_non_paretic_day` : Number of functional movements of the non-paretic arm  
- `FuncUse_paretic_day` : Number of functional movements of the paretic arm  
- `FuncUseRatio_day` : Daily FuncUseRatio 

### 3.3. Script organization
#### 3.3.1. Visualization of daily FuncUseRatio distributions
- **Aim:** To visualize the distribution of dailies FuncUseRatio for each patient over the six months.
- **Input:** `results_FuncUsePerDay_all_patients_filtered.csv` in `data` folder
- **Output:** `boxplot_FuncUseRatio_CXPXX.png` saved in the `results` folder: Boxplots showing the distribution of dailies FuncUseRatio across the six months for each patient.  

#### 3.3.2. Intraclass Correlation Coefficient (ICC)
- **Aim:** To measure the reliability of FuncUseRatio values over six months by quantifying the consistency of repeated measurements for the same patient.
- **Input:** `results_FuncUsePerDay_all_patients_filtered.csv` in `data` folder
- **Calculation:**  ICC(2,1) model is used, which assumes that the subjects and the months are a random effect.  

$\text{ICC(2,1)} = \frac{MS_R - MS_E}{MS_R + (k - 1) \cdot MS_E + \frac{k}{n} (MS_C - MS_E)}$  

*where:*    
$MS_R$ *is the variance between subjects*  
$MS_C$ *is the variance between FuncUseRatio across months*  
$MS_E$ *is the residual error variance*  
$n$ *is the number of subjects*  
$k$ *is the number of FuncUseRatio across months per subject*   
- **Output:**  ICC value and 95% confidence interval, indicating the degree of agreement between FuncUseRatio measurements across months.  

#### 3.3.3. Coefficient of Variation (CV)
- **Aim:** To assess the relative dispersion of FuncUseRatio measurements by calculating the ratio between the standard deviation and the mean.
- **Input:** `results_FuncUsePerDay_all_patients_filtered.csv` in `data` folder
- **Calculation:** 
$CV = \frac{\sigma}{\mu} \times 100$

*where:*  
$\sigma$ *is the standard deviation of FuncUseRatio measurements*  
$\mu$ *is the mean of FuncUseRatio.*  
- **Output:** CV value for each patient, indicating the degree of variability in FuncUseRatio measurements across months.

### 3.4. Conclusion
The analysis of the FuncUseRatio over six consecutive months in post-stroke patients reveals that:

- The ICC value demonstrates good test-retest reliability (ICC between 0.75 and 0.9), indicating that the FuncUseRatio remains highly stable over time within each patient. 

- The CV values are below 10% for two patients and between 10 and 20% for two other patients, indicating low to moderate intra-individual relative variability.  

Together, these results support the conclusion that FuncUseRatio is a consistent and reliable metric for assessing upper limb use in daily life among chronic stroke patients. This is consistent with the fact that, in the absence of intervention, motor deficits tend to remain relatively stable in the chronic phase of stroke.  
It may serve as a valuable outcome metric for long-term monitoring of spontaneous arm use at home.

## 4. Reference
ClinicalTrials.gov. (2024). *Actimetry Monitoring of the Paretic Upper Limb in Chronic Post Stroke. (ParUse).* https://clinicaltrials.gov/study/NCT05581602locStr=Montpellier,%20France&country=France&state=Occitanie&cit=Montpellier&cond=Stroke,%20Chronic&rank=3

Dusfour et al. (2023). Comparison of wrist actimetry variables of paretic upper limb use in post stroke patients for ecological monitoring. *Journal of NeuroEngineering and Rehabilitation.* 20:52 https://doi.org/10.1186/s12984-023-01167-y

Kleim, J. A., & Jones, T. A. (2008). Principles of experience-dependent neural plasticity: implications for rehabilitation after brain damage. *Journal of speech, language, and hearing research : JSLHR, 51*(1), S225–S239. https://doi.org/10.1044/1092-4388(2008/018) 

Leuenberger, K., Gonzenbach, R., Wachter, S. et al. (2017). Une méthode pour évaluer qualitativement l'utilisation des bras chez les survivants d'un AVC à domicile. *Med Biol Eng Comput 55,* 141-150. https://doi.org/10.1007/s11517-016-1496-7

Taub, E., Miller, N. E., Novack, T. A., Cook, E. W., Fleming, W. C., Nepomuceno, C. S., Connell, J. S., & Crago, J. E. (1993). *Technique to improve chronic motor deficit after stroke. Archives of Physical Medicine and Rehabilitation, 74*(4), 347‐354. https://pubmed.ncbi.nlm.nih.gov/8466415/
#
