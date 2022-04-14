USE [master]
GO
/****** Object:  Database [chameleon_db]    Script Date: 13/04/2022 0:44:08 ******/
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
/****** Object:  Table [dbo].[chameleon_main]    Script Date: 13/04/2022 0:44:08 ******/
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
	[gender] [varchar](2) NULL,
	[stage] [varchar](150) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[measurements]    Script Date: 13/04/2022 0:44:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[measurements](
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
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'ASDFGR53GF', 123456789, N'אבי נוסבאום', 5, 4, N'כאבי בטן', 1, 1, NULL, N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'GJKB45BV3H', 637284537, N'נפטלי בנט', 5, 4, N'כאבי ראש', 1, 2, NULL, N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'GC34B5B4LD', 494651134, N'אלברט אינשטיין', 5, 3, N'הקאות', 2, 1, NULL, N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'PEND8SB4H6', 187356296, N'משה דיין', 5, 2, N'פציעה בעין', 3, 1, NULL, N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'n9h079rOJ4S8v7A737x', 268508599, N'Dustin Bryant', 2, 4, N'כאבי ראש', 2, 1, N'Democratic help.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'B1o453ldh1f1J3U438V', 923698996, N'Robert Powers', 1, 1, N'קשיי נשימה', 3, 0, N'Hard prove her.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'U7s198QAQ2M1S7H577H', 28517419, N'Keith Gould', 3, 2, N'כאבי בטן', 1, 5, N'Center role pattern.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'G0g447npX3T0P3B514m', 760186618, N'Mary Campos', 1, 2, N'קשיי נשימה', 4, 1, N'News matter be.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'p4Y592cQi1V1m6B382p', 701731386, N'Pamela Rodriguez', 1, 3, N'כאבים בחזה', 3, 6, N'That claim meeting building.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'k0i172WwI4D7A7n921o', 63634520, N'Charles Carrillo', 1, 4, N'כאבים בחזה', 1, 8, N'Themselves image anyone.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'u5h507NnO0X1y0T740X', 963176788, N'Dale Lee', 3, 3, N'הקאות', 2, 0, N'Can build.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'p8x446rLJ9I4b9W199I', 699800721, N'Benjamin Smith', 1, 4, N'הקאות', 1, 1, N'Decision same.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'B2u519uHR2o9z1S371i', 17690019, N'Michael Lane', 3, 2, N'כאבי בטן', 2, 3, N'Soon call them.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'u4q631EAR5D4S3k386V', 694522776, N'Keith Meyer', 1, 1, N'סחרחורות', 4, 3, N'Point probably.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'F5Q924VhF6K7B7b752y', 311051467, N'Bruce Lozano', 2, 4, N'כאבי ראש', 3, 5, N'Miss share.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'V4f744Avi1X7G0W592N', 816084545, N'Dustin Stevens', 2, 2, N'כאבים בחזה', 2, 3, N'Firm tonight.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'F8X111slx9m6p9w429u', 60890566, N'Katherine Miller', 2, 2, N'פגיעה בראש', 4, 0, N'Easy past.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'K7y751egy8k9m4D883r', 16288770, N'Eric Lynch', 2, 2, N'חתך ביד', 1, 0, N'Defense memory.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'y7R668dWb1Q3Y6n879I', 792886501, N'Brittany Rodriguez', 2, 3, N'פציעה בעין', 1, 2, N'Lot anyone main.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'u3R761Zcb5E7h1I498P', 388175846, N'Elizabeth Cruz', 2, 4, N'קשיי נשימה', 3, 8, N'Red serve move.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'G8j570cjA7B3d3y521J', 852381529, N'Mark King', 2, 1, N'כאבי ראש', 3, 0, N'Senior have.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N's2q802LmG1u6N9U485v', 305679167, N'Amanda Martin', 1, 2, N'כאבי ראש', 3, 4, N'Nearly.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'n5W701ubi4k8y7V186I', 672861438, N'Melissa Smith', 3, 4, N'סחרחורות', 2, 1, N'Record these contain.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'q5K435RzU4N0r1q348x', 571286413, N'Kimberly Perez', 2, 1, N'חתך ביד', 4, 4, N'Box today cost.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'X5k515WeD3K0h0x577b', 885444566, N'Elijah Brown', 3, 2, N'כאבי בטן', 2, 4, N'Ten whether.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'x1Q512dbw0l8q8v997M', 181804703, N'Jennifer Hall', 1, 3, N'פציעה בעין', 4, 2, N'Decade step walk.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'g1C375vkU2y1h9m465x', 524884687, N'Jennifer Brown', 2, 4, N'כאבי ראש', 4, 7, N'Third determine.', N'M', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'b5Z866fQl1r0m5Q830w', 881854670, N'Madison Morse', 3, 1, N'כאבי ראש', 3, 2, N'Impact administration large.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'a0y353yjo4X1o9e896G', 250329947, N'Jamie Flores', 2, 1, N'סחרחורות', 3, 5, N'Day local.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'd6e148VkB9O6K6Z112A', 227493299, N'Helen Tucker', 2, 3, N'הקאות', 1, 7, N'Painting leg.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'v3i537rIt2b4B9H458g', 552137216, N'Chad Moore', 2, 3, N'קשיי נשימה', 1, 6, N'Which avoid employee.', N'F', N'אושפז')
GO
INSERT [dbo].[chameleon_main] ([id_num], [patient_id], [patient_name], [unit], [unit_wing], [main_cause], [esi], [bed_num], [warnings], [gender], [stage]) VALUES (N'B7x537PLy9Q1C1x871o', 871144155, N'George Franklin', 1, 1, N'פגיעה בראש', 3, 3, N'Behavior her.', N'F', N'אושפז')
GO
SET IDENTITY_INSERT [dbo].[measurements] ON
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'a0y353yjo4X1o9e896G', CAST(N'2022-04-12T06:11:36.000' AS DateTime), 11, N'טמפ', 62.21, 32.27, 80.18, N'World join.', 1)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'a0y353yjo4X1o9e896G', CAST(N'2022-04-12T06:11:36.000' AS DateTime), 12, N'דופק', 81.3, 69.24, 113.14, N'Him father administration.', 2)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'a0y353yjo4X1o9e896G', CAST(N'2022-04-12T06:11:36.000' AS DateTime), 101, N'לחץ דם סיסטולי', 38.89, 55.39, 104.89, N'Debate goal.', 3)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'a0y353yjo4X1o9e896G', CAST(N'2022-04-12T06:11:36.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 88, 68.27, 83.5, N'Seem cultural win.', 4)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'ASDFGR53GF', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 11, N'טמפ', 36.6, 35.9, 36.8, N'0', 5)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'ASDFGR53GF', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 12, N'דופק', 75, 60, 100, N'0', 6)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'ASDFGR53GF', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 101, N'לחץ סיסטולי', 160, 90, 140, N'1', 7)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'ASDFGR53GF', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 102, N'לחץ דיאסטולי', 70, 60, 90, N'0', 8)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B1o453ldh1f1J3U438V', CAST(N'2022-04-10T16:37:34.000' AS DateTime), 11, N'טמפ', 139.43, 54.21, 129.81, N'Eight military arm.', 9)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B1o453ldh1f1J3U438V', CAST(N'2022-04-10T16:37:34.000' AS DateTime), 12, N'דופק', 57.24, 39.31, 134.93, N'Bank political over.', 10)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B1o453ldh1f1J3U438V', CAST(N'2022-04-10T16:37:34.000' AS DateTime), 101, N'לחץ דם סיסטולי', 47.59, 49.43, 118.6, N'Thought federal.', 11)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B1o453ldh1f1J3U438V', CAST(N'2022-04-10T16:37:34.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 31.88, 41.21, 117.31, N'Goal again conference between.', 12)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B2u519uHR2o9z1S371i', CAST(N'2022-04-12T06:15:01.000' AS DateTime), 11, N'טמפ', 27.12, 57.88, 137.53, N'Size game.', 13)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B2u519uHR2o9z1S371i', CAST(N'2022-04-12T06:15:01.000' AS DateTime), 12, N'דופק', 76.51, 31.45, 127.66, N'Choose capital.', 14)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B2u519uHR2o9z1S371i', CAST(N'2022-04-12T06:15:01.000' AS DateTime), 101, N'לחץ דם סיסטולי', 42.61, 55.9, 98.65, N'Long especially along.', 15)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B2u519uHR2o9z1S371i', CAST(N'2022-04-12T06:15:01.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 159.6, 67.8, 128.1, N'Bill imagine.', 16)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'b5Z866fQl1r0m5Q830w', CAST(N'2022-04-12T06:10:03.000' AS DateTime), 11, N'טמפ', 116.21, 33.96, 139.9, N'Purpose set certainly.', 17)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'b5Z866fQl1r0m5Q830w', CAST(N'2022-04-12T06:10:03.000' AS DateTime), 12, N'דופק', 34, 64.47, 123.85, N'Opportunity yes manage.', 18)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'b5Z866fQl1r0m5Q830w', CAST(N'2022-04-12T06:10:03.000' AS DateTime), 101, N'לחץ דם סיסטולי', 118.5, 44.37, 120.8, N'Reflect would report because.', 19)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'b5Z866fQl1r0m5Q830w', CAST(N'2022-04-12T06:10:03.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 150.29, 76.39, 96.53, N'Deal quite.', 20)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B7x537PLy9Q1C1x871o', CAST(N'2022-04-12T06:18:54.000' AS DateTime), 11, N'טמפ', 12.14, 77.93, 139.54, N'All particularly before.', 21)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B7x537PLy9Q1C1x871o', CAST(N'2022-04-12T06:18:54.000' AS DateTime), 12, N'דופק', 88.48, 67.39, 149.18, N'When blood.', 22)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B7x537PLy9Q1C1x871o', CAST(N'2022-04-12T06:18:54.000' AS DateTime), 101, N'לחץ דם סיסטולי', 137.93, 65.82, 125.91, N'Cup.', 23)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'B7x537PLy9Q1C1x871o', CAST(N'2022-04-12T06:18:54.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 23.1, 41.3, 86.88, N'Behind standard spend.', 24)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'd6e148VkB9O6K6Z112A', CAST(N'2022-04-12T06:11:48.000' AS DateTime), 11, N'טמפ', 111.82, 58.78, 148.76, N'Measure station everything color.', 25)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'd6e148VkB9O6K6Z112A', CAST(N'2022-04-12T06:11:48.000' AS DateTime), 12, N'דופק', 148.89, 55.77, 110.4, N'Resource mouth choice.', 26)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'd6e148VkB9O6K6Z112A', CAST(N'2022-04-12T06:11:48.000' AS DateTime), 101, N'לחץ דם סיסטולי', 11.17, 38.21, 112.6, N'War strong.', 27)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'd6e148VkB9O6K6Z112A', CAST(N'2022-04-12T06:11:48.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 57.29, 38.92, 144.47, N'Hope safe.', 28)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'f4A645viP0D2H6h782Q', CAST(N'2022-04-09T00:00:00.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 88.43, 66.2, 103.62, N'Number financial work keep management.', 29)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F7G872Dll8B2h3G186O', CAST(N'2022-04-09T00:00:00.000' AS DateTime), 11, N'דופק', 17.1, 76.79, 119.62, N'Next cell check goal region mouth.', 30)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F8X111slx9m6p9w429u', CAST(N'2022-04-10T16:51:17.000' AS DateTime), 11, N'טמפ', 147.18, 58, 115.28, N'Friend scene author anyone.', 31)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F8X111slx9m6p9w429u', CAST(N'2022-04-10T16:51:17.000' AS DateTime), 12, N'דופק', 114.57, 50.68, 97.93, N'Ability claim.', 32)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F8X111slx9m6p9w429u', CAST(N'2022-04-10T16:51:17.000' AS DateTime), 101, N'לחץ דם סיסטולי', 109.73, 37.26, 92.42, N'Believe father happen.', 33)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F8X111slx9m6p9w429u', CAST(N'2022-04-10T16:51:17.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 142.49, 35.71, 81.72, N'Account hope write.', 34)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G0g447npX3T0P3B514m', CAST(N'2022-04-10T16:47:59.000' AS DateTime), 11, N'טמפ', 94.58, 41.31, 127.62, N'Least job.', 35)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G0g447npX3T0P3B514m', CAST(N'2022-04-10T16:47:59.000' AS DateTime), 12, N'דופק', 130.31, 69.34, 108.98, N'Matter window.', 36)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G0g447npX3T0P3B514m', CAST(N'2022-04-10T16:47:59.000' AS DateTime), 101, N'לחץ דם סיסטולי', 46.51, 44.13, 120.28, N'Product process.', 37)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G0g447npX3T0P3B514m', CAST(N'2022-04-10T16:47:59.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 120.49, 43.2, 89.59, N'Police.', 38)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'g1C375vkU2y1h9m465x', CAST(N'2022-04-12T06:08:24.000' AS DateTime), 11, N'טמפ', 26.12, 54.93, 81.23, N'Tax indicate.', 39)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'g1C375vkU2y1h9m465x', CAST(N'2022-04-12T06:08:24.000' AS DateTime), 12, N'דופק', 118.28, 34.99, 117.65, N'Project civil whatever.', 40)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'g1C375vkU2y1h9m465x', CAST(N'2022-04-12T06:08:24.000' AS DateTime), 101, N'לחץ דם סיסטולי', 65.19, 55.53, 116.93, N'Open.', 41)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'g1C375vkU2y1h9m465x', CAST(N'2022-04-12T06:08:24.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 85.79, 54.85, 105.93, N'Instead box.', 42)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G8j570cjA7B3d3y521J', CAST(N'2022-04-12T05:45:45.000' AS DateTime), 11, N'טמפ', 99.8, 46.48, 111.49, N'Specific we.', 43)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G8j570cjA7B3d3y521J', CAST(N'2022-04-12T05:45:45.000' AS DateTime), 12, N'דופק', 43.76, 61.5, 104.32, N'Nor among final stage.', 44)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G8j570cjA7B3d3y521J', CAST(N'2022-04-12T05:45:45.000' AS DateTime), 101, N'לחץ דם סיסטולי', 152.2, 56.67, 149.28, N'Article check son.', 45)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G8j570cjA7B3d3y521J', CAST(N'2022-04-12T05:45:45.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 80.67, 65.55, 91.32, N'Say choice.', 46)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'GC34B5B4LD', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 11, N'טמפ', 38.6, 35.9, 36.8, N'1', 47)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'GC34B5B4LD', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 12, N'דופק', 75, 60, 100, N'0', 48)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'GC34B5B4LD', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 101, N'לחץ סיסטולי', 120, 90, 140, N'0', 49)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'GC34B5B4LD', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 102, N'לחץ דיאסטולי', 80, 60, 90, N'0', 50)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'GJKB45BV3H', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 11, N'טמפ', 36.5, 35.9, 36.8, N'0', 51)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'GJKB45BV3H', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 12, N'דופק', 80, 60, 100, N'0', 52)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'GJKB45BV3H', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 101, N'לחץ סיסטולי', 100, 90, 140, N'0', 53)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'GJKB45BV3H', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 102, N'לחץ דיאסטולי', 120, 60, 90, N'1', 54)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'k0i172WwI4D7A7n921o', CAST(N'2022-04-10T16:49:16.000' AS DateTime), 11, N'טמפ', 102.19, 38.87, 141.51, N'Newspaper.', 55)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'k0i172WwI4D7A7n921o', CAST(N'2022-04-10T16:49:16.000' AS DateTime), 12, N'דופק', 133.8, 67.7, 102.45, N'School heart project.', 56)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'k0i172WwI4D7A7n921o', CAST(N'2022-04-10T16:49:16.000' AS DateTime), 101, N'לחץ דם סיסטולי', 99.4, 33.37, 118.41, N'Group direction drop.', 57)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'k0i172WwI4D7A7n921o', CAST(N'2022-04-10T16:49:16.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 124.43, 63.5, 86.77, N'Democratic car compare.', 58)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'K7y751egy8k9m4D883r', CAST(N'2022-04-12T05:39:23.000' AS DateTime), 11, N'טמפ', 128.76, 47.1, 86.55, N'Reduce member.', 59)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'K7y751egy8k9m4D883r', CAST(N'2022-04-12T05:39:23.000' AS DateTime), 12, N'דופק', 86.48, 65.7, 112.7, N'Be serious.', 60)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'K7y751egy8k9m4D883r', CAST(N'2022-04-12T05:39:23.000' AS DateTime), 101, N'לחץ דם סיסטולי', 90.86, 51.27, 90.93, N'Fund issue.', 61)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'K7y751egy8k9m4D883r', CAST(N'2022-04-12T05:39:23.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 63.92, 60.81, 81.89, N'Fight specific.', 62)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'n5W701ubi4k8y7V186I', CAST(N'2022-04-12T05:46:25.000' AS DateTime), 11, N'טמפ', 88.83, 71.93, 116.51, N'Often.', 63)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'n5W701ubi4k8y7V186I', CAST(N'2022-04-12T05:46:25.000' AS DateTime), 12, N'דופק', 95.59, 50.53, 102.67, N'Charge.', 64)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'n5W701ubi4k8y7V186I', CAST(N'2022-04-12T05:46:25.000' AS DateTime), 101, N'לחץ דם סיסטולי', 100.24, 69.86, 127.41, N'Buy create.', 65)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'n5W701ubi4k8y7V186I', CAST(N'2022-04-12T05:46:25.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 145.1, 47.77, 116.43, N'Morning task threat.', 66)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'n9h079rOJ4S8v7A737x', CAST(N'2022-04-10T16:35:03.000' AS DateTime), 11, N'טמפ', 154.57, 39.75, 98.29, N'State.', 67)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'n9h079rOJ4S8v7A737x', CAST(N'2022-04-10T16:35:04.000' AS DateTime), 12, N'דופק', 68.55, 41.93, 136.2, N'Hope me past.', 68)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'n9h079rOJ4S8v7A737x', CAST(N'2022-04-10T16:35:07.000' AS DateTime), 101, N'לחץ דם סיסטולי', 147.5, 73.13, 85.3, N'Respond industry.', 69)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'n9h079rOJ4S8v7A737x', CAST(N'2022-04-10T16:35:23.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 15.24, 44, 133.52, N'Tax per instead.', 70)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'p4Y592cQi1V1m6B382p', CAST(N'2022-04-10T16:48:34.000' AS DateTime), 11, N'טמפ', 45.88, 37.45, 99.68, N'Her talk impact.', 71)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'p4Y592cQi1V1m6B382p', CAST(N'2022-04-10T16:48:34.000' AS DateTime), 12, N'דופק', 36.27, 43.25, 109.93, N'Decision quite compare choose.', 72)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'p4Y592cQi1V1m6B382p', CAST(N'2022-04-10T16:48:34.000' AS DateTime), 101, N'לחץ דם סיסטולי', 98.43, 36.64, 99.98, N'Brother without sign.', 73)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'p4Y592cQi1V1m6B382p', CAST(N'2022-04-10T16:48:34.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 102.48, 66.75, 130.6, N'Science reach.', 74)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'p8x446rLJ9I4b9W199I', CAST(N'2022-04-12T06:14:23.000' AS DateTime), 11, N'טמפ', 111.41, 41.33, 127.6, N'Common teach could.', 75)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'p8x446rLJ9I4b9W199I', CAST(N'2022-04-12T06:14:23.000' AS DateTime), 12, N'דופק', 12.35, 72.87, 109.17, N'Glass like rise.', 76)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'p8x446rLJ9I4b9W199I', CAST(N'2022-04-12T06:14:23.000' AS DateTime), 101, N'לחץ דם סיסטולי', 139.45, 31.45, 130.7, N'But mission price.', 77)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'p8x446rLJ9I4b9W199I', CAST(N'2022-04-12T06:14:23.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 131.17, 56.4, 104.33, N'Performance stop four.', 78)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'PEND8SB4H6', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 11, N'טמפ', 36.5, 35.9, 36.8, N'0', 79)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'PEND8SB4H6', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 12, N'דופק', 120, 60, 100, N'1', 80)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'PEND8SB4H6', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 101, N'לחץ סיסטולי', 130, 90, 140, N'0', 81)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'PEND8SB4H6', CAST(N'2022-04-06T00:00:00.000' AS DateTime), 102, N'לחץ דיאסטולי', 65, 60, 90, N'0', 82)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'q5K435RzU4N0r1q348x', CAST(N'2022-04-12T05:47:44.000' AS DateTime), 11, N'טמפ', 70.51, 47.9, 104.45, N'Inside reality.', 83)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'q5K435RzU4N0r1q348x', CAST(N'2022-04-12T05:47:44.000' AS DateTime), 12, N'דופק', 104.51, 62.43, 134.61, N'Cover miss office yes.', 84)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'q5K435RzU4N0r1q348x', CAST(N'2022-04-12T05:47:44.000' AS DateTime), 101, N'לחץ דם סיסטולי', 156.92, 66.75, 87.45, N'Effect week room.', 85)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'q5K435RzU4N0r1q348x', CAST(N'2022-04-12T05:47:44.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 59.77, 32.6, 140.4, N'Land floor young.', 86)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N's2q802LmG1u6N9U485v', CAST(N'2022-04-12T05:46:14.000' AS DateTime), 11, N'טמפ', 42.28, 52.21, 98, N'Outside by continue.', 87)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N's2q802LmG1u6N9U485v', CAST(N'2022-04-12T05:46:14.000' AS DateTime), 12, N'דופק', 81.68, 54.3, 104.8, N'Sister window including.', 88)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N's2q802LmG1u6N9U485v', CAST(N'2022-04-12T05:46:14.000' AS DateTime), 101, N'לחץ דם סיסטולי', 36.38, 30.8, 106.5, N'Throw.', 89)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N's2q802LmG1u6N9U485v', CAST(N'2022-04-12T05:46:14.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 146.1, 46.57, 109.59, N'Agree edge.', 90)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'u3R761Zcb5E7h1I498P', CAST(N'2022-04-12T05:43:40.000' AS DateTime), 11, N'טמפ', 159.24, 56.48, 84.11, N'Drive player.', 91)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'u3R761Zcb5E7h1I498P', CAST(N'2022-04-12T05:43:40.000' AS DateTime), 12, N'דופק', 141.56, 74.14, 103.81, N'Three again.', 92)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'u3R761Zcb5E7h1I498P', CAST(N'2022-04-12T05:43:40.000' AS DateTime), 101, N'לחץ דם סיסטולי', 131.16, 48.73, 90.74, N'Like director trouble.', 93)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'u3R761Zcb5E7h1I498P', CAST(N'2022-04-12T05:43:40.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 71.33, 39.83, 89.48, N'Crime buy president.', 94)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'u5h507NnO0X1y0T740X', CAST(N'2022-04-11T20:46:43.000' AS DateTime), 11, N'טמפ', 14.86, 36.92, 140.57, N'Baby time.', 95)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'u5h507NnO0X1y0T740X', CAST(N'2022-04-11T20:46:43.000' AS DateTime), 12, N'דופק', 143.6, 39.96, 142.7, N'Despite measure who.', 96)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'u5h507NnO0X1y0T740X', CAST(N'2022-04-11T20:46:43.000' AS DateTime), 101, N'לחץ דם סיסטולי', 18.88, 71.35, 82.89, N'Glass region.', 97)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'u5h507NnO0X1y0T740X', CAST(N'2022-04-11T20:46:43.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 96.8, 41.77, 119.2, N'Test major model.', 98)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'U7s198QAQ2M1S7H577H', CAST(N'2022-04-10T16:43:45.000' AS DateTime), 11, N'טמפ', 46.79, 46.15, 103.33, N'Not study defense.', 99)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'U7s198QAQ2M1S7H577H', CAST(N'2022-04-10T16:43:45.000' AS DateTime), 12, N'דופק', 96.7, 45.76, 92.29, N'Price bag then.', 100)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'U7s198QAQ2M1S7H577H', CAST(N'2022-04-10T16:43:45.000' AS DateTime), 101, N'לחץ דם סיסטולי', 85.5, 37.71, 95.96, N'Remain fall.', 101)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'U7s198QAQ2M1S7H577H', CAST(N'2022-04-10T16:43:45.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 104.9, 57.95, 140.86, N'Model generation put.', 102)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'v3i537rIt2b4B9H458g', CAST(N'2022-04-12T06:13:01.000' AS DateTime), 11, N'טמפ', 135.67, 66.59, 146.92, N'Themselves sea say.', 103)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'v3i537rIt2b4B9H458g', CAST(N'2022-04-12T06:13:01.000' AS DateTime), 12, N'דופק', 11.6, 63.2, 108.2, N'See staff.', 104)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'v3i537rIt2b4B9H458g', CAST(N'2022-04-12T06:13:01.000' AS DateTime), 101, N'לחץ דם סיסטולי', 117.86, 72.6, 129.9, N'Admit cell recently.', 105)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'v3i537rIt2b4B9H458g', CAST(N'2022-04-12T06:13:01.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 134.18, 68.8, 83.75, N'Measure not.', 106)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'V4f744Avi1X7G0W592N', CAST(N'2022-04-10T16:45:44.000' AS DateTime), 11, N'טמפ', 152.91, 37.52, 140.67, N'Most computer.', 107)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'V4f744Avi1X7G0W592N', CAST(N'2022-04-10T16:45:44.000' AS DateTime), 12, N'דופק', 21.53, 71.9, 81.33, N'Congress view budget.', 108)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'V4f744Avi1X7G0W592N', CAST(N'2022-04-10T16:45:44.000' AS DateTime), 101, N'לחץ דם סיסטולי', 20.73, 79.86, 103.77, N'There a.', 109)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'V4f744Avi1X7G0W592N', CAST(N'2022-04-10T16:45:44.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 75.43, 47.45, 110.38, N'Author area I.', 110)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'x1Q512dbw0l8q8v997M', CAST(N'2022-04-12T05:49:29.000' AS DateTime), 11, N'טמפ', 125.83, 46.36, 105.1, N'Tough.', 111)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'x1Q512dbw0l8q8v997M', CAST(N'2022-04-12T05:49:29.000' AS DateTime), 12, N'דופק', 34.56, 69.3, 148.18, N'Radio professional.', 112)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'x1Q512dbw0l8q8v997M', CAST(N'2022-04-12T05:49:29.000' AS DateTime), 101, N'לחץ דם סיסטולי', 151.97, 53.21, 131.98, N'To remain.', 113)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'x1Q512dbw0l8q8v997M', CAST(N'2022-04-12T05:49:29.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 47.3, 53.69, 132.8, N'Look eight.', 114)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'X5k515WeD3K0h0x577b', CAST(N'2022-04-12T05:48:46.000' AS DateTime), 11, N'טמפ', 54.7, 42.24, 136.72, N'Key.', 115)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'X5k515WeD3K0h0x577b', CAST(N'2022-04-12T05:48:46.000' AS DateTime), 12, N'דופק', 151.54, 39.37, 94.91, N'Tv full.', 116)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'X5k515WeD3K0h0x577b', CAST(N'2022-04-12T05:48:46.000' AS DateTime), 101, N'לחץ דם סיסטולי', 138.52, 60.76, 94.51, N'Student live movement.', 117)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'X5k515WeD3K0h0x577b', CAST(N'2022-04-12T05:48:46.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 54.51, 71.72, 85.17, N'Indicate.', 118)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'y7R668dWb1Q3Y6n879I', CAST(N'2022-04-12T05:39:59.000' AS DateTime), 11, N'טמפ', 61.83, 61.5, 147.76, N'While.', 119)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'y7R668dWb1Q3Y6n879I', CAST(N'2022-04-12T05:40:01.000' AS DateTime), 12, N'דופק', 106.8, 72.1, 104.3, N'Success detail eat.', 120)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'y7R668dWb1Q3Y6n879I', CAST(N'2022-04-12T05:40:01.000' AS DateTime), 101, N'לחץ דם סיסטולי', 136.15, 71.47, 98.4, N'Special reason.', 121)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'y7R668dWb1Q3Y6n879I', CAST(N'2022-04-12T05:40:02.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 145.98, 67.89, 124.56, N'Party add.', 122)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F5Q924VhF6K7B7b752y', CAST(N'2022-04-12T21:18:19.000' AS DateTime), 11, N'טמפ', 98.74, 65.12, 94.78, N'Security table Democrat.', 123)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F5Q924VhF6K7B7b752y', CAST(N'2022-04-12T21:18:19.000' AS DateTime), 12, N'דופק', 149.58, 72.46, 90.32, N'Month allow friend.', 124)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F5Q924VhF6K7B7b752y', CAST(N'2022-04-12T21:18:19.000' AS DateTime), 101, N'לחץ דם סיסטולי', 147.71, 38.1, 124.67, N'Include such.', 125)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'F5Q924VhF6K7B7b752y', CAST(N'2022-04-12T21:18:19.000' AS DateTime), 102, N'לחץ דם דיאסטולי', 144.17, 49.59, 127.59, N'Join game brother.', 126)
GO
INSERT [dbo].[measurements] ([id_num], [Parameter_Date], [Parameter_Id], [Parameter_Name], [Result], [Min_Value], [Max_Value], [Warnings], [pk_measurement_id]) VALUES (N'G0g447npX3T0P3B514m', CAST(N'2022-04-12T21:18:19.000' AS DateTime), 11, N'טמפ', 23.67, 68.94, 128.7, N'Example themselves.', 127)
GO
SET IDENTITY_INSERT [dbo].[measurements] OFF
GO
USE [master]
GO
ALTER DATABASE [chameleon_db] SET  READ_WRITE
GO
