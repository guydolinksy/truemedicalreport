execute_set_patient_admission = """execute sbwnd81c_chameleon.dbo.faker_RoomPlacmentPatient_admission {}"""

execute_set_hospitalized_decision = """execute sbwnd81c_chameleon.dbo.faker_decision {}"""

execute_set_responsible_doctor = """execute sbwnd81c_chameleon.dbo.faker_ResponsibleDoctor {}"""

execute_set_nurse_remarks = """execute sbwnd81c_chameleon.dbo.proc_faker_nurse_remarks {} """

delete_room_placement = """ truncate table sbwnd81c_chameleon.dbo.RoomPlacementPatient"""

delete_admission_treatment_decision = """truncate table sbwnd81c_chameleon.dbo.AdmissionTreatmentDecision"""

delete_responsible_doctor = """truncate table sbwnd81c_chameleon.dbo.ResponsibleDoctor"""

delete_TreatmentCause = """truncate table sbwnd81c_chameleon.dbo.TreatmentCause"""
