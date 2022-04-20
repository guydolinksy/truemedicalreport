USE [master]
GO
/****** Object:  Database [chameleon_db]    Script Date: 13/04/2022 0:44:08 ******/
create DATABASE [chameleon_db]
 CONTAINMENT = NONE
 ON  PRIMARY
( NAME = N'chameleon_db', FILENAME = N'/var/opt/mssql/data/chameleon_db.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON
( NAME = N'chameleon_db_log', FILENAME = N'/var/opt/mssql/data/chameleon_db_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
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
alter database [chameleon_db] SET CURSOR_DEFAULT  GLOBAL
GO
alter database [chameleon_db] SET CONCAT_NULL_YIELDS_NULL OFF
GO
alter database [chameleon_db] SET NUMERIC_ROUNDABORT OFF
GO
alter database [chameleon_db] SET QUOTED_IDENTIFIER OFF
GO
alter database [chameleon_db] SET RECURSIVE_TRIGGERS OFF
GO
alter database [chameleon_db] SET  DISABLE_BROKER
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
alter database [chameleon_db] SET  MULTI_USER
GO
alter database [chameleon_db] SET PAGE_VERIFY CHECKSUM
GO
alter database [chameleon_db] SET DB_CHAINING OFF
GO
alter database [chameleon_db] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF )
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
/****** Object:  Table [dbo].[chameleon_main]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[chameleon_main](
	[id_num] [int] IDENTITY(1,1) NOT NULL,
	[patient_id] [varchar](250) NULL,
	[patient_name] [varchar](200) NULL,
	[unit] [int] NULL,
	[unit_wing] [varchar](200) NULL,
	[main_cause] [varchar](250) NULL,
	[esi] [int] NULL,
	[bed_num] [int] NULL,
	[warnings] [varchar](150) NULL,
	[gender] [varchar](2) NULL,
	[age] [varchar](7) NULL,
	[birthdate] [datetime] NULL,
	[stage] [varchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[measurements]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create TABLE [dbo].[measurements](
	[pk_measurement_id] [int] IDENTITY(1,1) NOT NULL,
	[id_num] [varchar](250) NOT NULL,
	[Parameter_Date] [datetime] NULL,
	[Parameter_Id] [int] NOT NULL,
	[Parameter_Name] [varchar](200) NULL,
	[Result] [float] NULL,
	[Min_Value] [float] NULL,
	[Max_Value] [float] NULL,
	[Warnings] [varchar](50) NULL,
 CONSTRAINT [PK_M] PRIMARY KEY CLUSTERED
(
	[pk_measurement_id] ASC
)with (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
USE [master]
GO
alter database [chameleon_db] SET  READ_WRITE
GO
