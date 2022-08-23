query_discharge_or_hospitalized = """select a.medical_record as id,b.Answer_Text,s.Name from sbwnd81c.chameleon.dbo.AdmissionTreatmentDecision a join (select distinct Answer_Code,Answer_Text from sbwnd81c.chameleon.dbo.TableAnswers
where Table_Code=1092)b on a.Decision=b.Answer_Code
left join sbwnd81c.chameleon.dbo.SystemUnits s on a.Hosp_Unit=s.Unit
join dwh.dw.Emergency_visits ev on ev.id=a.medical_record and  ev.DepartmentWingDischarge is null and ev.DepartmentAdmission between getdate()-3 and getdate() and ev.DepartmentCode={}
where a.delete_date is null"""

# uncomment sql lines in production
query_patient_admission = """
SELECT
	ev.id,CONCAT(p.first_name,' ',p.last_name) AS full_name,p.birth_date AS	birthdate,p.gender,
	ev.esi,ev.MainCause,rb.Bed_Name,ev.DepartmentWing,'er' AS Name,
	ev.DepartmentAdmission,ev.DepartmentWingDischarge
FROM [sbwnd81c].[chameleon].dbo.RoomPlacmentPatient AS rpp
--INNER JOIN MedicalRecords AS mr ON mr.Medical_Record = rpp.Medical_Record AND mr.Delete_Date IS NULL
right join dwh.dw.Emergency_visits as ev on rpp.Medical_Record=ev.id 
left JOIN dwh.ris.patients AS p ON p.patient_id = ev.id
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomDetails AS rd ON rd.Room_Code = rpp.Room AND rd.Unit = rpp.Unit
LEFT JOIN [sbwnd81c].[chameleon].dbo.RoomBeds AS rb ON rb.Row_ID = rpp.Bed_ID
LEFT JOIN [sbwnd81c].[chameleon].dbo.SystemUnits AS su ON su.Unit = rpp.Unit
WHERE
p.patient_id NOT LIKE '%99999%' AND 
TRY_CAST(p.patient_id AS bigint) IS NOT NULL
AND rpp.End_Date IS NULL
and ev.DepartmentCode=1184000
and ev.DepartmentWingDischarge is null

"""
