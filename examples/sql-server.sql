CREATE TABLE [Enrollments].[StudentData]
(
    [StudentId] INT IDENTITY(1,1) PRIMARY KEY,
    [StudentFirstName] NVARCHAR(100),
    [StudentLastName] NVARCHAR(100),
    [StudentProfileUrl] NVARCHAR(255) UNIQUE
);