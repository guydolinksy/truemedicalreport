query_treatment = """
SELECT
    ev.Medical_Record AS MedicalRecord,
    de.Answer_Text AS Decision,
    su.Name AS UnitName
FROM [sbwnd81c].[chameleon].dbo.EmergancyVisits AS ev
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomPlacmentPatient AS rpp 
    ON ev.Medical_Record = rpp.Medical_Record
LEFT JOIN [sbwnd81c].[chameleon].dbo.AdmissionTreatmentDecision AS atd 
    ON ev.Medical_Record = atd.Medical_Record and atd.delete_date is null
LEFT JOIN [sbwnd81c].[chameleon].dbo.V_TableAnswers AS de 
    ON de.Table_Code = 1092 AND de.Answer_Code = atd.Decision AND rpp.Unit = de.Unit
LEFT JOIN [sbwnd81c].[chameleon].dbo.SystemUnits AS su 
    ON atd.Hosp_Unit = su.Unit
WHERE 
    ev.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND rpp.Unit = {unit}
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
FROM [sbwnd81c].[chameleon].dbo.EmergancyVisits AS ev
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomPlacmentPatient AS rpp ON ev.Medical_Record = rpp.Medical_Record
LEFT JOIN [sbwnd81c].[chameleon].dbo.Patients AS pat ON ev.patient = pat.patient
LEFT JOIN [sbwnd81c].[chameleon].dbo.PersonalDetails AS pd ON pat.patient = pd.patient
LEFT JOIN [sbwnd81c].[chameleon].dbo.V_TableAnswers AS gen ON gen.Table_Code = 1128 AND gen.Answer_Code = pd.Gender AND gen.Unit IS NULL 
LEFT JOIN [sbwnd81c].[chameleon].dbo.AdmissionTreatmentUrgency AS urg ON ev.Medical_Record = urg.Medical_Record AND urg.Delete_Date IS NULL
LEFT JOIN [sbwnd81c].[chameleon].dbo.V_TableAnswers AS esi ON esi.Table_Code = 1090 AND esi.Answer_Code = urg.Urgent AND esi.Unit = ev.Unit
LEFT JOIN [sbwnd81c].[chameleon].dbo.TreatmentCause AS tc ON ev.Medical_Record = tc.Medical_Record AND tc.Delete_Date IS NULL
LEFT JOIN [sbwnd81c].[chameleon].dbo.V_TableAnswers AS mc ON mc.Table_Code = 1196 AND mc.Answer_Code = tc.Main_Cause AND mc.Unit = ev.Unit
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomDetails AS rd ON rd.Room_Code = rpp.Room AND rd.Unit = rpp.Unit
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomBeds AS rb ON rb.Row_ID = rpp.Bed_ID
LEFT JOIN [sbwnd81c].[chameleon].dbo.SystemUnits AS su ON su.Unit = ev.Unit
WHERE 
    ev.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND rpp.Unit = {unit}
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
    FROM [sbwnd81c].[chameleon].dbo.Monitor AS m
    LEFT JOIN [sbwnd81c].[chameleon].dbo.Execution AS e
     ON m.Execution_Row_ID = e.Row_ID AND e.Delete_Date IS NULL
    UNION ALL 
    SELECT 
        m.Medical_Record,
        m.Parameter,
        m.Monitor_Date,
        COALESCE(dpt.Parameter_Translation, m.Result) AS Result, 
        NULL,
        NULL
    FROM [sbwnd81c].[Devices].dbo.DeviceMonitor AS m
    LEFT JOIN [sbwnd81c].[chameleon].dbo.MedicalRecords AS mr
     ON m.Medical_Record = mr.Medical_Record AND mr.Delete_Date IS NULL
    LEFT JOIN [sbwnd81c].[chameleon].dbo.DevicesPerUnit AS dpu
     ON mr.Unit = dpu.Unit AND m.Machine = dpu.Dongle_Id AND dpu.Delete_Date IS NULL
    LEFT JOIN [sbwnd81c].[chameleon].dbo.DeviceParametersTranslate AS dpt
     ON m.Parameter = dpt.Parameter AND dpu.Device_Code = dpt.Device_Type AND m.Result = dpt.Device_Parameter_Value
) AS m
LEFT JOIN [sbwnd81c].[chameleon].dbo.EmergancyVisits AS ev ON m.Medical_Record = ev.Medical_Record
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomPlacmentPatient AS rpp ON ev.Medical_Record = rpp.Medical_Record
LEFT JOIN [sbwnd81c].[chameleon].dbo.MedicalRecords AS mr 
    ON ev.Medical_Record = mr.Medical_Record AND mr.Delete_Date IS NULL
LEFT JOIN [sbwnd81c].[chameleon].dbo.MonitoringParameters AS mp ON mp.Row_ID = m.Parameter
WHERE 
    ev.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND rpp.Unit = {unit}
    AND m.Parameter IN {codes}
"""

query_images = """
SELECT
    ato.Order_Number AS OrderNumber,
    dates.Order_Date AS OrderDate,
    mr.Medical_Record AS MedicalRecord,
    [at].Name as TestName,
    ato.Order_Status as OrderStatus,
    atd.Result,
    atd.Panic
FROM [Chameleon].[dbo].[AuxiliaryTestOrders] AS ato
JOIN [Chameleon].[dbo].[AuxTests] AS [at] ON ato.Test = [at].Code
JOIN [Chameleon].[dbo].[MedicalRecords] AS mr ON ato.Patient = mr.Patient
JOIN [Chameleon].[dbo].[RoomPlacmentPatient] AS rpp ON mr.medical_record = rpp.Medical_record
JOIN (
    SELECT MIN(Test_date) AS Order_Date, Order_Number
    from Chameleon.dbo.AuxiliaryTestOrders GROUP BY Order_Number
    ) AS dates ON dates.Order_Number = ato.Order_Number
LEFT OUTER JOIN  [Chameleon].[dbo].[AuxiliaryTestDates] atd 
    ON ato.Accession_Number = atd.Accession_Number AND atd.Delete_Date IS NULL
WHERE 
    ato.Delete_Date IS NULL
    AND ato.Test_Date > rpp.Start_Date 
    AND rpp.End_Date IS NULL 
    AND rpp.Unit = {unit} 
"""

query_refferals = """
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
JOIN [Chameleon].[dbo].[MedicalRecords] AS mr ON rd.Medical_Record = mr.Medical_Record
JOIN [Chameleon].[dbo].[patients] AS pat ON pat.Patient = mr.Patient
JOIN [Chameleon].[dbo].[RoomPlacmentPatient] AS rpp ON mr.Medical_Record = rpp.Medical_Record
WHERE
    rd.Delete_Date IS NULL
    AND rpp.End_Date IS NULL
    AND mr.Unit = {unit}
"""
