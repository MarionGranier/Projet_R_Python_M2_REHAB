# R and Python project for Master’s internship 
_____________
# Actimetry and use of the paretic upper limb in post-stroke patients

## Scientific problem
A stroke is an acquired brain injury that occurs due to the obstruction or hemorrhage of a blood vessel. It is the leading cause of acquired disability in France.
Depending on the location and extent of the affected area, the consequences of a stroke vary. One of the main consequences is motor impairment of the upper limb, known as paresis. 80% of hemiparetic individuals experience difficulties in performing daily life activities (Dusfour, 2023). According to Kleim and Jones (2008), motor recovery of the paretic upper limb is enhanced by its use, whereas if the arm is not used, functional abilities are lost: “Use it and improve it, or lose it.” After returning home, the goal is to use the paretic arm as much as possible. However, due to motor impairment, using the paretic arm requires increased effort and is often associated with failures and harmful compensatory movements. This leads to learned non-use of the arm (Taub et al., 2006).

### Aim:
The primary objective of this study is to investigate whether the intra-individual variability of the FuncUseRatio, measured over one week in chronic-phase post-stroke patients, is significantly different over six consecutive months, based on accelerometric measurements in an ecological setting.

### Method:
Each participant wore an AX3 accelerometer (Axivity, Newcastle Helix, England, https://axivity.com/product/ax3) on each wrist at home for 7 days per month over six consecutive months. During these 7 days of accelerometer wear, participants were required to complete an activity journal, recording the start and end times of each activity performed. After each meal, they had to rate their fatigue using a Visual Analog Scale (VAS). The wristbands containing the accelerometers were not to be removed during the 7-day recording period.

### Participants:
5 hemiparetic patients in the chronic phase of stroke.

### Outcome measure:
FuncUse: amount of functional arm movements   

$\text{FuncUseRatio} = \frac{\text{FuncUse of paretic UL}}{\text{paretic and non-paretic UL FuncUse}} \times 100$


### Results of analysis:
Analysis in progress...

## Data organization

### Participants data:
`participants_X.csv`:   
- `X` is the ID of the month of record (`0` = first month ; `1` = second month ; `2` = third month ; `3` = fourth month ; `4` = fifth month ; `5` = sixth month)
- The file contains, for each patient, their anonymous ID, the start and end date of recording, the sampling frequency, their age, their laterality, the number of months post-stroke, the paretic side, the Fugl-Meyer (FM) score (/66), the Barthel score (/100), the Box and Blocks test (bbt) scores.

### Actimetry data: 
For each patient and each month:
- `left_ymd.csv` and `right_ymd.csv`: 7-day actimetric data from each patient's arm
    - Column 0: time stamp (YYYY-MM-DD HH:MM:SS.SSS)
    - Column 1, 2 and 3: acceleration of x, y and z axes
      - Sampling frequency: 50 Hz
      - Amplitude range: - 8 g, + 8 g
      - Acceleration unit: g
- `left.cwa` and `right.cwa`: 7-day actimetric data from each patient's arm
    - Column 0: time stamp (YYYY-MM-DD HH:MM:SS.SSS)
    - Column 1, 2 and 3: acceleration of x, y and z axes
      - Sampling frequency: 50 Hz
      - Amplitude range: - 8 g, + 8 g
      - Acceleration unit: g
    - Column 4: temperature in degree Celsius (°C)
    - Column 5: light in lux (lx)

## Notebooks organization
`is_data_exploitable.ipynb`:     
- **Aim**: Checks that the actimetric data is present and exploitable (the data cannot be used if the exposure time is less than 5 days). 
- **Input**: `right.cwa` or `left.cwa`  
- **Output**: present or not present, exploitable or not exploitable (number of days of wearing)

## Results organization
No results available yet...

## Reference
ClinicalTrials.gov. (2024). Actimetry Monitoring of the Paretic Upper Limb in Chronic Post Stroke. (ParUse). [https://clinicaltrials.gov/study/NCT05581602locStr=Montpellier,%20France&country=France&state=Occitanie&cit=Montpellier&cond=Stroke,%20Chronic&rank=3 ](https://clinicaltrials.gov/study/NCT05581602?locStr=Montpellier,%20France&country=France&state=Occitanie&city=Montpellier&cond=Stroke,%20actimetry&rank=1)
#
