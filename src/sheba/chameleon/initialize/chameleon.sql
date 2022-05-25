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
    [id]                  [int] IDENTITY (1,1) NOT NULL,
    [DepartmentName]      [varchar](200)       NULL,
    [DepartmentWing]      [varchar](200)       NULL,
    [DepartmentAdmission] [datetime]           NULL,
    [MainCause]           [varchar](200)       NULL,
    [esi]                 [int]                NULL,
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
CREATE TABLE [dbo].[referrals](
	[ReferralCode] [int] IDENTITY (1,1) NOT NULL,
	[id] [int] NOT NULL,
	[DoctorName] [varchar](50) NULL,
	[OrderDate] [datetime] NULL,
	[CompletedDate] [datetime] NULL,
) ON [PRIMARY]
GO
alter database [chameleon_db] SET READ_WRITE
USE [master]
GO