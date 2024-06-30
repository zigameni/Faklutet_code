-- Create the database
CREATE DATABASE Trznicentar;
GO

USE Trznicentar;
GO

-- Create the table for Trzni Centar
CREATE TABLE TrzniCentar (
    Id INT PRIMARY KEY IDENTITY,
    Naziv NVARCHAR(100) NOT NULL,
    RadnoVreme NVARCHAR(50) NOT NULL,
    BrojSpratova INT NOT NULL,
    PovrsinaSprata DECIMAL(10, 2) NOT NULL,
    Grad NVARCHAR(100) NOT NULL,
    Ulica NVARCHAR(100) NOT NULL,
    Broj NVARCHAR(10) NOT NULL
);
GO

-- Create the table for Sprat
CREATE TABLE Sprat (
    Id INT PRIMARY KEY IDENTITY,
    RedniBroj INT NOT NULL,
    KapacitetRadnji INT NOT NULL,
    KapacitetCistackogOsoblja INT NOT NULL,
    KapacitetSigurnosnogOsoblja INT NOT NULL,
    TrzniCentarId INT,
    FOREIGN KEY (TrzniCentarId) REFERENCES TrzniCentar(Id)
);
GO

-- Create the table for Radnja
CREATE TABLE Radnja (
    Id INT PRIMARY KEY IDENTITY,
    VlasnikId INT,
    Povrsina DECIMAL(10, 2) NOT NULL,
    KapacitetProdavaca INT NOT NULL,
    KapacitetSigurnosnogOsoblja INT NOT NULL,
    SpratId INT,
    FOREIGN KEY (SpratId) REFERENCES Sprat(Id)
);
GO

-- Create the table for Radnik
CREATE TABLE Radnik (
    BrLicneKarte NVARCHAR(20) PRIMARY KEY,
    Ime NVARCHAR(50) NOT NULL,
    Prezime NVARCHAR(50) NOT NULL,
    Grad NVARCHAR(100) NOT NULL,
    Ulica NVARCHAR(100) NOT NULL,
    Broj NVARCHAR(10) NOT NULL,
    BrojTelefona NVARCHAR(20) NOT NULL
);
GO

-- Create the table for Prodavac
CREATE TABLE Prodavac (
    RadnikId NVARCHAR(20),
    RadnjaId INT,
    PRIMARY KEY (RadnikId),
    FOREIGN KEY (RadnikId) REFERENCES Radnik(BrLicneKarte),
    FOREIGN KEY (RadnjaId) REFERENCES Radnja(Id)
);
GO

-- Create the table for CistackoOsoblje
CREATE TABLE CistackoOsoblje (
    RadnikId NVARCHAR(20),
    SpratId INT,
    PRIMARY KEY (RadnikId),
    FOREIGN KEY (RadnikId) REFERENCES Radnik(BrLicneKarte),
    FOREIGN KEY (SpratId) REFERENCES Sprat(Id)
);
GO

-- Create the table for MenadzerSprata
CREATE TABLE MenadzerSprata (
    RadnikId NVARCHAR(20),
    SpratId INT,
    PRIMARY KEY (RadnikId),
    FOREIGN KEY (RadnikId) REFERENCES Radnik(BrLicneKarte),
    FOREIGN KEY (SpratId) REFERENCES Sprat(Id)
);
GO

-- Create the table for SigurnosnoOsoblje
CREATE TABLE SigurnosnoOsoblje (
    RadnikId NVARCHAR(20),
    RadnjaId INT NULL,
    SpratId INT NULL,
    PRIMARY KEY (RadnikId),
    FOREIGN KEY (RadnikId) REFERENCES Radnik(BrLicneKarte),
    FOREIGN KEY (RadnjaId) REFERENCES Radnja(Id),
    FOREIGN KEY (SpratId) REFERENCES Sprat(Id)
);
GO

-- Create the table for Vlasnik
CREATE TABLE Vlasnik (
    RadnikId NVARCHAR(20),
    PRIMARY KEY (RadnikId),
    FOREIGN KEY (RadnikId) REFERENCES Radnik(BrLicneKarte)
);
GO

-- Create the table for MenadzerTrznogCentra
CREATE TABLE MenadzerTrznogCentra (
    RadnikId NVARCHAR(20),
    TrzniCentarId INT,
    PRIMARY KEY (RadnikId, TrzniCentarId),
    FOREIGN KEY (RadnikId) REFERENCES Radnik(BrLicneKarte),
    FOREIGN KEY (TrzniCentarId) REFERENCES TrzniCentar(Id)
);
GO
