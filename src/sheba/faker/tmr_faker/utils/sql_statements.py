execute_set_patient_admission = """execute dwh.dbo.faker_RoomPlacmentPatient_admission {}"""

execute_set_hospitalized_decision = """execute dwh.dbo.faker_decision {}"""

execute_set_responsible_doctor = """execute dwh.dbo.faker_ResponsibleDoctor {}"""

delete_room_placement =""" truncate table sbwnd81c.chameleon.dbo.RoomPlacementPatient"""

delete_admission_treatment_decision = """truncate table sbwnd81c.chameleon.dbo.AdmissionTreatmentDecision"""

delete_responsible_doctor= """truncate table sbwnd81c.chameleon.dbo.ResponsibleDoctor"""
