USE [master]
GO
/****** Object:  Database [chameleon]    Script Date: 12/06/2022 1:01:52 ******/
create DATABASE [chameleon]
    CONTAINMENT = NONE
    ON PRIMARY
    ( NAME = N'chameleon', FILENAME = N'/var/opt/mssql/data/chameleon.mdf' , SIZE = 8192 KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536 KB )
    LOG ON
    ( NAME = N'chameleon_log', FILENAME = N'/var/opt/mssql/data/chameleon_log.ldf' , SIZE = 8192 KB , MAXSIZE = 2048 GB , FILEGROWTH = 65536 KB )
    COLLATE Hebrew_CI_AS
GO
alter database [chameleon] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
    begin
        EXEC [chameleon].[dbo].[sp_fulltext_database] @action = 'enable'
    end
GO
ALTER DATABASE [chameleon] SET ANSI_NULL_DEFAULT OFF
GO
alter database [chameleon] SET ANSI_NULLS OFF
GO
alter database [chameleon] SET ANSI_PADDING OFF
GO
alter database [chameleon] SET ANSI_WARNINGS OFF
GO
alter database [chameleon] SET ARITHABORT OFF
GO
alter database [chameleon] SET AUTO_CLOSE OFF
GO
alter database [chameleon] SET AUTO_SHRINK OFF
GO
alter database [chameleon] SET AUTO_UPDATE_STATISTICS ON
GO
alter database [chameleon] SET CURSOR_CLOSE_ON_COMMIT OFF
GO
alter database [chameleon] SET CURSOR_DEFAULT GLOBAL
GO
alter database [chameleon] SET CONCAT_NULL_YIELDS_NULL OFF
GO
alter database [chameleon] SET NUMERIC_ROUNDABORT OFF
GO
alter database [chameleon] SET QUOTED_IDENTIFIER OFF
GO
alter database [chameleon] SET RECURSIVE_TRIGGERS OFF
GO
alter database [chameleon] SET DISABLE_BROKER
GO
alter database [chameleon] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO
alter database [chameleon] SET DATE_CORRELATION_OPTIMIZATION OFF
GO
alter database [chameleon] SET TRUSTWORTHY OFF
GO
alter database [chameleon] SET ALLOW_SNAPSHOT_ISOLATION OFF
GO
alter database [chameleon] SET PARAMETERIZATION SIMPLE
GO
alter database [chameleon] SET READ_COMMITTED_SNAPSHOT OFF
GO
alter database [chameleon] SET HONOR_BROKER_PRIORITY OFF
GO
alter database [chameleon] SET RECOVERY FULL
GO
alter database [chameleon] SET MULTI_USER
GO
alter database [chameleon] SET PAGE_VERIFY CHECKSUM
GO
alter database [chameleon] SET DB_CHAINING OFF
GO
alter database [chameleon] SET FILESTREAM ( NON_TRANSACTED_ACCESS = OFF )
GO
alter database [chameleon] SET TARGET_RECOVERY_TIME = 60 SECONDS
GO
alter database [chameleon] SET DELAYED_DURABILITY = DISABLED
GO
alter database [chameleon] SET ACCELERATED_DATABASE_RECOVERY = OFF
GO
EXEC sys.sp_db_vardecimal_storage_format N'chameleon', N'ON'
GO
alter database [chameleon] SET QUERY_STORE = OFF
GO
USE [chameleon]
GO
/****** Object:  Table [dbo].[AdmissionTreatmentDecision]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[AdmissionTreatmentDecision]
(
    [Decision]       [int]      NULL,
    [Hosp_Unit]      [int]      NULL,
    [Delete_Date]    [datetime] NULL,
    [Medical_Record] [int]      NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[faker_answer_HospUnit]
(
    [decision] [int] NULL,
    [name]     [int] NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[MedicalRecords]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[MedicalRecords]
(
    [Medical_Record] [int]      NULL,
    [Delete_Date]    [datetime] NULL,
    [Unit]           [int]      NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ResponsibleDoctor]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[ResponsibleDoctor]
(
    [Doctor]         [nvarchar](150) NULL,
    [Medical_Record] [int]           NULL,
    [Delete_Date]    [datetime]      NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SystemUnits]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[SystemUnits]
(
    [Unit] [int]           NULL,
    [Name] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TableAnswers]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[TableAnswers]
(
    [Answer_Code] [int]           NULL,
    [Answer_Text] [nvarchar](150) NULL,
    [Table_Code]  [int]           NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TreatmentCause]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[TreatmentCause]
(
    [remarks]        [nvarchar](2000) NULL,
    [Medical_Record] [bigint]         NULL,
    [Entry_Date]     [datetime]       NULL,
    [delete_date]    [datetime]       NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[Users]
(
    [usernamenotitle] [nvarchar](150) NULL,
    [Code]            [nvarchar](150) NULL
) ON [PRIMARY]
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[faker_wing_Doctor]
(
    [DepartmentWing] [nvarchar](150) NULL,
    [Code]           [nvarchar](150) NULL
) ON [PRIMARY]
GO
create TABLE [dbo].[RoomBeds]
(
    [Row_ID]   [int]           NULL,
    [Bed_Name] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[RoomDetails]    Script Date: 23/06/2022 9:09:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[RoomDetails]
(
    [Room_Code] [int]           NULL,
    [Unit]      [int]           NULL,
    [Beds]      [int]           NULL,
    [Room_Name] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[RoomPlacmentPatient]    Script Date: 23/06/2022 9:09:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[RoomPlacmentPatient]
(
    [Start_Date]     [datetime] NULL,
    [End_Date]       [datetime] NULL,
    [Unit]           [int]      NULL,
    [Bed_ID]         [int]      NULL,
    [Medical_Record] [int]      NULL,
    [Room]           [int]      NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[faker_beds]
(
    [room]     [nvarchar](150) NOT NULL,
    [bed_name] [nvarchar](150) NOT NULL,
    [row_id]   [int]           NOT NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[MedicalRecords](
	[Patient] [bigint] NULL,
	[Medical_Record] [bigint] NULL,
	[Record_Date] [datetime] NULL,
    [Unit] [int] NULL,
	[Delete_Date] [datetime] NULL
) ON [PRIMARY]
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'819000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'834000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'836000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'837000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'853000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'859000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'860000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'870000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'871000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'872000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'873000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'874000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'875000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'876000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'972000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'1505100')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'1539200')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'1549983')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15054500')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15059312')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15063421')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15064114')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15065323')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15066727')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068347')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068369')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068397')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068422')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068423')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068448')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068510')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068531')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068593')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068594')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068596')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068598')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (1, N'15068666')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name])
VALUES (2, NULL)
GO
delete
from [dbo].[faker_beds]
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'1', 1)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'2', 2)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'3', 3)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'4', 4)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'5', 5)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'6', 6)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'7', 7)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'8', 8)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'9', 9)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'10', 10)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'11', 11)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B1', N'12', 12)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'1', 13)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'2', 14)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'3', 15)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'4', 16)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'5', 17)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'6', 18)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'7', 19)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'8', 20)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'9', 21)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'10', 22)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'11', 23)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B2', N'12', 24)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'1', 25)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'2', 26)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'3', 27)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'4', 28)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'5', 29)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'6', 30)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'7', 31)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'8', 32)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'9', 33)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'10', 34)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'11', 35)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'12', 36)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'13', 37)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'14', 38)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'15', 39)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף B3', N'16', 40)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף הולכים', N'1', 41)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף הולכים', N'2', 42)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף הולכים', N'3', 43)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף הולכים', N'4', 44)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'אגף הולכים', N'5', 45)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'חדר הלם', N'1', 46)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'חדר הלם', N'2', 47)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'חדר הלם', N'3', 48)
GO
insert [dbo].[faker_beds] ([room], [bed_name], [row_id])
VALUES (N'חדר הלם', N'4', 49)
GO
SET IDENTITY_INSERT [dbo].[RoomBeds] ON
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'1', 1)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'2', 2)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'3', 3)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'4', 4)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'5', 5)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'6', 6)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'7', 7)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'8', 8)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'9', 9)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'10', 10)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'11', 11)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'12', 12)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'13', 13)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'14', 14)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'15', 15)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'16', 16)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'17', 17)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'18', 18)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'19', 19)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'20', 20)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'21', 21)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'22', 22)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'23', 23)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'24', 24)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'25', 25)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'26', 26)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'27', 27)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'28', 28)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'29', 29)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'30', 30)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'31', 31)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'32', 32)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'33', 33)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'34', 34)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'35', 35)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'36', 36)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'37', 37)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'38', 38)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'39', 39)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'40', 40)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'1', 41)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'2', 42)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'3', 43)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'4', 44)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'5', 45)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'1', 46)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'2', 47)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'3', 48)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id])
VALUES (N'4', 49)
GO
SET IDENTITY_INSERT [dbo].[RoomBeds] OFF
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (1, 1184000, 12, N'אגף B2')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (2, 1184000, 16, N'אגף B3')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (3, 1184000, 5, N'אגף הולכים')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (4, 1184000, 4, N'חדר הלם')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (5, 1184000, 12, N'אגף B1')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (6, 1184000, 15, N'אגף פסיכיאטרי')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (7, 1184000, 37, N'בידוד אדום')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (8, 1184000, 99, N'אגף אנטיגן')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name])
VALUES (9, 1184000, 99, N'אגף שוכבים ירוק')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (819000, N'פנימית גריאטריה ג')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (834000, N'כירורגית חזה-כלי דם')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (836000, N'כירורגית ב')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (837000, N'כירורגית ג')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (853000, N'כירורגית ילדים')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (859000, N'כירורגית כויות')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (860000, N'כירורגית לב')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (870000, N'כירורגית פה ולסת')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (871000, N'פנימית א')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (872000, N'פנימית ב')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (873000, N'פנימית ג')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (874000, N'פנימית ד')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (875000, N'פנימית ה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (876000, N'פנימית ו')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (972000, N'אשפוז יום שיקום ילדים')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (1505100, N'אשפוז יום שיקומי - לצפייה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (1539200, N'אשפוז יום פסיכיאטרי')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (1549983, N'פנימית בלינסון')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15054500, N'כירורגית לב ילדים')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15059312, N'אשפוז יום גניקולוגי')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15063421, N'פנימית')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15064114, N'אשפוז יום נפגעי ראש - לצפייה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15065323, N'פנימית ט')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15066727, N'אשפוז יום נוירואונקולוגי')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068347, N'אשפוז יום הפרעות אכילה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068369, N'פנימית גריאטריה ד')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068397, N'אשפוז יום נשימתי - לצפייה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068422, N'כירורגית חזה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068423, N'כירורגית כלי דם')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068448, N'וירטואלי פנימית א')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068510, N'אשפוז')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068531, N'אשפוז כירורגי קצר')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068593, N'פנימית קורונה ג')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068594, N'פנימית קורונה ד')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068596, N'פנימית קורונה ב')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068598, N'פנימית קורונה ה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (15068666, N'פנימית קורונה ח')
GO
insert [dbo].[SystemUnits] ([Unit], [Name])
VALUES (1184000, N'המחלקה לרפואה דחופה')
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (1, N'אשפוז', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (3, N'אשפוז בית', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (4, N'באולטרסאונד גינקולוגי', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (5, N'בדיקה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (6, N'בדיקה חוזרת', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (7, N'בירור', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (8, N'במיון הכללי', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (9, N'במיון כללי', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (10, N'הלך על דעת עצמו', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (11, N'המתנה למעבדה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (12, N'העברה לחדר לידה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (13, N'העברה לצינתורים', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (14, N'השראת לידה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (15, N'חדר לידה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (16, N'חדר ניתוח', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (17, N'חזרה לאשפוז', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (18, N'חזרה למחלקת האשפוז', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (19, N'חזרה למיון', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (20, N'ממתינה לאולטרסאונד', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (21, N'ניטור', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (22, N'נפטר במיון', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (23, N'נפטר/ה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (24, N'עבר למיון אחר', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (25, N'עזבו על דעת עצמם', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code])
VALUES (2, N'שחרור', 1092)
GO
insert [dbo].[Users] ([usernamenotitle], [Code])
VALUES (N'ניסים אהרון', N'1')
GO
insert [dbo].[Users] ([usernamenotitle], [Code])
VALUES (N'שירה גרינשטיין', N'2')
GO
insert [dbo].[Users] ([usernamenotitle], [Code])
VALUES (N'ניצן חלבי', N'3')
GO
insert [dbo].[Users] ([usernamenotitle], [Code])
VALUES (N'עמית גזית', N'4')
GO
insert into [dbo].[faker_wing_Doctor]
values (N'אגף הולכים', 1),
       (N'אגף הולכים', 5),
       (N'אגף B1', 2),
       (N'אגף B1', 3),
       (N'אגף B2', 4),
       (N'אגף B2', 6),
       (N'אגף B3', 7),
       (N'אגף B3', 8)
go
insert into [dbo].[Users] ([usernamenotitle], [Code])
VALUES (N'אחמד מלמוד', 5),
       (N'מוחמד דבור', 6),
       (N'אילנית כהן', 7),
       (N'נגב ניצן', 8)
GO
USE [master]
GO
alter database [chameleon] SET READ_WRITE
GO

USE [master]
GO
CREATE LOGIN [arc_cham_login] WITH PASSWORD='Password123', DEFAULT_DATABASE=[master], DEFAULT_LANGUAGE=[us_english], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF
GO

ALTER SERVER ROLE [sysadmin] ADD MEMBER [arc_cham_login]
GO

ALTER SERVER ROLE [serveradmin] ADD MEMBER [arc_cham_login]
GO
USE [chameleon]
GO
CREATE USER [arc_cham_login] FOR LOGIN [arc_cham_login]
GO
USE [chameleon]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [arc_cham_login]
GO
USE [chameleon]
GO
ALTER ROLE [db_owner] ADD MEMBER [arc_cham_login]
GO
USE [master]
GO
CREATE USER [arc_cham_login] FOR LOGIN [arc_cham_login]
GO
USE [master]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [arc_cham_login]
GO
USE [master]
GO
ALTER ROLE [db_owner] ADD MEMBER [arc_cham_login]
GO
USE [model]
GO
CREATE USER [arc_cham_login] FOR LOGIN [arc_cham_login]
GO
USE [model]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [arc_cham_login]
GO
USE [model]
GO
ALTER ROLE [db_owner] ADD MEMBER [arc_cham_login]
GO
USE [msdb]
GO
CREATE USER [arc_cham_login] FOR LOGIN [arc_cham_login]
GO
USE [msdb]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [arc_cham_login]
GO
USE [msdb]
GO
ALTER ROLE [db_owner] ADD MEMBER [arc_cham_login]
GO
USE [tempdb]
GO
CREATE USER [arc_cham_login] FOR LOGIN [arc_cham_login]
GO
USE [tempdb]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [arc_cham_login]
GO
USE [tempdb]
GO
ALTER ROLE [db_owner] ADD MEMBER [arc_cham_login]
GO
use [master]
GO
GRANT ALTER ANY CONNECTION TO [arc_cham_login]
GO
use [master]
GO
GRANT ALTER ANY LINKED SERVER TO [arc_cham_login]
GO
use [master]
GO
GRANT ALTER ANY LOGIN TO [arc_cham_login]
GO
use [master]
GO
GRANT CONNECT ANY DATABASE TO [arc_cham_login]
GO
use [master]
GO
GRANT IMPERSONATE ANY LOGIN TO [arc_cham_login]
GO