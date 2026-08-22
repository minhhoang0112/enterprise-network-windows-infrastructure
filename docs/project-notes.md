# Project Source of Truth

Use this file as the factual reference when editing the README with VS Code, Codex, or another AI assistant.

## Project Name
Enterprise Network & Windows Server Infrastructure Lab

## Important Accuracy Rule
Do NOT claim that Cisco Packet Tracer and VMware are directly connected.
They are complementary lab environments representing the network layer and system-services layer of the same enterprise design.

## Packet Tracer
- VLAN 10: Admin / IT - 192.168.10.0/24
- VLAN 20: Staff - 192.168.20.0/24
- VLAN 30: Server - 192.168.30.0/24
- VLAN 40: Guest WiFi - 192.168.40.0/24
- VLAN 99: Management - 192.168.99.0/24
- Routing / inter-VLAN connectivity configured
- Guest access restrictions / ACL used
- NAT / external connectivity simulation used
- Edge router, switches, ISP/public network simulated

## VMware / Windows
- SERVER01: Windows Server 2022
- SERVER01 IP: 192.168.30.10/24
- Domain: corp.local
- CLIENT01: Windows 10 Pro
- CLIENT01 joined corp.local
- CLIENT01 uses Windows Server DNS
- CLIENT01 receives DHCP from SERVER01
- DHCP pool: 192.168.30.20 - 192.168.30.100
- CLIENT01 reservation: 192.168.30.20
- DNS forward + reverse lookup configured

## Active Directory
CORP
- Computers
- Groups
- Servers
- Users
  - IT
  - HR
  - Accounting
  - Sales

Security groups:
- GG_IT
- GG_HR
- GG_Accounting
- GG_Sales

Sample users:
- an.nguyen -> GG_IT
- lan.tran -> GG_HR
- hoa.le -> GG_Accounting
- nam.pham -> GG_Sales

## File Server
D:\CORP-DATA
- IT
- HR
- Accounting
- Sales
- Public

Share:
\\SERVER01\CORP-DATA

Departmental groups receive Modify permission to their own folders.

## GPO
- GPO-CLIENT-BASELINE linked to CORP\Computers
- GPO-USER-BASELINE linked to CORP\Users
- User restrictions tested: Control Panel restriction, CMD restriction, Registry Editor restriction
- Drive Maps deployed using Group Policy Preferences + item-level targeting

Drive mappings:
- GG_IT -> I: -> \\SERVER01\CORP-DATA\IT
- GG_HR -> H: -> \\SERVER01\CORP-DATA\HR
- GG_Accounting -> A: -> \\SERVER01\CORP-DATA\Accounting
- GG_Sales -> S: -> \\SERVER01\CORP-DATA\Sales
- Public -> P: -> \\SERVER01\CORP-DATA\Public

## Validation already completed
- Domain login on CLIENT01
- whoami -> corp\an.nguyen
- hostname -> CLIENT01
- logon server -> \\SERVER01
- DNS forward lookup
- DNS reverse lookup
- DHCP lease
- DHCP reservation
- GPO application
- CMD restriction
- IT folder access
- Cross-department access restriction
- IT mapped drive
- Public mapped drive
