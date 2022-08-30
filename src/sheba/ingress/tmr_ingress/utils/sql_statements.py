query_discharge_or_hospitalized = """select a.medical_record as id,b.Answer_Text,s.Name from sbwnd81c_chameleon.dbo.AdmissionTreatmentDecision a join (select distinct Answer_Code,Answer_Text from sbwnd81c_chameleon.dbo.TableAnswers
where Table_Code=1092)b on a.Decision=b.Answer_Code
left join sbwnd81c_chameleon.dbo.SystemUnits s on a.Hosp_Unit=s.Unit
join chameleon_db.dbo.Emergency_visits ev on ev.id=a.medical_record and  ev.DepartmentWingDischarge is null and ev.DepartmentAdmission between getdate()-3 and getdate() and ev.DepartmentCode={}
where a.delete_date is null"""

query_patient_admission = """

"""

query_nurse_remarks = """select ev.id,tc.remarks,tc.Entry_Date from chameleon_db.dbo.Emergency_visits ev left join sbwnd81c_chameleon.dbo.TreatmentCause tc
on ev.id=tc.Medical_Record and tc.delete_date is null and ev.DepartmentWingDischarge is null
where ev.DepartmentCode= {} """