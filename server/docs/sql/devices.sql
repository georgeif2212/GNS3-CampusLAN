CREATE TABLE devices (
    id_device UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    hostname VARCHAR(50),
    software_version VARCHAR(50),
    model VARCHAR(50),
    serial_number VARCHAR(50),
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