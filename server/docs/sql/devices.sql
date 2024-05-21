CREATE TABLE devices (
    ID_Device UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    HostName VARCHAR(50),
    SoftwareVersion VARCHAR(50),
    Model VARCHAR(50),
    SerialNumber VARCHAR(50),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trgUpdateTimestamp ON devices
AFTER
UPDATE
    AS BEGIN
SET
    NOCOUNT ON;

UPDATE
    devices
SET
    datetime = CURRENT_TIMESTAMP
FROM
    inserted
WHERE
    devices.ID_Device = inserted.ID_Device;

END;