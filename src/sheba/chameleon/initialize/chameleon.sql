USE [master]
GO
/****** Object:  Database [chameleon_db]    Script Date: 13/04/2022 0:44:08 ******/
create DATABASE [chameleon_db]
    CONTAINMENT = NONE
    ON PRIMARY
    ( NAME = N'chameleon_db', FILENAME = N'/var/opt/mssql/data/chameleon_db.mdf' , SIZE = 8192 KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536 KB )
    LOG ON
    ( NAME = N'chameleon_db_log', FILENAME = N'/var/opt/mssql/data/chameleon_db_log.ldf' , SIZE = 8192 KB , MAXSIZE = 2048 GB , FILEGROWTH = 65536 KB )
    COLLATE Hebrew_CI_AS
GO
alter database [chameleon_db] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
    begin
        EXEC [chameleon_db].[dbo].[sp_fulltext_database] @action = 'enable'
    end
GO
ALTER DATABASE [chameleon_db] SET ANSI_NULL_DEFAULT OFF
GO
alter database [chameleon_db] SET ANSI_NULLS OFF
GO
alter database [chameleon_db] SET ANSI_PADDING OFF
GO
alter database [chameleon_db] SET ANSI_WARNINGS OFF
GO
alter database [chameleon_db] SET ARITHABORT OFF
GO
alter database [chameleon_db] SET AUTO_CLOSE OFF
GO
alter database [chameleon_db] SET AUTO_SHRINK OFF
GO
alter database [chameleon_db] SET AUTO_UPDATE_STATISTICS ON
GO
alter database [chameleon_db] SET CURSOR_CLOSE_ON_COMMIT OFF
GO
alter database [chameleon_db] SET CURSOR_DEFAULT GLOBAL
GO
alter database [chameleon_db] SET CONCAT_NULL_YIELDS_NULL OFF
GO
alter database [chameleon_db] SET NUMERIC_ROUNDABORT OFF
GO
alter database [chameleon_db] SET QUOTED_IDENTIFIER OFF
GO
alter database [chameleon_db] SET RECURSIVE_TRIGGERS OFF
GO
alter database [chameleon_db] SET DISABLE_BROKER
GO
alter database [chameleon_db] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO
alter database [chameleon_db] SET DATE_CORRELATION_OPTIMIZATION OFF
GO
alter database [chameleon_db] SET TRUSTWORTHY OFF
GO
alter database [chameleon_db] SET ALLOW_SNAPSHOT_ISOLATION OFF
GO
alter database [chameleon_db] SET PARAMETERIZATION SIMPLE
GO
alter database [chameleon_db] SET READ_COMMITTED_SNAPSHOT OFF
GO
alter database [chameleon_db] SET HONOR_BROKER_PRIORITY OFF
GO
alter database [chameleon_db] SET RECOVERY FULL
GO
alter database [chameleon_db] SET MULTI_USER
GO
alter database [chameleon_db] SET PAGE_VERIFY CHECKSUM
GO
alter database [chameleon_db] SET DB_CHAINING OFF
GO
alter database [chameleon_db] SET FILESTREAM ( NON_TRANSACTED_ACCESS = OFF )
GO
alter database [chameleon_db] SET TARGET_RECOVERY_TIME = 60 SECONDS
GO
alter database [chameleon_db] SET DELAYED_DURABILITY = DISABLED
GO
alter database [chameleon_db] SET ACCELERATED_DATABASE_RECOVERY = OFF
GO
EXEC sys.sp_db_vardecimal_storage_format N'chameleon_db', N'ON'
GO
alter database [chameleon_db] SET QUERY_STORE = OFF
GO
USE [chameleon_db]
GO
/****** Object:  Table [dbo].[patients]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[patients]
(
    [id]         [int] IDENTITY (1,1) NOT NULL,
    [first_name] [varchar](200)       NULL,
    [last_name]  [varchar](200)       NULL,
    [gender]     [varchar](2)         NULL,
    [birth_date] [datetime]           NULL,
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Emergency_visits]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[Emergency_visits]
(
    [id]                      [int] IDENTITY (1,1) NOT NULL,
    [DepartmentName]          [varchar](200)       NULL,
    [DepartmentWing]          [varchar](200)       NULL,
    [DepartmentAdmission]     [datetime]           NULL,
    [DepartmentWingDischarge] [datetime]           NULL,
    [MainCause]               [varchar](200)       NULL,
    [esi]                     [int]                NULL,
    [DepartmentCode]          [int]                NULL,
    --[medical_record]      [int]                NULL,
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[measurements]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[measurements]
(
    [id]             [varchar](250) NOT NULL,
    [entry_time]     [datetime]     NULL,
    [ParameterCode]  [int]          NOT NULL,
    [Parameter_Name] [varchar](200) NULL,
    [Result]         [float]        NULL,
    [Min_Value]      [float]        NULL,
    [Max_Value]      [float]        NULL,
) ON [PRIMARY]
GO
create TABLE [dbo].[Imaging]
(
    [sps_key]              [int] IDENTITY (1,1) NOT NULL,
    [id]                   [int]                NOT NULL,
    [OrderDate]            [datetime]           NOT NULL,
    [OrderedProcedureType] [varchar](100)       NOT NULL,
    [ProcedureStatus]      [varchar](100)       NOT NULL,
    [Interpretation]       [varchar](300)       NULL,
)
GO
CREATE TABLE [dbo].[lab_results]
(
    [id]             int            NOT NULL,
    [TestCode]       [int]          NOT NULL,
    [TestName]       [varchar](150) NULL,
    [result]         [varchar](60)  NULL,
    [NormMinimum]    [float]        NULL,
    [NormMaximum]    [float]        NULL,
    [OrderDate]      [datetime]     NOT NULL,
    [collectiondate] [datetime]     NULL,
    [ResultTime]     [datetime]     NULL,
)
GO
CREATE TABLE [dbo].[medical_free_text]
(
    [Row_ID]           [BIGINT] IDENTITY (1,1) PRIMARY KEY,
    [Id]               [BIGINT]       NULL,
    [Medical_Record]   [BIGINT]       NULL,
    [DocumentingDate]  [DATE]         NULL,
    [DocumentingTime]  [DATETIME]     NULL,
    [unit_name]        [VARCHAR](80)  NULL,
    [Unit]             [BIGINT]       NULL,
    [Description_code] [BIGINT]       NULL,
    [Description]      [VARCHAR](500) NULL,
    [Description_Text] [VARCHAR](MAX) NULL,
    [DocumentingUser]  [BIGINT]       NULL,
    [source]           [VARCHAR](25)  NULL,
    /*date of insert the row to ARC db*/
    [insert_date]      [DATETIME]     NULL

)
GO
CREATE TABLE [dbo].[referrals]
(
    [ReferralCode]  [int] IDENTITY (1,1) NOT NULL,
    [id]            [int]                NOT NULL,
    [DoctorName]    [varchar](50)        NULL,
    [OrderDate]     [datetime]           NULL,
    [CompletedDate] [datetime]           NULL,
) ON [PRIMARY]
GO
alter database [chameleon_db] SET READ_WRITE
USE [master]
GO
/****** Object:  Database [sbwnd81c_chameleon]    Script Date: 12/06/2022 1:01:52 ******/
CREATE DATABASE [sbwnd81c_chameleon]
    CONTAINMENT = NONE
    ON PRIMARY
    ( NAME = N'sbwnd81c_chameleon', FILENAME = N'/var/opt/mssql/data/sbwnd81c_chameleon.mdf' , SIZE = 8192 KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536 KB )
    LOG ON
    ( NAME = N'sbwnd81c_chameleon_log', FILENAME = N'/var/opt/mssql/data/sbwnd81c_chameleon_log.ldf' , SIZE = 8192 KB , MAXSIZE = 2048 GB , FILEGROWTH = 65536 KB )
    COLLATE Hebrew_CI_AS
GO
ALTER DATABASE [sbwnd81c_chameleon] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
    begin
        EXEC [sbwnd81c_chameleon].[dbo].[sp_fulltext_database] @action = 'enable'
    end
GO
ALTER DATABASE [sbwnd81c_chameleon] SET ANSI_NULL_DEFAULT OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET ANSI_NULLS OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET ANSI_PADDING OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET ANSI_WARNINGS OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET ARITHABORT OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET AUTO_CLOSE OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET AUTO_SHRINK OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET AUTO_UPDATE_STATISTICS ON
GO
ALTER DATABASE [sbwnd81c_chameleon] SET CURSOR_CLOSE_ON_COMMIT OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET CURSOR_DEFAULT GLOBAL
GO
ALTER DATABASE [sbwnd81c_chameleon] SET CONCAT_NULL_YIELDS_NULL OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET NUMERIC_ROUNDABORT OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET QUOTED_IDENTIFIER OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET RECURSIVE_TRIGGERS OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET DISABLE_BROKER
GO
ALTER DATABASE [sbwnd81c_chameleon] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET DATE_CORRELATION_OPTIMIZATION OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET TRUSTWORTHY OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET ALLOW_SNAPSHOT_ISOLATION OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET PARAMETERIZATION SIMPLE
GO
ALTER DATABASE [sbwnd81c_chameleon] SET READ_COMMITTED_SNAPSHOT OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET HONOR_BROKER_PRIORITY OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET RECOVERY FULL
GO
ALTER DATABASE [sbwnd81c_chameleon] SET MULTI_USER
GO
ALTER DATABASE [sbwnd81c_chameleon] SET PAGE_VERIFY CHECKSUM
GO
ALTER DATABASE [sbwnd81c_chameleon] SET DB_CHAINING OFF
GO
ALTER DATABASE [sbwnd81c_chameleon] SET FILESTREAM ( NON_TRANSACTED_ACCESS = OFF )
GO
ALTER DATABASE [sbwnd81c_chameleon] SET TARGET_RECOVERY_TIME = 60 SECONDS
GO
ALTER DATABASE [sbwnd81c_chameleon] SET DELAYED_DURABILITY = DISABLED
GO
ALTER DATABASE [sbwnd81c_chameleon] SET ACCELERATED_DATABASE_RECOVERY = OFF
GO
EXEC sys.sp_db_vardecimal_storage_format N'sbwnd81c_chameleon', N'ON'
GO
ALTER DATABASE [sbwnd81c_chameleon] SET QUERY_STORE = OFF
GO
USE [sbwnd81c_chameleon]
GO
/****** Object:  Table [dbo].[AdmissionTreatmentDecision]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[AdmissionTreatmentDecision]
(
    [Decision]       [nvarchar](150) NULL,
    [Hosp_Unit]      [int]           NULL,
    [Delete_Date]    [datetime]      NULL,
    [Medical_Record] [int]           NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[MedicalRecords]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MedicalRecords]
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
CREATE TABLE [dbo].[ResponsibleDoctor]
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
CREATE TABLE [dbo].[SystemUnits]
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
CREATE TABLE [dbo].[TableAnswers]
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
CREATE TABLE [dbo].[TreatmentCause]
(
    [remarks]        [nvarchar](250) NULL,
    [Medical_Record] [int]           NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users]
(
    [usernamenotitle] [nvarchar](150) NULL,
    [Code]            [nvarchar](150) NULL
) ON [PRIMARY]
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[faker_wing_Doctore](
	[DepartmentWing] [nvarchar](150) NULL,
	[Code] [nvarchar](150) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[RoomBeds](
	[Row_ID] [int] NULL,
	[Bed_Name] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[RoomDetails]    Script Date: 23/06/2022 9:09:52 ******/
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
/****** Object:  Table [dbo].[RoomPlacmentPatient]    Script Date: 23/06/2022 9:09:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[RoomPlacmentPatient](
	[Start_Date] [datetime] NULL,
	[End_Date] [datetime] NULL,
	[Unit] [int] NULL,
	[Bed_ID] [int] NULL,
	[Medical_Record] [int] NULL,
	[Room] [nvarchar](150) NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[faker_beds](
	[room] [nvarchar](150) NULL,
	[row_id] [nvarchar](150) NULL
) ON [PRIMARY]
GO
INSERT [dbo].[AdmissionTreatmentDecision] ([Decision], [Hosp_Unit], [Delete_Date], [Medical_Record]) VALUES (N'2', 118390, NULL, 1111111)
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'1')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'2')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'3')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'4')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'5')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'6')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'7')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'8')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'9')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'10')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'11')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'12')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'13')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'14')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'1')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'2')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'3')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'4')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'5')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'6')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'7')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'8')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'9')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'10')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'11')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'12')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'13')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'14')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'15')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'16')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'17')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'18')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'19')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'20')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'1')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'2')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'3')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'4')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'5')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'6')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'7')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'8')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'9')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'10')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'11')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'12')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'13')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'1')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'2')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'3')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'4')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'5')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'6')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'7')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'8')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'9')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'10')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'11')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'12')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'13')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'14')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'15')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'16')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'17')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'18')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'19')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'20')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'21')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'22')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'23')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'24')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'25')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'26')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'27')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'28')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'29')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'30')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'31')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'32')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'33')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'34')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'35')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'36')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'37')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'38')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'39')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'40')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'41')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'42')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'43')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'44')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'45')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'46')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'47')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'48')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'49')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'50')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'51')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'52')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'53')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'54')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'55')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'56')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'57')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'58')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'59')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'60')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'61')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'62')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'63')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'64')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'65')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'66')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'67')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'68')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'69')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'70')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'71')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'72')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'73')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'74')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'75')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'76')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'77')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'78')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'79')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'80')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'81')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'82')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'83')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'84')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'85')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'86')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'87')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'88')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'89')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'90')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'91')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'92')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'93')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'94')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'95')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'96')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'97')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'98')
GO
INSERT [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'99')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (1, 1184000, 14, N'אגף B2')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (2, 1184000, 20, N'אגף B3')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (3, 1184000, 99, N'אגף הולכים')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (4, 1184000, 5, N'חדר הלם')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (5, 1184000, 13, N'אגף B1')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (6, 1184000, 15, N'אגף פסיכיאטרי')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (7, 1184000, 37, N'בידוד אדום')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (8, 1184000, 99, N'אגף אנטיגן')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (9, 1184000, 99, N'אגף שוכבים ירוק')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (123, N'השהיה מלרד')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (126, N'נוירולוגיה')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (124, N'עור ומין')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (125, N'פנימית')
GO
INSERT [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1184000, N'המחלקה לרפואה דחופה')
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (1, N'אחר', 1092)
GO
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (2, N'אשפוז', 1092)
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
INSERT [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (26, N'שחרור', 1092)
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code]) VALUES (N'ניסים אהרון', N'1')
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code]) VALUES (N'שירה גרינשטיין', N'2')
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code]) VALUES (N'ניצן חלבי', N'3')
GO
INSERT [dbo].[Users] ([usernamenotitle], [Code]) VALUES (N'עמית גזית', N'4')
GO
/****** Object:  StoredProcedure [dbo].[faker_ResponsibleDoctor]    Script Date: 23/06/2022 10:09:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[faker_ResponsibleDoctor](@medical_record nvarchar(50))
	AS
	Begin
	if exists (select * from [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] rd where rd.medical_record=@medical_record and rd.delete_date is null)
		begin
			update [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] set  delete_date= GETDATE() where medical_record=@medical_record and delete_date is null;
			insert into [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] values(
			(select top 1 rd.doctor from (select top 1 id,DepartmentWing from [chameleon_db].[dbo].[Emergency_visits] order by DepartmentAdmission desc) ev
			join [sbwnd81c_chameleon].[dbo].[faker_wing_Doctore] as fwd on fwd.DepartmentWing=ev.DepartmentWing
			join [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] as rd on rd.doctor = fwd.code
			where id=@medical_record
			group by  rd.doctor
			order by count(*) asc),@medical_record,null);
		end
	else
		begin
			insert into [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] values(select top 1 fwd.code from (select top 1 DepartmentWing from [chameleon_db].[dbo].[Emergency_visits] where
            id=@medical_record and
            DepartmentWingDischarge is null ) ev
            join [sbwnd81c_chameleon].[dbo].[faker_wing_Doctore] as fwd on fwd.DepartmentWing=ev.DepartmentWing
            left join [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] as rd on rd.doctor = fwd.code
            group by  rd.doctor
            order by count(*) asc),@medical_record,null);
		end
	end
GO
/****** Object:  StoredProcedure [dbo].[faker_RoomPlacmentPatient_admission]    Script Date: 23/06/2022 10:09:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[faker_RoomPlacmentPatient_admission](@medical_record int,@room_num nvarchar)
	AS
	Begin
	declare @bed_name as varchar;
	-- insert into @bed_name
	select  top 1 @bed_name= fb.row_id  from [sbwnd81c_chameleon].[dbo].[faker_beds] fb
	where row_id not in (select bed_id from [sbwnd81c_chameleon].[dbo].[RoomPlacmentPatient] rpp where rpp.unit=1184000 and rpp.end_date is not null and rpp.start_date is not null and room =@room_num)
	and room=@room_num
	order by newid();
	insert into  [sbwnd81c_chameleon].[dbo].[RoomPlacmentPatient]  values (GETUTCDATE(), null,1184000,@bed_name,@medical_record ,@room_num);
	end
	;
GO
/****** Object:  StoredProcedure [dbo].[faker_RoomPlacmentPatient_dismission]    Script Date: 23/06/2022 10:09:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
	CREATE PROCEDURE [dbo].[faker_RoomPlacmentPatient_dismission](@medical_record nvarchar(50))
	AS
	Begin
	update [sbwnd81c_chameleon].[dbo].[RoomPlacmentPatient] set end_date = GETUTCDATE() where [Medical_Record]=@medical_record and end_date is null;
	end
	;
GO
USE [master]
GO
ALTER DATABASE [sbwnd81c_chameleon] SET READ_WRITE
GO
