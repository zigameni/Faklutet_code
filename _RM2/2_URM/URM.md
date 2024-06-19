# Network Systems and Management

<div align="justify">



## Concepts of Network Management

### Classical Network Management

- **Independent Devices**: Network devices operate independently, each with its own specialized hardware, operating system, application software (protocols), and set of interfaces.
- **Independent Network View**: Each device independently calculates its own view of the network and forwarding rules.
- **Individual Device Management**: Devices are managed independently, requiring separate configuration and monitoring.
- **Advanced Networks**: Utilize software tools for device and service management.

### Software Defined Networking (SDN)

- **Standard Protocol**: Communication between devices and a central controller uses a standardized protocol.
- **Packet Forwarding**: Communication devices primarily serve to forward packets.
- **Centralized Control**: The controller manages all devices within its domain, calculating paths and forwarding rules.

#### SDN Example

- **OpenFlow Protocol**: Used for sending forwarding rules.
  - `If header = p, forward to port 4`
  - `If header = q, rewrite header to h, forward to port 1`
  - `If header = r, forward to ports 2, 5, and 6`

## Network Management Scope

### ISO FCAPS Model (Device-Oriented)

- **Fault**: Detecting and managing network faults.
- **Configuration**: Setting up and maintaining network configurations.
- **Accounting**: Tracking usage for billing or analysis.
- **Performance**: Monitoring and ensuring network performance.
- **Security**: Securing the network and data.

### TMF Model (Service-Oriented)

- **OSS Components Design**: Encompasses the entire design of Operational Support System (OSS) components.
- **Business Framework (eTOM)**: A comprehensive framework for managing business processes.
- **Application Framework (TAM)**: Provides a structure for application development.
- **Information Framework (SID)**: Defines data models and relationships.
- **Interfaces (MTOSI, OSS/J)**: Standard interfaces for integrating various management systems.

## Network Monitoring Methods

### Passive Monitoring

- **Variable Reading**: Uses different protocols to read variables.
  - **Challenge**: Monitoring end-to-end performance and accessing devices in other domains.

### Active Monitoring

- **Test Packets**: Sending test packet sequences to derive desired path parameters.
  - **Examples**: Ping and traceroute for determining device availability and network paths.

#### Active Network Monitoring Tools

- **IETF IPPM Working Group**: Focuses on IP Performance Metrics.
  - **OWAMP (RFC 4656)**: Measures one-way delay.
  - **TWAMP (RFC 5357)**: Measures two-way delay, jitter, packet loss, and reordering.
- **Vendor Tools**: Cisco IP SLA, Juniper Real-time Performance Monitoring (RPM).
- **RIPE Projects**: 
  - **TTM**: Measures delay, packet loss, jitter, available bandwidth using GPS-equipped computers.
  - **Atlas**: Thousands of probes worldwide conduct ICMP tests.

### RIPE Atlas Project

- **Initiated**: Fall 2010.
- **Probes**: Devices like Lantronix Xport Pro and Raspberry Pi perform ICMP tests.
- **Scope**: Over 10,000 probes globally.

## Network Management Technologies

### Command Line Interface (CLI)

- **Access**: Device access via Telnet/SSH.
- **Configuration**: Input configuration parameters through the shell.
- **Startup Configuration**: Configuration file loaded during device startup.
- **Monitoring**: Possible to monitor link status and protocols.

### Simple Network Management Protocol (SNMP)

- **Versions**:
  - **v1**: RFC 1157
  - **v2**: RFC 3416 - 3418
  - **v3**: RFC 3410 - 3418
- **Entities**: Consists of agents and Network Management Systems (NMS).
- **Information Storage**: Managed in Management Information Base (MIB).
- **Transport Protocol**: Uses UDP (ports 161 for sending/receiving, 162 for traps).

### SNMP Data Types

- **v1**: Integer, Octet string, Counter, OID, IpAddress, Gauge, TimeTicks.
- **v2**: Integer32, Counter32, Counter64.
- **Operations**: get, getnext, getbulk, set, getresponse, trap, notification, inform, report.

### SNMPv3 Security

- **User-based Security Model**:
  - **Levels**: noAuthNoPriv, authNoPriv, authPriv.
  - **Algorithms**: MD5, SHA, HMAC versions, and encryption (DES, 3DES, AES).
- **View-based Access Control Model**: Defines access levels to MIB objects.

### syslog

- **Origin**: Derived from Unix systems for logging events.
- **Function**: Logs significant events based on importance.
- **Protocol**: Transmits log messages to a central station.
- **Reconstruction**: Essential for reconstructing network events.

### Modern Log Processing Tools

- **Examples**: ELK stack (Elasticsearch, Logstash, Kibana), Graylog, Splunk, SIEM tools, AIOps.

### NetFlow/IPFIX

- **Traffic Statistics**: Collects data on traffic flows.
- **Flow Definition**: Determined by IP addresses, layer 4 ports, layer 3 protocol type, ToS fields.
- **Usage**: Enables traffic log searches, security analysis, anomaly detection, and sampling for high-speed interfaces.

### NETCONF

- **RFCs**: 4741, 6241
- **Function**: Designed for configuration management, complements SNMP's passive monitoring.
- **Data Format**: Uses XML for configuration data.
- **Transport**: Transmitted via SSH, TLS, SOAP, BEEP.
- **Configuration**: Whole or partial configurations can be sent as NETCONF messages.
- **Operations**: get-config, edit-config, copy-config, delete-config, lock, unlock, get, close-session, kill-session.
- **YANG (RFC 6020)**: Language for specifying configuration data models.
- **OpenConfig**: A collaborative effort to standardize network configuration models.

This document provides a comprehensive overview of network systems and management, detailing the classical and modern approaches, monitoring methods, technologies used, and various tools and protocols involved.

<div>
