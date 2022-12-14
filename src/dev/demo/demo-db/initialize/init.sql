USE [master]
GO
/****** Object:  Database [DemoDB]    Script Date: 14/12/2022 18:18:00 ******/
CREATE DATABASE [DemoDB]
 CONTAINMENT = NONE
 ON  PRIMARY
( NAME = N'DemoDB', FILENAME = N'/var/opt/mssql/data/DemoDB.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON
( NAME = N'DemoDB_log', FILENAME = N'/var/opt/mssql/data/DemoDB_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 COLLATE Hebrew_CI_AS
GO
ALTER DATABASE [DemoDB] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [DemoDB].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [DemoDB] SET ANSI_NULL_DEFAULT OFF
GO
ALTER DATABASE [DemoDB] SET ANSI_NULLS OFF
GO
ALTER DATABASE [DemoDB] SET ANSI_PADDING OFF
GO
ALTER DATABASE [DemoDB] SET ANSI_WARNINGS OFF
GO
ALTER DATABASE [DemoDB] SET ARITHABORT OFF
GO
ALTER DATABASE [DemoDB] SET AUTO_CLOSE OFF
GO
ALTER DATABASE [DemoDB] SET AUTO_SHRINK OFF
GO
ALTER DATABASE [DemoDB] SET AUTO_UPDATE_STATISTICS ON
GO
ALTER DATABASE [DemoDB] SET CURSOR_CLOSE_ON_COMMIT OFF
GO
ALTER DATABASE [DemoDB] SET CURSOR_DEFAULT  GLOBAL
GO
ALTER DATABASE [DemoDB] SET CONCAT_NULL_YIELDS_NULL OFF
GO
ALTER DATABASE [DemoDB] SET NUMERIC_ROUNDABORT OFF
GO
ALTER DATABASE [DemoDB] SET QUOTED_IDENTIFIER OFF
GO
ALTER DATABASE [DemoDB] SET RECURSIVE_TRIGGERS OFF
GO
ALTER DATABASE [DemoDB] SET  DISABLE_BROKER
GO
ALTER DATABASE [DemoDB] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO
ALTER DATABASE [DemoDB] SET DATE_CORRELATION_OPTIMIZATION OFF
GO
ALTER DATABASE [DemoDB] SET TRUSTWORTHY OFF
GO
ALTER DATABASE [DemoDB] SET ALLOW_SNAPSHOT_ISOLATION OFF
GO
ALTER DATABASE [DemoDB] SET PARAMETERIZATION SIMPLE
GO
ALTER DATABASE [DemoDB] SET READ_COMMITTED_SNAPSHOT OFF
GO
ALTER DATABASE [DemoDB] SET HONOR_BROKER_PRIORITY OFF
GO
ALTER DATABASE [DemoDB] SET RECOVERY FULL
GO
ALTER DATABASE [DemoDB] SET  MULTI_USER
GO
ALTER DATABASE [DemoDB] SET PAGE_VERIFY CHECKSUM
GO
ALTER DATABASE [DemoDB] SET DB_CHAINING OFF
GO
ALTER DATABASE [DemoDB] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF )
GO
ALTER DATABASE [DemoDB] SET TARGET_RECOVERY_TIME = 60 SECONDS
GO
ALTER DATABASE [DemoDB] SET DELAYED_DURABILITY = DISABLED
GO
ALTER DATABASE [DemoDB] SET ACCELERATED_DATABASE_RECOVERY = OFF
GO
EXEC sys.sp_db_vardecimal_storage_format N'DemoDB', N'ON'
GO
ALTER DATABASE [DemoDB] SET QUERY_STORE = OFF
GO
USE [DemoDB]
GO
/****** Object:  User [arc_cham_login]    Script Date: 14/12/2022 18:18:00 ******/
CREATE USER [arc_cham_login] FOR LOGIN [arc_cham_login] WITH DEFAULT_SCHEMA=[dbo]
GO
ALTER ROLE [db_owner] ADD MEMBER [arc_cham_login]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [arc_cham_login]
GO
/****** Object:  Table [dbo].[faker_answer_HospUnit]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[faker_answer_HospUnit](
	[decision] [int] NULL,
	[name] [int] NULL,
	[unit_name] [varchar](100) NULL,
	[treatment_decision] [varchar](100) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[faker_beds]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[faker_beds](
	[room] [nvarchar](150) NOT NULL,
	[bed_name] [nvarchar](150) NOT NULL,
	[row_id] [int] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[faker_nurse_remarks]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[faker_nurse_remarks](
	[MainCause] [nvarchar](200) NULL,
	[gender] [nvarchar](2) NULL,
	[remarks] [varchar](500) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[faker_wing_Doctor]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[faker_wing_Doctor](
	[DepartmentWing] [nvarchar](150) NULL,
	[Code] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[images]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[images](
	[ev_MedicalRecord] [bigint] NULL,
	[TestOrders_Order_Num] [nvarchar](100) NULL,
	[TestOrders_Order_Status] [smallint] NULL,
	[TestDates_Result] [nvarchar](1) NULL,
	[TestDates_Panic] [bit] NULL,
	[AuxTest_Name] [nvarchar](200) NULL,
	[TestOrders_Test_Date] [datetime] NULL,
	[TestOrders_Delete_Date] [datetime] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Labs]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Labs](
	[ev_MedicalRecord] [bigint] NULL,
	[Lab_Headline_Name] [nvarchar](100) NULL,
	[LR_Test_code] [int] NULL,
	[LR_Test_Name] [varchar](150) NULL,
	[LR_Result] [varchar](150) NULL,
	[LR_Units] [varchar](150) NULL,
	[LR_Norm_Minimum] [varchar](150) NULL,
	[LR_Norm_Maximum] [varchar](150) NULL,
	[LR_Result_Date] [datetime] NULL,
	[LR_Result_Entry_Date] [datetime] NULL,
	[LR_Delete_Date] [datetime] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[measurements]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[measurements](
	[ev_MedicalRecord] [bigint] NULL,
	[Device_monitor_Parameter] [smallint] NULL,
	[Device_monitor_date] [datetime] NULL,
	[Device_monitor_result] [nvarchar](200) NULL,
	[Monitoring_Max_Value] [float] NULL,
	[Monitoring_Min_Value] [float] NULL,
	[Faker_Name] [nvarchar](200) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[patient_info_plus]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[patient_info_plus](
	[ev_MedicalRecord] [bigint] NULL,
	[ev_Unit] [int] NULL,
	[Delete_Date] [datetime] NULL,
	[Admission_Date] [datetime] NULL,
	[Birth_Date] [datetime] NULL,
	[End_Date] [datetime] NULL,
	[Gender] [nvarchar](100) NULL,
	[ESI] [nvarchar](100) NULL,
	[MainCause] [nvarchar](100) NULL,
	[BedName] [nvarchar](200) NULL,
	[RoomName] [nvarchar](100) NULL,
	[UnitName] [nvarchar](100) NULL,
	[Doctor_intake_MedicalText] [nvarchar](100) NULL,
	[Doctor_intake_Time] [datetime] NULL,
	[Nurse_Remarks_Text] [nvarchar](4000) NULL,
	[Nurse_Remarks_Entry_Date] [datetime] NULL,
	[ReferralID] [bigint] NULL,
	[ReferralDate] [datetime] NULL,
	[Referral_MedicalLicense] [int] NULL,
	[Referral_Title] [nvarchar](100) NULL,
	[Referral_FirstName] [nvarchar](100) NULL,
	[Referral_LastName] [nvarchar](100) NULL,
	[Treatmant_Decision] [varchar](100) NULL,
	[Treatment_UnitName] [varchar](100) NULL,
	[First_Name] [varchar](100) NULL,
	[Last_Name] [varchar](100) NULL,
	[Wing] [nvarchar](100) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[RoomBeds]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[RoomBeds](
	[Row_ID] [int] NULL,
	[Bed_Name] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[RoomDetails]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[RoomDetails](
	[Room_Code] [int] NULL,
	[Unit] [int] NULL,
	[Beds] [int] NULL,
	[Room_Name] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SystemUnits]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SystemUnits](
	[Unit] [int] NULL,
	[Name] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TableAnswers]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TableAnswers](
	[Answer_Code] [int] NULL,
	[Answer_Text] [nvarchar](150) NULL,
	[Table_Code] [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TreatmentCause]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TreatmentCause](
	[remarks] [nvarchar](2000) NULL,
	[Medical_Record] [bigint] NULL,
	[Entry_Date] [datetime] NULL,
	[delete_date] [datetime] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
	[usernamenotitle] [nvarchar](150) NULL,
	[Code] [nvarchar](150) NULL,
	[Title] [nvarchar](100) NULL,
	[First_Name] [nvarchar](100) NULL,
	[Last_Name] [nvarchar](100) NULL,
	[Medical_License] [int] NULL,
	[row_ID] [bigint] NULL
) ON [PRIMARY]
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 819000, N'פנימית גריאטריה ג', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 834000, N'כירורגית חזה-כלי דם', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 836000, N'כירורגית ב', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 837000, N'כירורגית ג', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 853000, N'כירורגית ילדים', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 859000, N'כירורגית כויות', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 860000, N'כירורגית לב', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 870000, N'כירורגית פה ולסת', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 871000, N'פנימית א', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 872000, N'פנימית ב', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 873000, N'פנימית ג', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 874000, N'פנימית ד', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 875000, N'פנימית ה', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 876000, N'פנימית ו', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 972000, N'אשפוז יום שיקום ילדים', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 1505100, N'אשפוז יום שיקומי - לצפייה', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 1539200, N'אשפוז יום פסיכיאטרי', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 1549983, N'פנימית בלינסון', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15054500, N'כירורגית לב ילדים', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15059312, N'אשפוז יום גניקולוגי', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15063421, N'פנימית', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15064114, N'אשפוז יום נפגעי ראש - לצפייה', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15065323, N'פנימית ט', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15066727, N'אשפוז יום נוירואונקולוגי', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068347, N'אשפוז יום הפרעות אכילה', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068369, N'פנימית גריאטריה ד', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068397, N'אשפוז יום נשימתי - לצפייה', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068422, N'כירורגית חזה', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068423, N'כירורגית כלי דם', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068448, N'וירטואלי פנימית א', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068510, N'אשפוז', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068531, N'אשפוז כירורגי קצר', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068593, N'פנימית קורונה ג', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068594, N'פנימית קורונה ד', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068596, N'פנימית קורונה ב', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068598, N'פנימית קורונה ה', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (1, 15068666, N'פנימית קורונה ח', N'אשפוז')
GO
INSERT [dbo].[faker_answer_HospUnit] ([decision], [name], [unit_name], [treatment_decision]) VALUES (2, NULL, NULL, N'שחרור')
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'1', 1)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'2', 2)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'3', 3)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'4', 4)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'5', 5)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'6', 6)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'7', 7)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'8', 8)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'9', 9)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'10', 10)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'11', 11)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B1', N'12', 12)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'1', 13)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'2', 14)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'3', 15)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'4', 16)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'5', 17)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'6', 18)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'7', 19)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'8', 20)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'9', 21)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'10', 22)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'11', 23)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B2', N'12', 24)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'1', 25)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'2', 26)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'3', 27)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'4', 28)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'5', 29)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'6', 30)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'7', 31)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'8', 32)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'9', 33)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'10', 34)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'11', 35)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'12', 36)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'13', 37)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'14', 38)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'15', 39)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף B3', N'16', 40)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף הולכים', N'1', 41)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף הולכים', N'2', 42)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף הולכים', N'3', 43)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף הולכים', N'4', 44)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'אגף הולכים', N'5', 45)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'חדר הלם', N'1', 46)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'חדר הלם', N'2', 47)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'חדר הלם', N'3', 48)
GO
INSERT [dbo].[faker_beds] ([room], [bed_name], [row_id]) VALUES (N'חדר הלם', N'4', 49)
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב חזה', N'M', N'ידוע על מחלה גרורתית של הערמונית.HCC,יתר לד .מהבוקר לחץ בחזה במנוחה מלווה בקושי בנשימה, ללא צרבצ, ללא הקרנה.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב חזה', N'M', N'בשע 12 כאבים בחזה ללא תלונות נוספות במשך 15 שעה אשר חלפו. מדווח על הרגשה טובה')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב חזה', N'F', N' לדבריה היום בשעה 16:15 הופיעו לחצים בחזה עם הקרנה לשני הידיים מלווה בזיעה. שוללת קושי בנשימה. מציינת כי השבוע לא לקחה אספירין.  קיבלה אספירין 300 מג בלעיסה ואיזוקט 1.25 ופרמין 10 מג')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב חזה', N'M', N'פנה עקב כאבים בחזה שחלפו.  הקרנה לגב')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב חזה', N'M', N' ברקע IHD VTN הגיע עם תלונה על כאב בחזה לסירוגין מקרין ליד שמאל חולף ספונטנית')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב חזה', N'F', N'חולה אונקולוגית עם חולשה וכאבים בחזה')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חבלה/נפילה', N'F', N'מטופת צלולה הובאה על ידי מדא לאחר נפילה טכנית עם חבלה בכפות הרגליים שוללת חבלות נוספות')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חבלה/נפילה', N'M', N' חולה המופיליה  לדבריו לפני שבוע נפילה ללא חבלת ראש מלווה בחבלה באגן ומאז חולשה כללית וקושי בהליכה ')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חבלה/נפילה', N'M', N'נפל נפילה טכנית   לדבריו נחבל בראש ובמרפק ימין   ללא איבוד הכרה , אינו זוכר אם נוטל תרופות לדילול דם ')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חבלה/נפילה', N'M', N'. לדבריו לפני כשעה וחצי נפילה טכנית במדרכה עם חבלת ראש ללא מדללי דם בקבלתו יציב נשימתית')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חבלה/נפילה', N'F', N'חשד לשבר פרק ירך שמאלית-נמצאת בחדר טיפולים-נבצע הכנה לאשפוז מחוסנת ב-2 חיסונים כנגד-COVID 19')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי בטן', N'F', N'לדב ריה לאחר ניתוח WHIPPLE OPERATION , כעת הגיעה עקב הפרשה מוגלתית מצלקת ניתוחית')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי בטן', N'M', N' הופנה  ממלר"ד אונקולוגי   עקב חולשה  הקאות וחשד  לחסימת  מעי.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי בטן', N'F', N' לדבריה מזה חודש   דימומים  רקטלים   \היום  קרישי  דם  .  כמו  כן  נבדקה על  ידי פרוקטולוג  הורגש  גוש')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי בטן', N'M', N'פנה לחדר מיון בשל עליה בתפקודי כבד , כאבים בטן אפיגסטריים מקרינים לגב ,')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי בטן', N'M', N'פניה חוזרת למיון עקב כאבי בטן על רקע דלקת במעי, שולל חום')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'קוצר נשימה', N'F', N'ברקע COPD מזה 5 ימים שיעול ליחתי ללא חום, סיימה טיפול ב-LEVOOFLOXACIN, כעת החמרה עם הקוצ"נ.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'קוצר נשימה', N'F', N'פנתה עקב קוצר נשימה מזה חודש. שוללת כאבים בחזה. ברקע ידוע על HTN, DM, היפרליפידמיה.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'קוצר נשימה', N'M', N'ברקע IHD COPD סכרת הובא לחדר מיון בשל קוצר נשימה חריף')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'קוצר נשימה', N'F', N' הובאה למיון ע"י נט"ן בשל קוצר נשימה חריף, הזעה וערכי ל"ד גבוהים. הוכנסה לחדר הלם לצורך הערכה וטיפול.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'קוצר נשימה', N'M', N' ברקע- אי ספיקת לב, לפי דברי בתו, בשבוע האחרון קושי בנשימה, ללא כאב בחזה, ללא שיעול')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חולשה', N'F', N'מזה חודש חולשה כללית, מלווה בתחושת קוצר נשימה קל במאמצים. ללא כאבים בחזה, לא חום')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חולשה', N'F', N'ברקע סכרת פנתה למיון עקב חולשה כללית וסוכר גבוהה בדם')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חולשה', N'M', N'מטופל עם מחלת CA OF COLON META הגיע כעת עקב חולשה ניכרת וקושי במילוי ADL ,ללא סיפור חבלתי  .')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חולשה', N'M', N'מטופל עם פניאומוניה מהקהילה , טופל ברוליד , היום אירוע של PRE SYNCOPE וחולשה כללית ללא סיפור חבלתי  .')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חולשה', N'F', N'לדבריה חולשה כללית מאתמול בבוקר, מלינה על כאבי ראש ולחץ דם גבוה סביב 200 סיסטולי בבית.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חום', N'M', N', ברקע - GASTRIC CA , היפותירואידיזם')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חום', N'F', N', ברקע: PTC  פנתה למיון עקב חום, מלווה בבחילות, ללא הקאות. מלווה בשיעול.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חום', N'M', N'רקע אונקולוגי. מזה כיומיים חום עד 39. מלווה בכאבי בטן והקאות.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חום', N'F', N'לדבריה הגיעה עקב מחלת חום  .   ברקע: CA OF LUNG .')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'חום', N'F', N'ברקע אם נקז של דרכי מרע מלפני שבוע -החלפה -כעת הגיעה עקב חום עד 37.7')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב גב', N'M', N'פנה בשל החמרה של כאבי גב ')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב גב', N'M', N'כאבי גב עזים קושי בהליכה לאחר אנלגטיקה  בוצע סיטי פריצות דיסק  הסיטי הוטמע ')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב גב', N'F', N'כאבי גב  כמה ימים. לפני שבועיים אישפוז באורטופדיה   עברה ניתוח ירכיים עקב שבר פטולוגי. ברקע HTN')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב גב', N'F', N'חולה עם  מחלה גרורתית  מפושתת מקור לבלב לדבריה כאבים בגב תחתון מקרינים לרגל שמאל')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאב גב', N'M', N'בעברו אונקולוגי. הועבר מברזילי לבקשתו שם אושפז בשל כאבי גב תחתון עם ממצא של פריצת דיסק')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'סחרחורת', N'F', N'פנתה למיון עקב סחרחורת, שמלווה בבחילות , שוללת כאבים בחזה')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'סחרחורת', N'M', N'הובא על ידי מד"א עקב בחילות וסחרחורות. ברקע ידוע על DM.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'סחרחורת', N'F', N'סחרחורות סיבוביות   בנסיון לקום מהמיטה הקאה אחת ללא מחלות')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'סחרחורת', N'M', N'ברקע חולה אונקולוגי ב 23.8 עבר ניתוח עקב הוצאת גידול מלבלב כעת הגיעה עקב סחרחורות הקאות -ללא חום')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'סחרחורת', N'F', N'ברקע:Digestive System Malignancy: Colon  לדבריה מזה מס" ימים כאבים ביד ימים , סחרחורת  שוללת כאבים בחזה.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי ראש', N'F', N'מזה 3 חודשים סובלת מכאבי ראש אתמול עשתה MRI  כעת הגיעה לצורך המשך בירור')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי ראש', N'F', N'פנתה למיון עקב יתר לחץ דם שמלווה בכאבי ראש ובחילות')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי ראש', N'F', N'לדבריה מזה הרבה זמן, היום לחץ באזור העורף וכן נימול בפנים, לחץ בלסתות. ברקע גידול בראש עם הגרורות. אמורה לקבל טיפול כמוטרפי')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי ראש', N'M', N'נפילה מתוך שינה וחבלת ראש . מאז כאבי ראש וסחרחורות .')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'כאבי ראש', N'M', N'לדבריו מזה שבועיים. לדבריו לראשונה מזה שבועיים, בעמידה ומאמץ אפילו קל מופעיים סחרחורות')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'שבר', N'M', N'לדברי בנו מטופל מעד ונפל נחבל ביד שמאל, נבדק במוקד ובוצע צילום וכן הודגם שבר בשורש כף יד שמאל, ברקע דמנציה')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'שבר', N'M', N' ברקע: הפטיטיס C.  כעת הופנה לאחר נפילה ביום חמישי האחרון עם חבלה במרפק.  בצילום שביצע בקהילה שבר באולנה פרוקסימאלית עם חשד לשבר בראש רדיוס.  בנוסף נפיחות בכף היד.')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'שבר', N'F', N'חבלת כתף  . החליקה נפלה נחבלה בכתף  .  ברקע HTN ')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'שבר', N'F', N'הבוקר גובסה במיון. כעת פנתה בשל כאב באזור הגבס ')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'שבר', N'F', N'חבלת קרסול שמאול  נפיחות כאבים חזקים באזור וחבלת גב . לפני כשעה נפלה. ברקע אוסטאופורוזיס')
GO
INSERT [dbo].[faker_nurse_remarks] ([MainCause], [gender], [remarks]) VALUES (N'שבר', N'M', N'נפל בלילה  לאחר סחרחורת  מדווח על חבלת אגן  רגל ימין . ברקע  שרטן מעיים  גרורתי')
GO
INSERT [dbo].[faker_wing_Doctor] ([DepartmentWing], [Code]) VALUES (N'אגף הולכים', N'1')
GO
INSERT [dbo].[faker_wing_Doctor] ([DepartmentWing], [Code]) VALUES (N'אגף הולכים', N'5')
GO
INSERT [dbo].[faker_wing_Doctor] ([DepartmentWing], [Code]) VALUES (N'אגף B1', N'2')
GO
INSERT [dbo].[faker_wing_Doctor] ([DepartmentWing], [Code]) VALUES (N'אגף B1', N'3')
GO
INSERT [dbo].[faker_wing_Doctor] ([DepartmentWing], [Code]) VALUES (N'אגף B2', N'4')
GO
INSERT [dbo].[faker_wing_Doctor] ([DepartmentWing], [Code]) VALUES (N'אגף B2', N'6')
GO
INSERT [dbo].[faker_wing_Doctor] ([DepartmentWing], [Code]) VALUES (N'אגף B3', N'7')
GO
INSERT [dbo].[faker_wing_Doctor] ([DepartmentWing], [Code]) VALUES (N'אגף B3', N'8')
GO
INSERT [dbo].[images] ([ev_MedicalRecord], [TestOrders_Order_Num], [TestOrders_Order_Status], [TestDates_Result], [TestDates_Panic], [AuxTest_Name], [TestOrders_Test_Date], [TestOrders_Delete_Date]) VALUES (NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL)
GO
INSERT [dbo].[measurements] ([ev_MedicalRecord], [Device_monitor_Parameter], [Device_monitor_date], [Device_monitor_result], [Monitoring_Max_Value], [Monitoring_Min_Value], [Faker_Name]) VALUES (345678, NULL, CAST(N'2022-01-01T00:00:00.000' AS DateTime), NULL, NULL, 654.4, NULL)
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (1, N'1')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (2, N'2')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (3, N'3')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (4, N'4')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (5, N'5')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (6, N'6')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (7, N'7')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (8, N'8')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (9, N'9')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (10, N'10')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (11, N'11')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (12, N'12')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (13, N'13')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (14, N'14')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (15, N'15')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (16, N'16')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (17, N'17')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (18, N'18')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (19, N'19')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (20, N'20')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (21, N'21')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (22, N'22')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (23, N'23')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (24, N'24')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (25, N'25')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (26, N'26')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (27, N'27')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (28, N'28')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (29, N'29')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (30, N'30')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (31, N'31')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (32, N'32')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (33, N'33')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (34, N'34')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (35, N'35')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (36, N'36')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (37, N'37')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (38, N'38')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (39, N'39')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (40, N'40')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (41, N'1')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (42, N'2')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (43, N'3')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (44, N'4')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (45, N'5')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (46, N'1')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (47, N'2')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (48, N'3')
GO
INSERT [dbo].[RoomBeds] ([Row_ID], [Bed_Name]) VALUES (49, N'4')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (1, 1184000, 12, N'אגף B2')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (2, 1184000, 16, N'אגף B3')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (3, 1184000, 5, N'אגף הולכים')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (4, 1184000, 4, N'חדר הלם')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (5, 1184000, 12, N'אגף B1')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (6, 1184000, 15, N'אגף פסיכיאטרי')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (7, 1184000, 37, N'בידוד אדום')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (8, 1184000, 99, N'אגף אנטיגן')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (9, 1184000, 99, N'אגף שוכבים ירוק')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (819000, N'פנימית גריאטריה ג')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (834000, N'כירורגית חזה-כלי דם')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (836000, N'כירורגית ב')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (837000, N'כירורגית ג')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (853000, N'כירורגית ילדים')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (859000, N'כירורגית כויות')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (860000, N'כירורגית לב')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (870000, N'כירורגית פה ולסת')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (871000, N'פנימית א')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (872000, N'פנימית ב')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (873000, N'פנימית ג')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (874000, N'פנימית ד')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (875000, N'פנימית ה')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (876000, N'פנימית ו')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (972000, N'אשפוז יום שיקום ילדים')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1505100, N'אשפוז יום שיקומי - לצפייה')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1539200, N'אשפוז יום פסיכיאטרי')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1549983, N'פנימית בלינסון')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15054500, N'כירורגית לב ילדים')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15059312, N'אשפוז יום גניקולוגי')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15063421, N'פנימית')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15064114, N'אשפוז יום נפגעי ראש - לצפייה')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15065323, N'פנימית ט')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15066727, N'אשפוז יום נוירואונקולוגי')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068347, N'אשפוז יום הפרעות אכילה')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068369, N'פנימית גריאטריה ד')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068397, N'אשפוז יום נשימתי - לצפייה')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068422, N'כירורגית חזה')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068423, N'כירורגית כלי דם')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068448, N'וירטואלי פנימית א')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068510, N'אשפוז')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068531, N'אשפוז כירורגי קצר')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068593, N'פנימית קורונה ג')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068594, N'פנימית קורונה ד')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068596, N'פנימית קורונה ב')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068598, N'פנימית קורונה ה')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068666, N'פנימית קורונה ח')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1184000, N'המחלקה לרפואה דחופה')
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (1, N'אשפוז', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (3, N'אשפוז בית', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (4, N'באולטרסאונד גינקולוגי', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (5, N'בדיקה', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (6, N'בדיקה חוזרת', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (7, N'בירור', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (8, N'במיון הכללי', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (9, N'במיון כללי', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (10, N'הלך על דעת עצמו', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (11, N'המתנה למעבדה', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (12, N'העברה לחדר לידה', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (13, N'העברה לצינתורים', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (14, N'השראת לידה', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (15, N'חדר לידה', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (16, N'חדר ניתוח', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (17, N'חזרה לאשפוז', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (18, N'חזרה למחלקת האשפוז', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (19, N'חזרה למיון', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (20, N'ממתינה לאולטרסאונד', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (21, N'ניטור', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (22, N'נפטר במיון', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (23, N'נפטר/ה', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (24, N'עבר למיון אחר', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (25, N'עזבו על דעת עצמם', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (2, N'שחרור', 1092)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code], [Title], [First_Name], [Last_Name], [Medical_License], [row_ID]) VALUES (N'ניסים אהרון', N'1', N' דר', N'ניסים', N' אהרון', 907997, 54)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code], [Title], [First_Name], [Last_Name], [Medical_License], [row_ID]) VALUES (N'שירה גרינשטיין', N'2', N' דר', N'שירה', N' גרינשטיין', 145250, 64)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code], [Title], [First_Name], [Last_Name], [Medical_License], [row_ID]) VALUES (N'ניצן חלבי', N'3', N' דר', N'ניצן', N' חלבי', 926660, 87)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code], [Title], [First_Name], [Last_Name], [Medical_License], [row_ID]) VALUES (N'עמית גזית', N'4', N' דר', N'עמית', N' גזית', 739361, 89)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code], [Title], [First_Name], [Last_Name], [Medical_License], [row_ID]) VALUES (N'אחמד מלמוד', N'5', N' דר', N'אחמד', N' מלמוד', 686113, 42)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code], [Title], [First_Name], [Last_Name], [Medical_License], [row_ID]) VALUES (N'מוחמד דבור', N'6', N' דר', N'מוחמד', N' דבור', 581779, 71)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code], [Title], [First_Name], [Last_Name], [Medical_License], [row_ID]) VALUES (N'אילנית כהן', N'7', N' דר', N'אילנית', N' כהן', 665425, 17)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code], [Title], [First_Name], [Last_Name], [Medical_License], [row_ID]) VALUES (N'נגב ניצן', N'8', N' דר', N'נגב', N' ניצן', 553520, 45)
GO
/****** Object:  StoredProcedure [dbo].[faker_decision]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   procedure [dbo].[faker_decision](@medical_record nvarchar(50))
	AS
	Begin
	declare @decision as int;
	declare @unit_hosp as int;
	if exists (select * from DemoDB.dbo.patient_info_plus p  where p.ev_MedicalRecord=@medical_record and p.Treatmant_Decision is null and p.Treatment_UnitName is null and p.End_Date is null)
		begin
		if (select top 1  count(*)*100/ sum(count(*)) over() as ratio from DemoDB.dbo.patient_info_plus p
		--left join DemoDB.dbo.[faker_answer_HospUnit] as f on p.= f.name
		group by (case when p.Treatmant_Decision =N'שחרור' then 0 else 1 end )
		order by (case when p.Treatmant_Decision=N'שחרור' then 0 else 1 end ) ) <30
		begin
		-- update release
		update DemoDB.dbo.patient_info_plus set Treatmant_Decision='שחרור', Treatment_UnitName= null where ev_MedicalRecord=@medical_record;
		end
	else
		begin
		-- insert hosp
		select top 1 @decision=hu.treatment_decision ,@unit_hosp=hu.unit_name
		from  DemoDB.dbo.faker_answer_HospUnit hu
		where hu.decision!=N'אשפוז' order by newid();
		update DemoDB.dbo.patient_info_plus set Treatmant_Decision=@decision, Treatment_UnitName= @unit_hosp where ev_MedicalRecord=@medical_record;
		end
		end
	end
GO
/****** Object:  StoredProcedure [dbo].[faker_ResponsibleDoctor]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   procedure [dbo].[faker_ResponsibleDoctor](@medical_record nvarchar(50))
	AS
	Begin
	if exists (select * from DemoDB.dbo.patient_info_plus p where p.ev_MedicalRecord=@medical_record and p.delete_date is null and p.ReferralDate is null and p.End_Date is null)
		begin
		select top 1 u.First_Name,u.Last_Name,u.row_ID,u.Medical_License,u.Title
		into #temp_ref
		from
		(select p.RoomName from  DemoDB.dbo.patient_info_plus p where p.ev_MedicalRecord=@medical_record ) as R
		join DemoDB.dbo.faker_wing_Doctor fwd on fwd.DepartmentWing = R.RoomName
		join  DemoDB.dbo.Users u on u.Code=fwd.Code
		join DemoDB.dbo.patient_info_plus p2 on R.RoomName=p2.RoomName
		group by u.Code, u.First_Name,u.Last_Name,u.row_ID,u.Medical_License,u.Title
		order by count(*) asc;
		update 	 DemoDB.dbo.patient_info_plus set Referral_FirstName = r.First_Name, Referral_LastName=r.Last_Name, ReferralID=r.row_ID
		, Referral_MedicalLicense=r.Medical_License, Referral_Title=r.Title, ReferralDate = GETDATE()
		from #temp_ref r where ev_MedicalRecord= @medical_record and Delete_Date is null;
		end
	end
GO
/****** Object:  StoredProcedure [dbo].[faker_RoomPlacementPatient_admission]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[faker_RoomPlacementPatient_admission](@medical_record int, @should_move int)
AS
Begin
    declare @bed_id as varchar(50);
    declare @department as int;
    declare @wing as varchar(50);
    declare @room_num as varchar(100);
	select @department=p.ev_Unit,@wing=p.RoomName from DemoDB.dbo.patient_info_plus p where p.ev_MedicalRecord=@medical_record;
    if exists(select * from DemoDB.dbo.patient_info_plus p where p.ev_MedicalRecord = @medical_record and p.RoomName is not null and p.Delete_Date is null and p.End_Date is null)
    begin
        if @should_move = 0 and  FLOOR(rand()*4)=0
        begin
				select top 1 @wing=fb.room, @bed_id=fb.bed_name from faker_beds fb
				left outer join dbo.patient_info_plus p2 on p2.RoomName = fb.room and p2.BedName=fb.bed_name
				where fb.room != @wing and
				p2.BedName is null order by newid();
		end
		else
		begin
				select top 1 @wing=fb.room, @bed_id=fb.bed_name from faker_beds fb
				left outer join dbo.patient_info_plus p2 on p2.RoomName = fb.room and p2.BedName=fb.bed_name
				where fb.room = @wing and
				p2.BedName is null order by newid();
		end
        if @bed_id is not null
        begin
			update DemoDB.dbo.patient_info_plus set BedName=@bed_id,wing=@wing, RoomName=@wing where ev_MedicalRecord=@medical_record and Delete_Date is null;
        end
    end
    else
    begin
        select top 1 @wing=fb.room, @bed_id=fb.bed_name from faker_beds fb
		left outer join dbo.patient_info_plus p2 on p2.RoomName = fb.room and p2.BedName=fb.bed_name
		where p2.RoomName = @wing and
		p2.BedName is null order by newid();
        if @bed_id is not null
        begin
            update DemoDB.dbo.patient_info_plus set BedName=@bed_id,Wing=@wing, RoomName=@wing where ev_MedicalRecord=@medical_record and Delete_Date is null;
        end
    end
end


GO
/****** Object:  StoredProcedure [dbo].[proc_faker_nurse_remarks]    Script Date: 14/12/2022 18:18:00 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE   procedure [dbo].[proc_faker_nurse_remarks](@medical_record nvarchar(50))
	AS
	Begin
	declare @remarks as varchar(500);
	declare @gender as varchar(5);
	declare @mainCause as varchar(50);

	if exists (select * from DemoDB.dbo.patient_info_plus p where ev_MedicalRecord=@medical_record and Nurse_Remarks_Text is null and End_Date is null)
		begin
			select @gender=Gender,@mainCause=MainCause from DemoDB.dbo.patient_info_plus where ev_MedicalRecord = @medical_record;

			select top 1 @remarks=nr.remarks from DemoDB.dbo.faker_nurse_remarks nr
			left join DemoDB.dbo.patient_info_plus p on p.Nurse_Remarks_Text= nr.remarks
			where nr.gender=@gender and nr.MainCause=@mainCause
			group by nr.remarks
			order by count(*);
			update DemoDB.dbo.patient_info_plus set Nurse_Remarks_Text = @remarks, Nurse_Remarks_Entry_Date = GETDATE() where ev_MedicalRecord= @medical_record and Delete_Date is null;
		end
	end
GO
USE [master]
GO
ALTER DATABASE [DemoDB] SET  READ_WRITE
GO
