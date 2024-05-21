CREATE TABLE arp (
    id_arp UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    id_device UNIQUEIDENTIFIER,
    ip_address VARCHAR(15),
    encryption_type VARCHAR(50),
    interface_name VARCHAR(50),
    link_type VARCHAR(50),
    arp_mode VARCHAR(50),
    hardware_type VARCHAR(50),
    mac_address VARCHAR(17),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_device) REFERENCES devices(id_device)
);