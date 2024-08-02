CREATE TABLE hardware (
    id_hardware UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    id_device UNIQUEIDENTIFIER,
    hw_type VARCHAR(50),
    hw_dev_index INT,
    version VARCHAR(50),
    part_number VARCHAR(50),
    serial_number VARCHAR(50),
    hw_description VARCHAR(255),
    FOREIGN KEY (id_device) REFERENCES devices(id_device)
);
