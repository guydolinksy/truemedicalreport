execute_set_patient_admission = """exec [dwh].[dw].[faker_RoomPlacementPatient_admission] {}, {}"""

execute_set_hospitalize_or_discharge = """exec dwh.dw.faker_decision {}"""

execute_set_responsible_doctor = """exec dwh.dw.faker_ResponsibleDoctor {} """

delete_room_placement = """EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.RoomPlacmentPatient' """

delete_admission_treatment_decision = """EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.AdmissionTreatmentDecision' """

delete_responsible_doctor = """EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.ResponsibleDoctor' """

insert_admit_patient = """insert into DemoDB.dbo.patient_info_plus
(ev_MedicalRecord,Gender,First_Name,Last_Name,Birth_Date,UnitName,Wing,Admission_Date,MainCause,ESI)
values({ev_MedicalRecord},'{Gender}','{First_Name}','{Last_Name}','{Birth_Date}','{UnitName}','{Wing}'
,'{Admission_Date}','{MainCause}','{ESI}') """

select_patients_list = """ SELECT distinct p.ev_MedicalRecord FROM DemoDB.dbo.patient_info_plus p
WHERE UnitName='{UnitName}'
AND Wing='{unit_wing}'
AND p.End_Date IS NULL
AND p.Delete_Date IS NULL"""

update_discharge_patient = """ Update DemoDB.dbo.patient_info_plus 
set End_Date= getdate() 
WHERE ev_MedicalRecord={ev_MedicalRecord} and End_Date is null """