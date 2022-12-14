execute_set_patient_admission = """exec [DemoDB].[dbo].[faker_RoomPlacementPatient_admission] {}, {}"""

execute_set_hospitalize_or_discharge = """exec DemoDB.dbo.faker_decision {}"""

execute_set_responsible_doctor = """exec DemoDB.dbo.faker_ResponsibleDoctor {} """

delete_room_placement = """EXEC DemoDB.dbo.sys.sp_executesql N'TRUNCATE TABLE  dbo.RoomPlacmentPatient' """

delete_admission_treatment_decision = """EXEC DemoDB.dbo.sys.sp_executesql N'TRUNCATE TABLE  dbo.AdmissionTreatmentDecision' """

delete_responsible_doctor = """EXEC DemoDB.dbo.sys.sp_executesql N'TRUNCATE TABLE  dbo.ResponsibleDoctor' """

insert_admit_patient = """insert into DemoDB.dbo.patient_info_plus
(ev_MedicalRecord,Gender,First_Name,Last_Name,Birth_Date,UnitName,RoomName,Admission_Date,MainCause,ESI)
values({ev_MedicalRecord},'{Gender}',N'{First_Name}',N'{Last_Name}','{Birth_Date}',N'{UnitName}',N'{Wing}'
,'{Admission_Date}',N'{MainCause}','{ESI}') """

select_patients_list = """ SELECT distinct p.ev_MedicalRecord FROM DemoDB.dbo.patient_info_plus p
WHERE UnitName='{UnitName}'
AND Wing='{unit_wing}'
AND p.End_Date IS NULL
AND p.Delete_Date IS NULL"""

update_discharge_patient = """ Update DemoDB.dbo.patient_info_plus 
set End_Date= getdate() 
WHERE ev_MedicalRecord={ev_MedicalRecord} and End_Date is null """

insert_measurements = """INSERT INTO  DemoDB.dbo.measurements (ev_MedicalRecord,m.Device_monitor_date,
m.Device_monitor_Parameter,m.Faker_Name,m.Monitoring_Min_Value,m.Monitoring_Max_Value,m.Device_monitor_result ) 
values({ev_MedicalRecord},'{Device_monitor_date}',{Device_monitor_Parameter},'{Faker_Name}',{Monitoring_Min_Value},
{Monitoring_Max_Value},'{Device_monitor_result}') """

insert_images = """INSERT INTO DemoDB.dbo.images(ev_MedicalRecord,TestOrders_Test_Date,AuxTest_Name, 
TestOrders_Order_Status,TestDates_Panic,TestOrders_Order_Num,TestOrders_Order_Status) VALUES({ev_MedicalRecord},'{TestOrders_Test_Date}',
N'{AuxTest_Name}', {TestOrders_Order_Status},{TestDates_Panic},'{TestOrders_Order_Num}',{TestOrders_Order_Status}) """

insert_labs = """INSERT INTO DemoDB.dbo.Labs (ev_MedicalRecord,LR_Test_code,Lab_Headline_Name,LR_Test_Name,LR_Result,
LR_Units,LR_Norm_Minimum,LR_Norm_Maximum,LR_Result_Date,LR_Result_Entry_Date) values({ev_MedicalRecord},
{LR_Test_code},N'{Lab_Headline_Name}',N'{LR_Test_Name}',N'{LR_Result}',N'{LR_Units}',N'{LR_Norm_Minimum}',
N'{LR_Norm_Maximum}','{LR_Result_Date}','{LR_Result_Entry_Date}') """

update_doctor_visit = """update DemoDB.dbo.patient_info_plus SET Doctor_intake_MedicalText=N'{
Doctor_intake_MedicalText}' , Doctor_intake_Time ='{Doctor_intake_Time}' where ev_MedicalRecord= {ev_MedicalRecord} 
and ev_Unit={doc_unit} and Delete_Date is null """