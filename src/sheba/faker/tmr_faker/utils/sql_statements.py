execute_set_patient_admission = """execute dwh.dw.faker_RoomPlacmentPatient_admission {}"""

execute_set_hospitalized_decision = """execute dwh.dw.faker_decision {}"""

execute_set_responsible_doctor = """execute dwh.dw.faker_ResponsibleDoctor {}"""

delete_room_placement = """ EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.RoomPlacementPatient' """

delete_admission_treatment_decision = """EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.AdmissionTreatmentDecision' """

delete_responsible_doctor = """EXEC sbwnd81c.chameleon.sys.sp_executesql N'TRUNCATE TABLE  dbo.ResponsibleDoctor' """
