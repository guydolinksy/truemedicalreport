query_treatment = """
SELECT
    ev.Medical_Record AS MedicalRecord,
    de.Answer_Text AS Decision,
    su.Name AS UnitName
FROM [chameleon].[dbo].[EmergancyVisits] AS ev
LEFT JOIN [chameleon].[dbo].[RoomPlacmentPatient] AS rpp
    ON ev.Medical_Record = rpp.Medical_Record
LEFT JOIN [chameleon].[dbo].[AdmissionTreatmentDecision] AS atd
    ON ev.Medical_Record = atd.Medical_Record and atd.delete_date is null
LEFT JOIN [chameleon].[dbo].[V_TableAnswers] AS de
    ON de.Table_Code = 1092 AND de.Answer_Code = atd.Decision AND rpp.Unit = de.Unit
LEFT JOIN [chameleon].[dbo].[SystemUnits] AS su
    ON atd.Hosp_Unit = su.Unit
WHERE
    ev.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND rpp.Unit = {unit}
            AND ev.Release_Time is null
            AND atd.Delete_Date is null
 """

query_patient_admission = """
SELECT
    ev.Medical_Record as MedicalRecord,
    CONCAT(pat.First_Name,' ',pat.Last_Name) AS FullName,
    pd.Birth_Date AS BirthDate,
    gen.Answer_Text AS Gender,
    esi.Answer_Text AS ESI,
    mc.Answer_Text AS MainCause,
    rb.Bed_Name AS BedName,
    rd.Room_Name AS RoomName,
    su.Name AS UnitName,
    ev.Admission_Date AS AdmissionDate,
    rpp.End_Date
FROM [chameleon].[dbo].[EmergancyVisits] AS ev
LEFT JOIN [chameleon].[dbo].[RoomPlacmentPatient] AS rpp ON ev.Medical_Record = rpp.Medical_Record
LEFT JOIN [chameleon].[dbo].[Patients] AS pat ON ev.patient = pat.patient
LEFT JOIN [chameleon].[dbo].[PersonalDetails] AS pd ON pat.patient = pd.patient
LEFT JOIN [chameleon].[dbo].[V_TableAnswers] AS gen ON gen.Table_Code = 1128 AND gen.Answer_Code = pd.Gender AND gen.Unit IS NULL 
LEFT JOIN [chameleon].[dbo].[AdmissionTreatmentUrgency] AS urg ON ev.Medical_Record = urg.Medical_Record AND urg.Delete_Date IS NULL
LEFT JOIN [chameleon].[dbo].[V_TableAnswers] AS esi ON esi.Table_Code = 1090 AND esi.Answer_Code = urg.Urgent AND esi.Unit = ev.Unit
LEFT JOIN [chameleon].[dbo].[TreatmentCause] AS tc ON ev.Medical_Record = tc.Medical_Record AND tc.Delete_Date IS NULL
LEFT JOIN [chameleon].[dbo].[V_TableAnswers] AS mc ON mc.Table_Code = 1196 AND mc.Answer_Code = tc.Main_Cause AND mc.Unit = ev.Unit
LEFT JOIN [chameleon].[dbo].[RoomDetails] AS rd ON rd.Room_Code = rpp.Room AND rd.Unit = rpp.Unit
LEFT JOIN [chameleon].[dbo].[RoomBeds] AS rb ON rb.Row_ID = rpp.Bed_ID
LEFT JOIN [chameleon].[dbo].[SystemUnits] AS su ON su.Unit = ev.Unit
WHERE 
    ev.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND rpp.Unit = {unit}
	AND ev.Release_Time is null
"""
query_measurements = """
SELECT
    CONCAT(m.Parameter, '#', m.Monitor_Date) AS MeasureID,
    ev.Medical_Record AS MedicalRecord,
    m.Result,
    mp.Min_Value AS MinValue,
    mp.Max_Value AS MaxValue,
    m.Monitor_Date AS At,
    m.Parameter AS Code
FROM (
    SELECT 
        m.Medical_Record,
        m.Parameter,
        m.Monitor_Date,
        m.Result, 
        m.Parameter_Value,
        e.Parameter as EParameter
    FROM [chameleon].[dbo].[Monitor] AS m
    LEFT JOIN [chameleon].[dbo].[Execution] AS e
     ON m.Execution_Row_ID = e.Row_ID AND e.Delete_Date IS NULL
    UNION ALL 
    SELECT 
        m.Medical_Record,
        m.Parameter,
        m.Monitor_Date,
        COALESCE(dpt.Parameter_Translation, m.Result) AS Result, 
        NULL,
        NULL
    FROM [Devices].[dbo].[DeviceMonitor] AS m
    LEFT JOIN [chameleon].[dbo].[MedicalRecords] AS mr
     ON m.Medical_Record = mr.Medical_Record AND mr.Delete_Date IS NULL
    LEFT JOIN [chameleon].[dbo].[DevicesPerUnit] AS dpu
     ON mr.Unit = dpu.Unit AND m.Machine = dpu.Dongle_Id AND dpu.Delete_Date IS NULL
    LEFT JOIN [chameleon].[dbo].[DeviceParametersTranslate] AS dpt
     ON m.Parameter = dpt.Parameter AND dpu.Device_Code = dpt.Device_Type AND m.Result = dpt.Device_Parameter_Value
) AS m
LEFT JOIN [chameleon].[dbo].[EmergancyVisits] AS ev ON m.Medical_Record = ev.Medical_Record
LEFT JOIN [chameleon].[dbo].[RoomPlacmentPatient] AS rpp ON ev.Medical_Record = rpp.Medical_Record
LEFT JOIN [chameleon].[dbo].[MedicalRecords] AS mr 
    ON ev.Medical_Record = mr.Medical_Record AND mr.Delete_Date IS NULL
LEFT JOIN [chameleon].[dbo].[MonitoringParameters] AS mp ON mp.Row_ID = m.Parameter
WHERE 
    ev.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND rpp.Unit = {unit}
    AND m.Parameter IN {codes}
	AND ev.Release_Time is null
"""

query_images = """
SELECT
    ato.Order_Number AS OrderNumber,
    d.Order_Date AS OrderDate,
    mr.Medical_Record AS MedicalRecord,
    [at].Name as TestName,
    ato.Order_Status as OrderStatus,
    atd.Result,
    atd.Panic
FROM [Chameleon].[dbo].[AuxiliaryTestOrders] AS ato
JOIN [Chameleon].[dbo].[AuxTests] AS [at] ON ato.Test = [at].Code
JOIN [Chameleon].[dbo].[MedicalRecords] AS mr ON ato.Patient = mr.Patient
JOIN [Chameleon].[dbo].[RoomPlacmentPatient] AS rpp ON mr.medical_record = rpp.Medical_record
JOIN [Chameleon].[dbo].[emergancyvisits] as ev ON ev.Medical_Record= rpp.Medical_Record
JOIN (
    SELECT MIN(o.Test_date) AS Order_Date, o.Order_Number
    from [Chameleon].[dbo].[AuxiliaryTestOrders] AS o GROUP BY o.Order_Number
) AS d ON d.Order_Number = ato.Order_Number
LEFT OUTER JOIN  [Chameleon].[dbo].[AuxiliaryTestDates] atd 
    ON ato.Accession_Number = atd.Accession_Number AND atd.Delete_Date IS NULL
WHERE 
    ato.Delete_Date IS NULL
    AND ato.Test_Date >= rpp.Start_Date 
    AND rpp.End_Date IS NULL 
    AND rpp.Unit = {unit}
	AND ev.Release_Time is null
	and ev.Delete_Date is null
	and d.Order_Date <= GETDATE()
"""

query_referrals = """
            SELECT
    rd.[Row_Id] AS ReferralId,
    rd.[Medical_Record] AS MedicalRecord,
    rd.[Entry_Date] AS ReferralDate,
    u.Medical_License AS MedicalLicense,
    u.Title,
    u.First_Name AS FirstName,
    u.Last_Name AS LastName
FROM [Chameleon].[dbo].[ResponsibleDoctor] AS rd
JOIN [Chameleon].[dbo].[Users] AS u ON rd.Doctor = u.Code
JOIN [Chameleon].[dbo].[EmergancyVisits] AS mr ON rd.Medical_Record = mr.Medical_Record
JOIN [Chameleon].[dbo].[RoomPlacmentPatient] AS rpp ON mr.Medical_Record = rpp.Medical_Record
WHERE
    rd.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND mr.Unit = {unit}
            AND mr.Release_Time is null
            AND rd.[Entry_Date] >= mr.Admission_Date
            AND mr.Delete_Date is null
"""

query_labs = """
select 
ev.Medical_Record AS MedicalRecord,
labr.test_code AS TestCode,
lhs.Name AS Category, 
labr.Test_Name AS TestName,
concat(labr.Result,' ',labr.Units)  AS Result,
labr.Norm_Minimum AS NormMinimum,
labr.Norm_Maximum AS NormMaximum,
labr.Result_Date AS OrderDate,
labr.Result_Entry_Date AS ResultTime,
rnc.panic AS Panic
from Results.dbo.LabResults AS labr
INNER JOIN chameleon.dbo.LabHeadlinesSort AS lhs ON lhs.Code = labr.Heading
INNER JOIN chameleon.dbo.emergancyvisits AS ev ON ev.patient = labr.Patient 
LEFT OUTER JOIN  Results.dbo.ResultNotConfirm rnc on rnc.Patient = ev.patient and rnc.entry_date >= ev.admission_date and labr.row_id = rnc.Source_Row_ID
WHERE ev.Delete_Date  IS NULL
AND ev.Release_Time  IS NULL
AND labr.Delete_Date IS NULL
and ev.unit = {unit}
and ev.admission_date > GETDATE()-7
and labr.Result_Entry_Date >= ev.admission_date"""

query_doctor_intake = """
SELECT
    d.[Medical_Record] AS MedicalRecord,
    d.[Description_Text] AS MedicalText,
    d.[Entry_Date] AS DocumentingTime
FROM [Chameleon].[dbo].[Descriptions] AS d
JOIN [Chameleon].[dbo].[EmergancyVisits] AS mr ON d.Medical_Record = mr.Medical_Record
JOIN [Chameleon].[dbo].[RoomPlacmentPatient] AS rpp ON mr.Medical_Record = rpp.Medical_Record
WHERE
    d.Delete_Date IS NULL
    AND d.Field = 1
    AND rpp.End_Date IS NULL
    AND mr.Unit = {unit}
       AND mr.Delete_Date is null
       AND mr.Release_Time is null
       AND d.[Entry_Date] >= mr.Admission_Date
"""

query_nurse_intake = """
       SELECT
    tc.[Medical_Record] AS MedicalRecord,
    tc.Remarks AS MedicalText,
    tc.[Entry_Date] AS DocumentingTime
FROM [Chameleon].[dbo].[TreatmentCause] AS tc
JOIN [Chameleon].[dbo].[EmergancyVisits] AS mr ON tc.Medical_Record = mr.Medical_Record
JOIN [Chameleon].[dbo].[RoomPlacmentPatient] AS rpp ON mr.Medical_Record = rpp.Medical_Record
WHERE
    tc.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND mr.Unit = {unit}
       AND mr.Delete_Date is null
       AND mr.Release_Time is null
       AND tc.[Entry_Date] >= mr.Admission_Date"""
