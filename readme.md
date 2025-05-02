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


## 2. Organization

### 2.1. Python Project
The objective of this project is to check that all actimetric files are present, and calculate the FuncUse of the paretic and non-paretic arm and the FuncUseRatio for each patient across six months.  

### 2.2. RStudio Project
The objective of this project is to analyze the temporal variability of the FuncUseRatio metric for each patient across six months. The analysis includes visualization, reliability assessment via the Intraclass Correlation Coefficient (ICC), and variability quantification via the Coefficient of Variation (CV).  


## 3. Reference
ClinicalTrials.gov. (2024). *Actimetry Monitoring of the Paretic Upper Limb in Chronic Post Stroke. (ParUse).* https://clinicaltrials.gov/study/NCT05581602locStr=Montpellier,%20France&country=France&state=Occitanie&cit=Montpellier&cond=Stroke,%20Chronic&rank=3

Dusfour et al. (2023). Comparison of wrist actimetry variables of paretic upper limb use in post stroke patients for ecological monitoring. *Journal of NeuroEngineering and Rehabilitation.* 20:52 https://doi.org/10.1186/s12984-023-01167-y

Kleim, J. A., & Jones, T. A. (2008). Principles of experience-dependent neural plasticity: implications for rehabilitation after brain damage. *Journal of speech, language, and hearing research : JSLHR, 51*(1), S225–S239. https://doi.org/10.1044/1092-4388(2008/018) 

Leuenberger, K., Gonzenbach, R., Wachter, S. et al. (2017). Une méthode pour évaluer qualitativement l'utilisation des bras chez les survivants d'un AVC à domicile. *Med Biol Eng Comput 55,* 141-150. https://doi.org/10.1007/s11517-016-1496-7

Taub, E., Miller, N. E., Novack, T. A., Cook, E. W., Fleming, W. C., Nepomuceno, C. S., Connell, J. S., & Crago, J. E. (1993). *Technique to improve chronic motor deficit after stroke. Archives of Physical Medicine and Rehabilitation, 74*(4), 347‐354. https://pubmed.ncbi.nlm.nih.gov/8466415/
#
