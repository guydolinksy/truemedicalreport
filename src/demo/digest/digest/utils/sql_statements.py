query_treatment = """
SELECT 
p.ev_MedicalRecord AS MedicalRecord,
p.Treatmant_Decision AS Decision,
p.Treatment_UnitName AS UnitName
FROM dbo.patient_info_plus p
WHERE p.ev_Unit = {unit}
AND p.End_Date is NULL
AND p.Delete_Date is NULL
"""

query_patient_admission = """
SELECT 
p.ev_MedicalRecord as MedicalRecord,
concat(p.First_Name,' ',p.Last_Name ) AS FullName,
p.Birth_Date AS BirthDate,
p.Gender AS Gender,
p.ESI AS ESI,
p.MainCause AS MainCause,
p.BedName AS BedName,
p.RoomName AS RoomName,
p.UnitName AS UnitName,
p.Admission_Date AS AdmissionDate,
p.End_Date
FROM dbo.patient_info_plus p
WHERE p.ev_Unit = {unit}
AND p.End_Date IS NULL
AND p.Delete_Date IS NULL
"""

query_measurements = """
SELECT
    CONCAT(m.Device_monitor_Parameter, '#', m.Device_monitor_date) AS MeasureID,
    m.ev_MedicalRecord AS MedicalRecord,
    m.Device_monitor_result AS Result,
    m.Monitoring_Min_Value AS MinValue,
    m.Monitoring_Max_Value AS MaxValue,
    m.Device_monitor_date AS At,
    m.Device_monitor_Parameter AS Code
FROM dbo.measurements m
join [dbo].[patient_info_plus] p on m.ev_MedicalRecord = p.ev_MedicalRecord
WHERE p.ev_Unit = {unit}
AND p.End_Date is NULL
AND p.Delete_Date is NULL
AND m.Device_monitor_Parameter IN ({codes})
"""

query_images = """
SELECT
    i.TestOrders_Order_Num AS OrderNumber,
    i.TestOrders_Test_Date AS OrderDate,
    i.ev_MedicalRecord AS MedicalRecord,
    i.AuxTest_Name as TestName,
    i.TestOrders_Order_Status as OrderStatus,
    i.TestDates_Result AS Result,
    i.TestDates_Panic AS Panic
FROM images i 
join [dbo].[patient_info_plus] p on i.ev_MedicalRecord = p.ev_MedicalRecord
WHERE
   i.TestOrders_Delete_Date IS NULL
    AND i.TestOrders_Test_Date > p.Admission_Date
    AND p.End_Date IS NULL 
    AND p.ev_Unit = {unit} 
"""

query_referrals = """
SELECT 
p.ReferralID AS ReferralId,
p.ev_MedicalRecord AS MedicalRecord,
p.ReferralDate AS ReferralDate,
p.Referral_MedicalLicense AS MedicalLicense,
p.Referral_Title As Title,
p.Referral_FirstName AS FirstName,
p.Referral_LastName AS LastName
FROM dbo.patient_info_plus p
WHERE p.ev_Unit = {unit}
AND p.End_Date IS NULL
AND p.Delete_Date IS NULL
"""

query_labs = """
SELECT 
p.ev_MedicalRecord AS MedicalRecord,
l.LR_Test_code AS TestCode,
l.Lab_Headline_Name AS Category, 
l.LR_Test_Name AS TestName,
concat(l.LR_Result,' ',l.LR_Units)  AS Result,
l.LR_Norm_Minimum AS NormMinimum,
l.LR_Norm_Maximum AS NormMaximum,
l.LR_Result_Date AS OrderDate,
l.LR_Result_Entry_Date AS ResultTime
FROM Labs l 
join  [dbo].[patient_info_plus] p on l.ev_MedicalRecord = p.ev_MedicalRecord
WHERE
l.LR_Delete_Date IS NULL
AND l.LR_Result_Date >= p.Admission_Date
AND p.End_Date IS NULL 
AND p.ev_Unit = {unit} 
AND p.Delete_Date IS NULL
"""

query_doctor_intake = """
SELECT 
P.ev_MedicalRecord AS MedicalRecord,
P.Doctor_intake_MedicalText AS MedicalText,
P.Doctor_intake_Time AS DocumentingTime
FROM dbo.patient_info_plus p
WHERE p.ev_Unit = {unit}
AND p.End_Date IS NULL
AND p.Delete_Date IS NULL
"""

query_nurse_intake = """
SELECT 
 p.ev_MedicalRecord AS MedicalRecord,
 p.Nurse_Remarks_Text AS MedicalText,
 p.Nurse_Remarks_Entry_Date AS DocumentingTime
FROM dbo.patient_info_plus p
WHERE p.ev_Unit = {unit}
AND p.End_Date IS NULL
AND p.Delete_Date IS NULL
"""
