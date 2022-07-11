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
create TABLE [dbo].[lab_results]
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
create TABLE [dbo].[medical_free_text]
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
create TABLE [dbo].[referrals]
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
create DATABASE [sbwnd81c_chameleon]
    CONTAINMENT = NONE
    ON PRIMARY
    ( NAME = N'sbwnd81c_chameleon', FILENAME = N'/var/opt/mssql/data/sbwnd81c_chameleon.mdf' , SIZE = 8192 KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536 KB )
    LOG ON
    ( NAME = N'sbwnd81c_chameleon_log', FILENAME = N'/var/opt/mssql/data/sbwnd81c_chameleon_log.ldf' , SIZE = 8192 KB , MAXSIZE = 2048 GB , FILEGROWTH = 65536 KB )
    COLLATE Hebrew_CI_AS
GO
alter database [sbwnd81c_chameleon] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
    begin
        EXEC [sbwnd81c_chameleon].[dbo].[sp_fulltext_database] @action = 'enable'
    end
GO
ALTER DATABASE [sbwnd81c_chameleon] SET ANSI_NULL_DEFAULT OFF
GO
alter database [sbwnd81c_chameleon] SET ANSI_NULLS OFF
GO
alter database [sbwnd81c_chameleon] SET ANSI_PADDING OFF
GO
alter database [sbwnd81c_chameleon] SET ANSI_WARNINGS OFF
GO
alter database [sbwnd81c_chameleon] SET ARITHABORT OFF
GO
alter database [sbwnd81c_chameleon] SET AUTO_CLOSE OFF
GO
alter database [sbwnd81c_chameleon] SET AUTO_SHRINK OFF
GO
alter database [sbwnd81c_chameleon] SET AUTO_UPDATE_STATISTICS ON
GO
alter database [sbwnd81c_chameleon] SET CURSOR_CLOSE_ON_COMMIT OFF
GO
alter database [sbwnd81c_chameleon] SET CURSOR_DEFAULT GLOBAL
GO
alter database [sbwnd81c_chameleon] SET CONCAT_NULL_YIELDS_NULL OFF
GO
alter database [sbwnd81c_chameleon] SET NUMERIC_ROUNDABORT OFF
GO
alter database [sbwnd81c_chameleon] SET QUOTED_IDENTIFIER OFF
GO
alter database [sbwnd81c_chameleon] SET RECURSIVE_TRIGGERS OFF
GO
alter database [sbwnd81c_chameleon] SET DISABLE_BROKER
GO
alter database [sbwnd81c_chameleon] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO
alter database [sbwnd81c_chameleon] SET DATE_CORRELATION_OPTIMIZATION OFF
GO
alter database [sbwnd81c_chameleon] SET TRUSTWORTHY OFF
GO
alter database [sbwnd81c_chameleon] SET ALLOW_SNAPSHOT_ISOLATION OFF
GO
alter database [sbwnd81c_chameleon] SET PARAMETERIZATION SIMPLE
GO
alter database [sbwnd81c_chameleon] SET READ_COMMITTED_SNAPSHOT OFF
GO
alter database [sbwnd81c_chameleon] SET HONOR_BROKER_PRIORITY OFF
GO
alter database [sbwnd81c_chameleon] SET RECOVERY FULL
GO
alter database [sbwnd81c_chameleon] SET MULTI_USER
GO
alter database [sbwnd81c_chameleon] SET PAGE_VERIFY CHECKSUM
GO
alter database [sbwnd81c_chameleon] SET DB_CHAINING OFF
GO
alter database [sbwnd81c_chameleon] SET FILESTREAM ( NON_TRANSACTED_ACCESS = OFF )
GO
alter database [sbwnd81c_chameleon] SET TARGET_RECOVERY_TIME = 60 SECONDS
GO
alter database [sbwnd81c_chameleon] SET DELAYED_DURABILITY = DISABLED
GO
alter database [sbwnd81c_chameleon] SET ACCELERATED_DATABASE_RECOVERY = OFF
GO
EXEC sys.sp_db_vardecimal_storage_format N'sbwnd81c_chameleon', N'ON'
GO
alter database [sbwnd81c_chameleon] SET QUERY_STORE = OFF
GO
USE [sbwnd81c_chameleon]
GO
/****** Object:  Table [dbo].[AdmissionTreatmentDecision]    Script Date: 12/06/2022 1:01:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[AdmissionTreatmentDecision]
(
    [Decision]       [int] NULL,
    [Hosp_Unit]      [int]           NULL,
    [Delete_Date]    [datetime]      NULL,
    [Medical_Record] [int]           NULL
) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[faker_answer_HospUnit](
	[decision] [int] NULL,
	[name] [int] NULL
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
    [remarks]        [nvarchar](250) NULL,
    [Medical_Record] [int]           NULL,
    [delete_date]  [datetime]
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
create TABLE [dbo].[faker_wing_Doctor](
	[DepartmentWing] [nvarchar](150) NULL,
	[Code] [nvarchar](150) NULL
) ON [PRIMARY]
GO
create TABLE [dbo].[RoomBeds](
	[Row_ID] [int] NULL,
	[Bed_Name] [nvarchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[RoomDetails]    Script Date: 23/06/2022 9:09:52 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[RoomDetails](
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
create TABLE [dbo].[RoomPlacmentPatient](
	[Start_Date] [datetime] NULL,
	[End_Date] [datetime] NULL,
	[Unit] [int] NULL,
	[Bed_ID] [int] NULL,
	[Medical_Record] [int] NULL,
	[Room] [nvarchar](150) NULL
) ON [PRIMARY]
GO
create TABLE [dbo].[faker_beds](
	[room] [nvarchar](150) NULL,
	[row_id] [nvarchar](150) NULL
) ON [PRIMARY]
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'819000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'834000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'836000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'837000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'853000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'859000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'860000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'870000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'871000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'872000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'873000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'874000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'875000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'876000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'972000')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'1505100')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'1539200')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'1549983')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15054500')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15059312')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15063421')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15064114')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15065323')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15066727')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068347')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068369')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068397')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068422')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068423')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068448')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068510')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068531')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068593')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068594')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068596')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068598')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (1, N'15068666')
GO
insert [dbo].[faker_answer_HospUnit] ([decision], [name]) VALUES (2, NULL)
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'1')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'2')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'3')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'4')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'5')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'6')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'7')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'8')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'9')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'10')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'11')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'12')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'13')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b1', N'14')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'1')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'2')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'3')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'4')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'5')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'6')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'7')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'8')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'9')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'10')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'11')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'12')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'13')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'14')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'15')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'16')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'17')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'18')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'19')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b2', N'20')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'1')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'2')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'3')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'4')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'5')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'6')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'7')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'8')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'9')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'10')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'11')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'12')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'b3', N'13')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'1')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'2')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'3')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'4')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'5')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'6')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'7')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'8')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'9')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'10')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'11')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'12')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'13')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'14')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'15')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'16')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'17')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'18')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'19')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'20')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'21')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'22')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'23')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'24')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'25')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'26')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'27')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'28')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'29')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'30')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'31')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'32')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'33')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'34')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'35')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'36')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'37')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'38')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'39')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'40')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'41')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'42')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'43')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'44')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'45')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'46')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'47')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'48')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'49')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'50')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'51')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'52')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'53')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'54')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'55')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'56')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'57')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'58')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'59')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'60')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'61')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'62')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'63')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'64')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'65')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'66')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'67')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'68')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'69')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'70')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'71')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'72')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'73')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'74')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'75')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'76')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'77')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'78')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'79')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'80')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'81')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'82')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'83')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'84')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'85')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'86')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'87')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'88')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'89')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'90')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'91')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'92')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'93')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'94')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'95')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'96')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'97')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'98')
GO
insert [dbo].[faker_beds] ([room], [row_id]) VALUES (N'a', N'99')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (1, 1184000, 14, N'אגף B2')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (2, 1184000, 20, N'אגף B3')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (3, 1184000, 99, N'אגף הולכים')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (4, 1184000, 5, N'חדר הלם')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (5, 1184000, 13, N'אגף B1')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (6, 1184000, 15, N'אגף פסיכיאטרי')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (7, 1184000, 37, N'בידוד אדום')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (8, 1184000, 99, N'אגף אנטיגן')
GO
insert [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (9, 1184000, 99, N'אגף שוכבים ירוק')
GO
insert [dbo].[RoomPlacmentPatient] ([Start_Date], [End_Date], [Unit], [Bed_ID], [Medical_Record], [Room]) VALUES (CAST(N'2022-06-23T06:59:11.777' AS DateTime), NULL, 1184000, 7, 123345345, N'a')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (819000, N'פנימית גריאטריה ג')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (834000, N'כירורגית חזה-כלי דם')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (836000, N'כירורגית ב')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (837000, N'כירורגית ג')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (853000, N'כירורגית ילדים')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (859000, N'כירורגית כויות')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (860000, N'כירורגית לב')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (870000, N'כירורגית פה ולסת')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (871000, N'פנימית א')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (872000, N'פנימית ב')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (873000, N'פנימית ג')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (874000, N'פנימית ד')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (875000, N'פנימית ה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (876000, N'פנימית ו')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (972000, N'אשפוז יום שיקום ילדים')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1505100, N'אשפוז יום שיקומי - לצפייה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1539200, N'אשפוז יום פסיכיאטרי')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1549983, N'פנימית בלינסון')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15054500, N'כירורגית לב ילדים')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15059312, N'אשפוז יום גניקולוגי')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15063421, N'פנימית')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15064114, N'אשפוז יום נפגעי ראש - לצפייה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15065323, N'פנימית ט')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15066727, N'אשפוז יום נוירואונקולוגי')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068347, N'אשפוז יום הפרעות אכילה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068369, N'פנימית גריאטריה ד')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068397, N'אשפוז יום נשימתי - לצפייה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068422, N'כירורגית חזה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068423, N'כירורגית כלי דם')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068448, N'וירטואלי פנימית א')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068510, N'אשפוז')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068531, N'אשפוז כירורגי קצר')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068593, N'פנימית קורונה ג')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068594, N'פנימית קורונה ד')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068596, N'פנימית קורונה ב')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068598, N'פנימית קורונה ה')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (15068666, N'פנימית קורונה ח')
GO
insert [dbo].[SystemUnits] ([Unit], [Name]) VALUES (1184000, N'המחלקה לרפואה דחופה')
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (1, N'אשפוז', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (3, N'אשפוז בית', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (4, N'באולטרסאונד גינקולוגי', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (5, N'בדיקה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (6, N'בדיקה חוזרת', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (7, N'בירור', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (8, N'במיון הכללי', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (9, N'במיון כללי', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (10, N'הלך על דעת עצמו', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (11, N'המתנה למעבדה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (12, N'העברה לחדר לידה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (13, N'העברה לצינתורים', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (14, N'השראת לידה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (15, N'חדר לידה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (16, N'חדר ניתוח', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (17, N'חזרה לאשפוז', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (18, N'חזרה למחלקת האשפוז', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (19, N'חזרה למיון', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (20, N'ממתינה לאולטרסאונד', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (21, N'ניטור', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (22, N'נפטר במיון', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (23, N'נפטר/ה', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (24, N'עבר למיון אחר', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (25, N'עזבו על דעת עצמם', 1092)
GO
insert [dbo].[TableAnswers] ([Answer_Code], [Answer_Text], [Table_Code]) VALUES (2, N'שחרור', 1092)
GO
insert [dbo].[Users] ([usernamenotitle], [Code]) VALUES (N'ניסים אהרון', N'1')
GO
insert [dbo].[Users] ([usernamenotitle], [Code]) VALUES (N'שירה גרינשטיין', N'2')
GO
insert [dbo].[Users] ([usernamenotitle], [Code]) VALUES (N'ניצן חלבי', N'3')
GO
insert [dbo].[Users] ([usernamenotitle], [Code]) VALUES (N'עמית גזית', N'4')
GO
insert into [dbo].[faker_wing_Doctor]  values('a',1),('a',5),('b1',2),('b1',3),('b2',4),('b2',6),('b3',7),('b3',8)
go
insert into [dbo].[Users] ([usernamenotitle],[Code]) VALUES (N'אחמד מלמוד',5),(N'מוחמד דבור',6),(N'אילנית כהן',7),(N'נגב ניצן',8)
GO
/****** Object:  StoredProcedure [dbo].[faker_ResponsibleDoctor]    Script Date: 23/06/2022 10:09:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[faker_ResponsibleDoctor](@medical_record nvarchar(50))
	AS
	Begin
	if exists (select * from [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] rd where rd.medical_record=@medical_record and rd.delete_date is null)
		begin
			update [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] set  delete_date= GETDATE() where medical_record=@medical_record and delete_date is null;
			insert into [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] values(
			(select top 1 fwd.code from (select top 1 id,DepartmentWing from [chameleon_db].[dbo].[Emergency_visits] where id=@medical_record order by DepartmentAdmission desc) ev
			join [sbwnd81c_chameleon].[dbo].[faker_wing_Doctor] as fwd on fwd.DepartmentWing=ev.DepartmentWing
			left join [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] as rd on rd.doctor = fwd.code
			group by  fwd.code
			order by count(*) asc),@medical_record,null);
		end
	else
		begin
			insert into [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] values(
			(select top 1 fwd.code from (select top 1 id,DepartmentWing from [chameleon_db].[dbo].[Emergency_visits] where id=@medical_record order by DepartmentAdmission desc) ev
			join [sbwnd81c_chameleon].[dbo].[faker_wing_Doctor] as fwd on fwd.DepartmentWing=ev.DepartmentWing
			left join [sbwnd81c_chameleon].[dbo].[ResponsibleDoctor] as rd on rd.doctor = fwd.code
			group by  fwd.code
			order by count(*) asc),@medical_record,null);
		end
	end
GO
/****** Object:  StoredProcedure [dbo].[faker_RoomPlacmentPatient_admission]    Script Date: 23/06/2022 10:09:29 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[faker_RoomPlacmentPatient_admission](@medical_record int,@room_num nvarchar)
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
	create procedure [dbo].[faker_RoomPlacmentPatient_dismission](@medical_record nvarchar(50))
	AS
	Begin
	update [sbwnd81c_chameleon].[dbo].[RoomPlacmentPatient] set end_date = GETUTCDATE() where [Medical_Record]=@medical_record and end_date is null;
	end
	;
GO
/****** Object:  StoredProcedure [dbo].[faker_decision]    Script Date: 04/07/2022 21:16:23 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[faker_decision](@medical_record nvarchar(50))
	AS
	Begin
	declare @decision as int;
	declare @unit_hosp as int;
	if exists (select * from [sbwnd81c_chameleon].[dbo].[AdmissionTreatmentDecision] atd where atd.medical_record=@medical_record and atd.delete_date is null)
		begin
			update [sbwnd81c_chameleon].[dbo].[AdmissionTreatmentDecision] set delete_date= getdate() where medical_record=@medical_record and delete_date is null;
		end
	if (select top 1  count(*)*100/ sum(count(*)) over() as ratio from [sbwnd81c_chameleon].[dbo].[AdmissionTreatmentDecision] a
		left join [dbo].[faker_answer_HospUnit] f on a.Hosp_Unit=f.name and a.Delete_Date is null
		group by (case when f.name is null then 0 else 1 end )
		order by (case when f.name is null then 0 else 1 end ) ) <30
		begin
		-- insert release
		insert into [sbwnd81c_chameleon].[dbo].[AdmissionTreatmentDecision]
		values(2,null,null,@medical_record);
		end
	else
		begin
		-- insert hosp
		select top 1 @decision=hu.decision ,@unit_hosp=hu.name
		from [sbwnd81c_chameleon].[dbo].faker_answer_HospUnit hu
		where hu.decision=1 order by newid();

		insert into [sbwnd81c_chameleon].[dbo].[AdmissionTreatmentDecision]
		values( @decision,@unit_hosp,null,@medical_record);
		end
	end
GO
USE [master]
GO
alter database [sbwnd81c_chameleon] SET READ_WRITE
GO
