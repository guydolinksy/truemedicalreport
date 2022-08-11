execute_set_patient_admission = """execute sbwnd81c_chameleon.dbo.faker_RoomPlacementPatient_admission {}, {}"""

execute_set_hospitalize_or_discharge = """execute sbwnd81c_chameleon.dbo.faker_decision {}"""

execute_set_responsible_doctor = """execute sbwnd81c_chameleon.dbo.faker_ResponsibleDoctor {}"""

delete_room_placement =""" truncate table sbwnd81c_chameleon.dbo.RoomPlacementPatient"""

delete_admission_treatment = """truncate table sbwnd81c_chameleon.dbo.AdmissionTreatmentDecision"""

delete_responsible_doctor= """truncate table sbwnd81c_chameleon.dbo.ResponsibleDoctor"""
