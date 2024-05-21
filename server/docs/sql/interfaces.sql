CREATE TABLE interfaces (
    id_interface UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    id_device UNIQUEIDENTIFIER,
    interface_name VARCHAR(50),
    ip_address VARCHAR(15),
    subnet_mask VARCHAR(15),
    cdp_state VARCHAR(20),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_device) REFERENCES devices(id_device)
);