CREATE TABLE software (
    id_software UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    id_device UNIQUEIDENTIFIER,
    current_time_device VARCHAR(30),
    boot_time VARCHAR(30),
    software_version TEXT,
    rommon_version VARCHAR(20),
    last_reboot_reason VARCHAR(20),
    FOREIGN KEY (id_device) REFERENCES devices(id_device)
);
