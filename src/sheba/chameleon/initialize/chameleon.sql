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
	[Room] [int] NULL
) ON [PRIMARY]
GO
CREATE TABLE [dbo].[faker_beds](
	[room] [nvarchar](150) NULL,
	[bed_name] [nvarchar](150) NULL,
	[row_id] [int] IDENTITY(1,1) NOT NULL
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
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'1')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'2')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'3')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'4')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'5')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'6')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'7')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'8')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'9')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'10')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'11')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'12')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'13')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b1', N'14')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'1')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'2')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'3')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'4')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'5')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'6')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'7')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'8')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'9')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'10')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'11')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'12')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'13')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'14')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'15')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'16')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'17')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'18')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'19')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b2', N'20')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'1')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'2')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'3')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'4')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'5')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'6')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'7')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'8')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'9')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'10')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'11')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'12')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'b3', N'13')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'1')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'2')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'3')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'4')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'5')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'6')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'7')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'8')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'9')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'10')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'11')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'12')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'13')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'14')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'15')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'16')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'17')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'18')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'19')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'20')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'21')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'22')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'23')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'24')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'25')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'26')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'27')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'28')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'29')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'30')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'31')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'32')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'33')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'34')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'35')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'36')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'37')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'38')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'39')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'40')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'41')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'42')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'43')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'44')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'45')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'46')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'47')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'48')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'49')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'50')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'51')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'52')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'53')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'54')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'55')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'56')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'57')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'58')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'59')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'60')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'61')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'62')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'63')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'64')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'65')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'66')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'67')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'68')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'69')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'70')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'71')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'72')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'73')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'74')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'75')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'76')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'77')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'78')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'79')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'80')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'81')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'82')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'83')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'84')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'85')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'86')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'87')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'88')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'89')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'90')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'91')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'92')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'93')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'94')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'95')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'96')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'97')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'98')
GO
insert [dbo].[faker_beds] ([room], [bed_name]) VALUES (N'a', N'99')
GO
SET IDENTITY_INSERT [dbo].[RoomBeds] ON
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'1', 1)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'2', 2)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'3', 3)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'4', 4)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'5', 5)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'6', 6)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'7', 7)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'8', 8)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'9', 9)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'10', 10)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'11', 11)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'12', 12)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'13', 13)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'14', 14)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'1', 15)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'2', 16)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'3', 17)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'4', 18)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'5', 19)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'6', 20)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'7', 21)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'8', 22)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'9', 23)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'10', 24)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'11', 25)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'12', 26)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'13', 27)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'14', 28)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'15', 29)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'16', 30)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'17', 31)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'18', 32)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'19', 33)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'20', 34)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'1', 35)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'2', 36)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'3', 37)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'4', 38)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'5', 39)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'6', 40)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'7', 41)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'8', 42)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'9', 43)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'10', 44)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'11', 45)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'12', 46)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'13', 47)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'1', 48)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'2', 49)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'3', 50)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'4', 51)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'5', 52)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'6', 53)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'7', 54)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'8', 55)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'9', 56)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'10', 57)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'11', 58)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'12', 59)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'13', 60)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'14', 61)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'15', 62)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'16', 63)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'17', 64)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'18', 65)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'19', 66)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'20', 67)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'21', 68)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'22', 69)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'23', 70)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'24', 71)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'25', 72)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'26', 73)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'27', 74)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'28', 75)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'29', 76)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'30', 77)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'31', 78)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'32', 79)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'33', 80)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'34', 81)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'35', 82)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'36', 83)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'37', 84)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'38', 85)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'39', 86)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'40', 87)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'41', 88)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'42', 89)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'43', 90)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'44', 91)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'45', 92)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'46', 93)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'47', 94)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'48', 95)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'49', 96)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'50', 97)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'51', 98)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'52', 99)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'53', 100)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'54', 101)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'55', 102)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'56', 103)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'57', 104)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'58', 105)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'59', 106)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'60', 107)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'61', 108)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'62', 109)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'63', 110)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'64', 111)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'65', 112)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'66', 113)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'67', 114)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'68', 115)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'69', 116)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'70', 117)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'71', 118)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'72', 119)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'73', 120)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'74', 121)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'75', 122)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'76', 123)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'77', 124)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'78', 125)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'79', 126)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'80', 127)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'81', 128)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'82', 129)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'83', 130)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'84', 131)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'85', 132)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'86', 133)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'87', 134)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'88', 135)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'89', 136)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'90', 137)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'91', 138)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'92', 139)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'93', 140)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'94', 141)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'95', 142)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'96', 143)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'97', 144)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'98', 145)
GO
INSERT [dbo].[RoomBeds] ([Bed_Name], [row_id]) VALUES (N'99', 146)
GO
SET IDENTITY_INSERT [dbo].[RoomBeds] OFF
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
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (10, 1184000, 99, N'a')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (11, 1184000, 13, N'b1')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (12, 1184000, 14, N'b2')
GO
INSERT [dbo].[RoomDetails] ([Room_Code], [Unit], [Beds], [Room_Name]) VALUES (13, 184000, 20, N'b3')
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