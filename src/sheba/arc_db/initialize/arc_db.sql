USE [master]
GO
/****** Object:  Database [dwh]    Script Date: 13/04/2022 0:44:08 ******/
create DATABASE [dwh]
    CONTAINMENT = NONE
    ON PRIMARY
    ( NAME = N'dwh', FILENAME = N'/var/opt/mssql/data/dwh.mdf' , SIZE = 8192 KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536 KB )
    LOG ON
    ( NAME = N'dwh_log', FILENAME = N'/var/opt/mssql/data/dwh_log.ldf' , SIZE = 8192 KB , MAXSIZE = 2048 GB , FILEGROWTH = 65536 KB )
    COLLATE Hebrew_CI_AS
GO
alter database [dwh] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
    begin
        EXEC [dwh].[dw].[sp_fulltext_database] @action = 'enable'
    end
GO
ALTER DATABASE [dwh] SET ANSI_NULL_DEFAULT OFF
GO
alter database [dwh] SET ANSI_NULLS OFF
GO
alter database [dwh] SET ANSI_PADDING OFF
GO
alter database [dwh] SET ANSI_WARNINGS OFF
GO
alter database [dwh] SET ARITHABORT OFF
GO
alter database [dwh] SET AUTO_CLOSE OFF
GO
alter database [dwh] SET AUTO_SHRINK OFF
GO
alter database [dwh] SET AUTO_UPDATE_STATISTICS ON
GO
alter database [dwh] SET CURSOR_CLOSE_ON_COMMIT OFF
GO
alter database [dwh] SET CURSOR_DEFAULT GLOBAL
GO
alter database [dwh] SET CONCAT_NULL_YIELDS_NULL OFF
GO
alter database [dwh] SET NUMERIC_ROUNDABORT OFF
GO
alter database [dwh] SET QUOTED_IDENTIFIER OFF
GO
alter database [dwh] SET RECURSIVE_TRIGGERS OFF
GO
alter database [dwh] SET DISABLE_BROKER
GO
alter database [dwh] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO
alter database [dwh] SET DATE_CORRELATION_OPTIMIZATION OFF
GO
alter database [dwh] SET TRUSTWORTHY OFF
GO
alter database [dwh] SET ALLOW_SNAPSHOT_ISOLATION OFF
GO
alter database [dwh] SET PARAMETERIZATION SIMPLE
GO
alter database [dwh] SET READ_COMMITTED_SNAPSHOT OFF
GO
alter database [dwh] SET HONOR_BROKER_PRIORITY OFF
GO
alter database [dwh] SET RECOVERY FULL
GO
alter database [dwh] SET MULTI_USER
GO
alter database [dwh] SET PAGE_VERIFY CHECKSUM
GO
alter database [dwh] SET DB_CHAINING OFF
GO
alter database [dwh] SET FILESTREAM ( NON_TRANSACTED_ACCESS = OFF )
GO
alter database [dwh] SET TARGET_RECOVERY_TIME = 60 SECONDS
GO
alter database [dwh] SET DELAYED_DURABILITY = DISABLED
GO
alter database [dwh] SET ACCELERATED_DATABASE_RECOVERY = OFF
GO
EXEC sys.sp_db_vardecimal_storage_format N'dwh', N'ON'
GO
alter database [dwh] SET QUERY_STORE = OFF
GO
USE [dwh]
GO
/****** Object:  Table [ris].[patients]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [ris].[patients]
(
    [PATIENT_ID] [bigint] IDENTITY (1,1) NOT NULL,
    [first_name] [varchar](200)       NULL,
    [last_name]  [varchar](200)       NULL,
    [gender]     [varchar](2)         NULL,
    [birth_date] [datetime]           NULL,
) ON [PRIMARY]
GO
/****** Object:  Table [dw].[Emergency_visits]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dw].[Emergency_visits]
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
/****** Object:  Table [dw].[measurements]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dw].[measurements]
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
create TABLE [dw].[Imaging]
(
    [sps_key]              [int] IDENTITY (1,1) NOT NULL,
    [id]                   [int]                NOT NULL,
    [OrderDate]            [datetime]           NOT NULL,
    [OrderedProcedureType] [varchar](100)       NOT NULL,
    [ProcedureStatus]      [varchar](100)       NOT NULL,
    [Interpretation]       [varchar](300)       NULL,
)
GO
create TABLE [dw].[lab_results]
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
create TABLE [dw].[medical_free_text]
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
create TABLE [dw].[referrals]
(
    [ReferralCode]  [int] IDENTITY (1,1) NOT NULL,
    [id]            [int]                NOT NULL,
    [DoctorName]    [varchar](50)        NULL,
    [OrderDate]     [datetime]           NULL,
    [CompletedDate] [datetime]           NULL,
) ON [PRIMARY]
GO

alter database [dwh] SET READ_WRITE
USE [master]
GO
CREATE LOGIN [arc_cham_login] WITH PASSWORD='Password123', DEFAULT_DATABASE=[master], DEFAULT_LANGUAGE=[us_english], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF
GO

ALTER SERVER ROLE [sysadmin] ADD MEMBER [arc_cham_login]
GO

ALTER SERVER ROLE [serveradmin] ADD MEMBER [arc_cham_login]
GO
USE [dwh]
GO
CREATE USER [arc_cham_login] FOR LOGIN [arc_cham_login]
GO
USE [dwh]
GO
ALTER ROLE [db_accessadmin] ADD MEMBER [arc_cham_login]
GO
USE [dwh]
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