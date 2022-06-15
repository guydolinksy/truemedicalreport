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
USE [master]
GO
ALTER DATABASE [sbwnd81c_chameleon] SET READ_WRITE
GO
