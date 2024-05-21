CREATE TABLE dhcp (
    id_dhcp UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    id_device UNIQUEIDENTIFIER,
    interface_name VARCHAR(50),
    client_ip_address VARCHAR(15),
    state VARCHAR(50),
    lease_server_address VARCHAR(15),
    gateway_address VARCHAR(15),
    lease_time INT,
    lease_expiry DATETIME,
    lease_remaining INT,
    primary_dns_address VARCHAR(15),
    secondary_dns_address VARCHAR(15),
    subnet_mask VARCHAR(15),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_device) REFERENCES devices(id_device)
);