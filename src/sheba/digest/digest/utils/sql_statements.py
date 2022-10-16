query_treatment = """
SELECT
    atd.Medical_Record AS MedicalRecord,
    de.Answer_Text AS Decision,
    su.Name AS UnitName
FROM [sbwnd81c].[chameleon].dbo.EmergancyVisits AS ev
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomPlacementPatient AS rpp ON ev.Medical_Record = rpp.Medical_Record
LEFT JOIN [sbwnd81c].[chameleon].dbo.AdmissionTreatmentDecision AS atd ON atd.delete_date is null
LEFT JOIN [sbwnd81c].[chameleon].dbo.V_TableAnswers AS de ON de.Table_Code = 1092 AND de.Answer_Code = atd.Decision AND atd.Unit = de.Unit
LEFT JOIN [sbwnd81c].[chameleon].dbo.SystemUnits AS su ON atd.Hosp_Unit = su.Unit
WHERE ev.Delete_Date IS NULL
AND rpp.End_Date IS NULL
and rpp.Unit = {unit}
 """

query_patient_admission = """
SELECT
    pat.Id_Num as Id,
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
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomPlacementPatient AS rpp ON ev.Medical_Record = rpp.Medical_Record
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
WHERE ev.Delete_Date IS NULL
AND rpp.End_Date IS NULL
and rpp.Unit = {unit}
"""
