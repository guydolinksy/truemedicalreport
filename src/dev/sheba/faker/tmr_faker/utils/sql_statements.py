execute_set_patient_admission = """exec [dwh].[dw].[faker_RoomPlacementPatient_admission] {}, {}"""

execute_set_hospitalize_or_discharge = """exec dwh.dw.faker_decision {}"""

execute_set_responsible_doctor = """exec dwh.dw.faker_ResponsibleDoctor {} """

delete_room_placement = """EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.RoomPlacmentPatient' """

delete_admission_treatment_decision = """EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.AdmissionTreatmentDecision' """

delete_responsible_doctor = """EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.ResponsibleDoctor' """