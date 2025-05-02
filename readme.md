# R and Python project for Master’s internship 
_____________

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


For each patient and each month:
- `left.csv` and `right.csv` : 7-day actimetric data from each patient's arm
    - Column 0: time stamp (YYYY-MM-DD HH:MM:SS.SSS)
    - Column 1, 2 and 3: acceleration of x, y and z axes
      - Sampling frequency: 50 Hz
      - Amplitude range: - 8 g, + 8 g
      - Acceleration unit: g  

The data is not available on GitHub because the files are too large. To obtain the data, please contact marion.granier02@etu.umontpellier.fr


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
#
