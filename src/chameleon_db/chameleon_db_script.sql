USE [master]
GO
/****** Object:  Database [chameleon_db]    Script Date: 29/03/2022 17:05:32 ******/
CREATE DATABASE [chameleon_db]
 CONTAINMENT = NONE
 ON  PRIMARY
( NAME = N'chameleon_db', FILENAME = N'/var/opt/mssql/data/chameleon_db.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON
( NAME = N'chameleon_db_log', FILENAME = N'/var/opt/mssql/data/chameleon_db_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [chameleon_db] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [chameleon_db].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [chameleon_db] SET ANSI_NULL_DEFAULT OFF
GO
ALTER DATABASE [chameleon_db] SET ANSI_NULLS OFF
GO
ALTER DATABASE [chameleon_db] SET ANSI_PADDING OFF
GO
ALTER DATABASE [chameleon_db] SET ANSI_WARNINGS OFF
GO
ALTER DATABASE [chameleon_db] SET ARITHABORT OFF
GO
ALTER DATABASE [chameleon_db] SET AUTO_CLOSE OFF
GO
ALTER DATABASE [chameleon_db] SET AUTO_SHRINK OFF
GO
ALTER DATABASE [chameleon_db] SET AUTO_UPDATE_STATISTICS ON
GO
ALTER DATABASE [chameleon_db] SET CURSOR_CLOSE_ON_COMMIT OFF
GO
ALTER DATABASE [chameleon_db] SET CURSOR_DEFAULT  GLOBAL
GO
ALTER DATABASE [chameleon_db] SET CONCAT_NULL_YIELDS_NULL OFF
GO
ALTER DATABASE [chameleon_db] SET NUMERIC_ROUNDABORT OFF
GO
ALTER DATABASE [chameleon_db] SET QUOTED_IDENTIFIER OFF
GO
ALTER DATABASE [chameleon_db] SET RECURSIVE_TRIGGERS OFF
GO
ALTER DATABASE [chameleon_db] SET  DISABLE_BROKER
GO
ALTER DATABASE [chameleon_db] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO
ALTER DATABASE [chameleon_db] SET DATE_CORRELATION_OPTIMIZATION OFF
GO
ALTER DATABASE [chameleon_db] SET TRUSTWORTHY OFF
GO
ALTER DATABASE [chameleon_db] SET ALLOW_SNAPSHOT_ISOLATION OFF
GO
ALTER DATABASE [chameleon_db] SET PARAMETERIZATION SIMPLE
GO
ALTER DATABASE [chameleon_db] SET READ_COMMITTED_SNAPSHOT OFF
GO
ALTER DATABASE [chameleon_db] SET HONOR_BROKER_PRIORITY OFF
GO
ALTER DATABASE [chameleon_db] SET RECOVERY FULL
GO
ALTER DATABASE [chameleon_db] SET  MULTI_USER
GO
ALTER DATABASE [chameleon_db] SET PAGE_VERIFY CHECKSUM
GO
ALTER DATABASE [chameleon_db] SET DB_CHAINING OFF
GO
ALTER DATABASE [chameleon_db] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF )
GO
ALTER DATABASE [chameleon_db] SET TARGET_RECOVERY_TIME = 60 SECONDS
GO
ALTER DATABASE [chameleon_db] SET DELAYED_DURABILITY = DISABLED
GO
ALTER DATABASE [chameleon_db] SET ACCELERATED_DATABASE_RECOVERY = OFF
GO
EXEC sys.sp_db_vardecimal_storage_format N'chameleon_db', N'ON'
GO
ALTER DATABASE [chameleon_db] SET QUERY_STORE = OFF
GO
USE [chameleon_db]
GO
/****** Object:  Table [dbo].[chameleon_main]    Script Date: 29/03/2022 17:05:32 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[chameleon_main](
	[id_num] [bigint] NULL,
	[patient] [bigint] NULL,
	[name] [varchar](100) NULL,
	[unit] [int] NULL,
	[unit_wing] [int] NULL,
	[main_cause] [varchar](150) NULL,
	[esi] [int] NULL,
	[bed_num] [int] NULL,
	[warnings] [varchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[measurements]    Script Date: 29/03/2022 17:05:33 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[measurements](
	[id_num] [bigint] NULL,
	[Parameter_Date] [date] NULL,
	[Parameter_Name] [varchar](100) NULL,
	[Result] [varchar](150) NULL,
	[warnings] [varchar](50) NULL
) ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [chameleon_db] SET  READ_WRITE
GO
COMMIT
GO