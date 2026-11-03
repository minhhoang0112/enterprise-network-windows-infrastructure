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
- Ubuntu static IP exclusion: 192.168.30.30 - 192.168.30.30, added 2026-10-30
- DNS forward + reverse lookup configured

## VMware / Ubuntu — verified 2026-10-30

- Ubuntu belongs to the project and now shares VMnet2 Host-only with Windows; the previous NAT/DHCP setup was a separate learning configuration.
- UBUNTU01: Ubuntu 26.04.1 LTS, kernel 7.0.0-42-generic, as reported by the VM.
- Interface ens33; static IP 192.168.30.30/24; DNS 192.168.30.10; search domain corp.local.
- No default gateway; Windows host 192.168.30.1 is not a router.
- Windows DNS A/PTR for UBUNTU01.corp.local were created and validated in both directions.
- SSH TCP 22 works from Windows, including after reboot.
- Local group labops contains labmember; labguest is outside labops. These are Linux local accounts, not AD accounts.
- /srv/system-lab/team is owned by root:labops with mode 2770. Member create/read/modify/delete and nonmember read/create denial were tested.
- UFW active: deny incoming, allow outgoing, allow 22/tcp for IPv4/IPv6.
- Temporary TCP 8088 listener tested blocked/allowed/blocked; rule removed and listener stopped.
- system-lab-demo.service is an enabled oneshot journal exercise; active (exited) is expected, not evidence of a permanent application service.
- SSH, DNS, permissions, firewall and demo service validated after reboot.
- Exported report: docs/evidence/ubuntu-report-2026-10-30.txt. Chat-derived supplementary evidence: docs/evidence/ubuntu-validation-2026-10-30.md.
- Review is based on user-provided outputs; no direct VM execution by the reviewer. Existing Windows/Packet Tracer tests were not comprehensively rerun.
- No AD join, permanent web server, Linux DHCP/DNS server, backup/restore deployment or monitoring is claimed.

Current Ubuntu details take precedence over the original NAT-based handover and personal execution plan, which are kept locally rather than published. See docs/ubuntu-server-lab.md.

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
