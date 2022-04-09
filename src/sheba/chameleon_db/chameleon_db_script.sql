USE [master]
GO
/****** Object:  Database [chameleon_db]    Script Date: 09/04/2022 19:57:57 ******/
CREATE DATABASE [chameleon_db]
 CONTAINMENT = NONE
 ON  PRIMARY
( NAME = N'chameleon_db', FILENAME = N'/var/opt/mssql/data/chameleon_db.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON
( NAME = N'chameleon_db_log', FILENAME = N'/var/opt/mssql/data/chameleon_db_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 COLLATE Hebrew_CI_AS
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
/****** Object:  Table [dbo].[chameleon_main]    Script Date: 09/04/2022 19:57:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[chameleon_main](
	[id_num] [varchar](250) NULL,
	[patient_id] [bigint] NULL,
	[patient_name] [varchar](200) NULL,
	[unit] [int] NULL,
	[unit_wing] [int] NULL,
	[main_cause] [varchar](250) NULL,
	[esi] [int] NULL,
	[bed_num] [int] NULL,
	[warnings] [varchar](150) NULL,
	[gender] [varchar](2) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[measurements]    Script Date: 09/04/2022 19:57:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[measurements](
	[id_num] [varchar](250) NOT NULL,
	[Parameter_Date] [datetime] NULL,
	[Parameter_Id] [int] NOT NULL,
	[Parameter_Name] [varchar](200) NULL,
	[Result] [float] NULL,
	[Min_Value] [float] NULL,
	[Max_Value] [float] NULL,
	[Warnings] [varchar](50) NULL,
PRIMARY KEY CLUSTERED
(
	[id_num] ASC,
	[Parameter_Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender]) VALUES (N'ASDFGR53GF', 123456789, N'אבי נוסבאום', 5, 4, N'כאבי בטן', 1, 1, NULL, N'M')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender]) VALUES (N'GJKB45BV3H', 637284537, N'נפטלי בנט', 5, 4, N'כאבי ראש', 1, 2, NULL, N'M')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender]) VALUES (N'GC34B5B4LD', 494651134, N'אלברט אינשטיין', 5, 3, N'הקאות', 2, 1, NULL, N'M')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender]) VALUES (N'PEND8SB4H6', 187356296, N'משה דיין', 5, 2, N'פציעה בעין', 3, 1, NULL, N'M')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'ASDFGR53GF', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 11, N'טמפ', 36.6, 35.9, 36.8, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'ASDFGR53GF', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 12, N'דופק', 75, 60, 100, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'ASDFGR53GF', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 101, N'לחץ סיסטולי', 160, 90, 140, N'1')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'ASDFGR53GF', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 102, N'לחץ דיאסטולי', 70, 60, 90, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'f4A645viP0D2H6h782Q', CAST(N'2022-04-09T00:00:00.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 88.43, 66.2, 103.62, N'Number financial work keep management.')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'F7G872Dll8B2h3G186O', CAST(N'2022-04-09T00:00:00.000' AS DateTime), 11, N'דופק', 17.1, 76.79, 119.62, N'Next cell check goal region mouth.')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'GC34B5B4LD', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 11, N'טמפ', 38.6, 35.9, 36.8, N'1')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'GC34B5B4LD', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 12, N'דופק', 75, 60, 100, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'GC34B5B4LD', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 101, N'לחץ סיסטולי', 120, 90, 140, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'GC34B5B4LD', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 102, N'לחץ דיאסטולי', 80, 60, 90, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'GJKB45BV3H', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 11, N'טמפ', 36.5, 35.9, 36.8, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'GJKB45BV3H', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 12, N'דופק', 80, 60, 100, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'GJKB45BV3H', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 101, N'לחץ סיסטולי', 100, 90, 140, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'GJKB45BV3H', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 102, N'לחץ דיאסטולי', 120, 60, 90, N'1')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'PEND8SB4H6', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 11, N'טמפ', 36.5, 35.9, 36.8, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'PEND8SB4H6', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 12, N'דופק', 120, 60, 100, N'1')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'PEND8SB4H6', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 101, N'לחץ סיסטולי', 130, 90, 140, N'0')
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings]) VALUES (N'PEND8SB4H6', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 102, N'לחץ דיאסטולי', 65, 60, 90, N'0')
GO
USE [master]
GO
ALTER DATABASE [chameleon_db] SET  READ_WRITE
GO
