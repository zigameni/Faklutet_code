-- Create table OBJEKAT
CREATE TABLE OBJEKAT (
    SifO INT PRIMARY KEY,
    Naziv VARCHAR(100) NOT NULL
);

-- Create table SEKTOR
CREATE TABLE SEKTOR (
    SifS INT PRIMARY KEY,
    Oznaka VARCHAR(10) NOT NULL,
    FaktorS DECIMAL(5, 2) NOT NULL,
    BrojRedova INT NOT NULL,
    SifO INT,
    FOREIGN KEY (SifO) REFERENCES OBJEKAT(SifO)
);

-- Create table RED
CREATE TABLE RED (
    SifR INT PRIMARY KEY,
    Broj INT NOT NULL,
    FaktorR DECIMAL(5, 2) NOT NULL,
    BrojSedišta INT NOT NULL,
    SifS INT,
    FOREIGN KEY (SifS) REFERENCES SEKTOR(SifS)
);

-- Create table DOGADJAJ
CREATE TABLE DOGADJAJ (
    SifD INT PRIMARY KEY,
    Naziv VARCHAR(100) NOT NULL,
    Opis TEXT,
    Datum DATE NOT NULL,
    OsnovnaCena DECIMAL(10, 2) NOT NULL,
    BrojPreostalihUlaznica INT
);

-- Create table DOGADJAJ_OTKAZAN
CREATE TABLE DOGADJAJ_OTKAZAN (
    SifD INT PRIMARY KEY,
    DatumOtkazivanja DATE NOT NULL,
    FOREIGN KEY (SifD) REFERENCES DOGADJAJ(SifD)
);

-- Create table KUPAC
CREATE TABLE KUPAC (
    SifK INT PRIMARY KEY,
    Ime VARCHAR(50) NOT NULL,
    Prezime VARCHAR(50) NOT NULL,
    Email VARCHAR(100),
    KorisnickoIme VARCHAR(50),
    Lozinka VARCHAR(50),
    BrojTelefona VARCHAR(20)
);

-- Create table ULAZNICA
CREATE TABLE ULAZNICA (
    SifU INT PRIMARY KEY,
    SifD INT,
    SifK INT,
    Datum DATE NOT NULL,
    SifraPlacanja VARCHAR(50),
    Status CHAR(1) CHECK (Status IN ('S', 'P')),
    SifR INT,
    FOREIGN KEY (SifD) REFERENCES DOGADJAJ(SifD),
    FOREIGN KEY (SifK) REFERENCES KUPAC(SifK),
    FOREIGN KEY (SifR) REFERENCES RED(SifR)
);

-- Create table KUPON
CREATE TABLE KUPON (
    SifK INT,
    Sifra VARCHAR(50) PRIMARY KEY,
    Popust DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (SifK) REFERENCES KUPAC(SifK)
);

-- Insert sample data into OBJEKAT
INSERT INTO OBJEKAT (SifO, Naziv) VALUES
(1, 'Arena'),
(2, 'Stadium'),
(3, 'Concert Hall');

-- Insert sample data into SEKTOR
INSERT INTO SEKTOR (SifS, Oznaka, FaktorS, BrojRedova, SifO) VALUES
(1, 'A', 1.5, 10, 1),
(2, 'B', 1.2, 15, 1),
(3, 'C', 1.1, 20, 2),
(4, 'D', 1.3, 5, 3);

-- Insert sample data into RED
INSERT INTO RED (SifR, Broj, FaktorR, BrojSedišta, SifS) VALUES
(1, 1, 1.2, 30, 1),
(2, 2, 1.1, 25, 1),
(3, 1, 1.3, 20, 2),
(4, 2, 1.2, 15, 2),
(5, 1, 1.1, 50, 3),
(6, 1, 1.4, 10, 4);

-- Insert sample data into DOGADJAJ
INSERT INTO DOGADJAJ (SifD, Naziv, Opis, Datum, OsnovnaCena, BrojPreostalihUlaznica) VALUES
(1, 'Concert A', 'Rock concert', '2024-07-15', 50.00, 500),
(2, 'Football Match', 'Local football league', '2024-08-01', 30.00, 1000),
(3, 'Opera Night', 'Classical opera performance', '2024-09-10', 70.00, 300);

-- Insert sample data into KUPAC
INSERT INTO KUPAC (SifK, Ime, Prezime, Email, KorisnickoIme, Lozinka, BrojTelefona) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', 'jdoe', 'password123', '123-456-7890'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', 'jsmith', 'mypassword', '234-567-8901'),
(3, 'Alice', 'Johnson', 'alice.johnson@example.com', 'ajohnson', 'alice2024', '345-678-9012');

-- Insert sample data into ULAZNICA
INSERT INTO ULAZNICA (SifU, SifD, SifK, Datum, SifraPlacanja, Status, SifR) VALUES
(1, 1, 1, '2024-07-01', 'PAY001', 'P', 1),
(2, 1, 2, '2024-07-01', 'PAY002', 'P', 2),
(3, 2, 1, '2024-07-10', 'PAY003', 'P', 3),
(4, 3, 3, '2024-08-20', 'PAY004', 'S', 5);

-- Insert sample data into KUPON
INSERT INTO KUPON (SifK, Sifra, Popust) VALUES
(1, 'DISC10', 10.00),
(2, 'DISC15', 15.00),
(3, 'DISC20', 20.00);
