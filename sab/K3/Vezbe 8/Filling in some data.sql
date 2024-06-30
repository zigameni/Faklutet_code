USE Trznicentar;
GO

-- Insert data into TrzniCentar
INSERT INTO TrzniCentar (Naziv, RadnoVreme, BrojSpratova, PovrsinaSprata, Grad, Ulica, Broj)
VALUES 
('Centar 1', '09:00-21:00', 3, 200.00, 'Belgrade', 'Ulica 1', '10'),
('Centar 2', '10:00-22:00', 2, 150.00, 'Novi Sad', 'Ulica 2', '20');
GO

-- Insert data into Sprat
INSERT INTO Sprat (RedniBroj, KapacitetRadnji, KapacitetCistackogOsoblja, KapacitetSigurnosnogOsoblja, TrzniCentarId)
VALUES 
(1, 10, 2, 3, 1),
(2, 8, 2, 2, 1),
(3, 6, 1, 2, 1),
(1, 5, 1, 1, 2),
(2, 4, 1, 1, 2);
GO

-- Insert data into Radnik
INSERT INTO Radnik (BrLicneKarte, Ime, Prezime, Grad, Ulica, Broj, BrojTelefona)
VALUES 
('123456789', 'Marko', 'Markovic', 'Belgrade', 'Ulica A', '1', '060123456'),
('987654321', 'Jovana', 'Jovanovic', 'Belgrade', 'Ulica B', '2', '060654321'),
('456789123', 'Petar', 'Petrovic', 'Novi Sad', 'Ulica C', '3', '060987654'),
('321654987', 'Ana', 'Anic', 'Novi Sad', 'Ulica D', '4', '060321654'),
('741852963', 'Ivan', 'Ivanovic', 'Belgrade', 'Ulica E', '5', '060741852');
GO

-- Insert data into Radnja
INSERT INTO Radnja (VlasnikId, Povrsina, KapacitetProdavaca, KapacitetSigurnosnogOsoblja, SpratId)
VALUES 
('123456789', 50.00, 3, 2, 1),
('987654321', 45.00, 2, 1, 2),
('456789123', 30.00, 1, 1, 3),
('321654987', 40.00, 2, 1, 4);
GO

-- Insert data into Prodavac
INSERT INTO Prodavac (RadnikId, RadnjaId)
VALUES 
('741852963', 1),
('321654987', 2);
GO

-- Insert data into CistackoOsoblje
INSERT INTO CistackoOsoblje (RadnikId, SpratId)
VALUES 
('987654321', 1),
('123456789', 2);
GO

-- Insert data into MenadzerSprata
INSERT INTO MenadzerSprata (RadnikId, SpratId)
VALUES 
('456789123', 3);
GO

-- Insert data into SigurnosnoOsoblje
INSERT INTO SigurnosnoOsoblje (RadnikId, RadnjaId, SpratId)
VALUES 
('321654987', 1, NULL),
('123456789', NULL, 1);
GO

-- Insert data into Vlasnik
INSERT INTO Vlasnik (RadnikId)
VALUES 
('123456789'),
('987654321');
GO

-- Insert data into MenadzerTrznogCentra
INSERT INTO MenadzerTrznogCentra (RadnikId, TrzniCentarId)
VALUES 
('456789123', 1),
('321654987', 2);
GO
