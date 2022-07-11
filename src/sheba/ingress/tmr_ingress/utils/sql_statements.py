query_discharge_or_hospitalized = """select a.medical_record as id,b.Answer_Text,s.Name from sbwnd81c_chameleon.dbo.[AdmissionTreatmentDecision] a join (select distinct Answer_Code,Answer_Text from sbwnd81c_chameleon.dbo.TableAnswers
where Table_Code=1092)b on a.Decision=b.Answer_Code
left join sbwnd81c_chameleon.dbo.SystemUnits s on a.Hosp_Unit=s.Unit
join chameleon_db.dbo.Emergency_visits ev on ev.id=a.medical_record and  ev.DepartmentWingDischarge is null and ev.DepartmentAdmission between getdate()-3 and getdate() and ev.DepartmentCode={}
where a.delete_date is null"""

execute_set_patient_admission = """execute sbwnd81c_chameleon.dbo.faker_RoomPlacmentPatient_admission {}"""

execute_set_hospitalized_decision = """execute sbwnd81c_chameleon.dbo.faker_decision {}"""

execute_set_responsible_doctor = """execute sbwnd81c_chameleon.dbo.faker_ResponsibleDoctor {}"""
