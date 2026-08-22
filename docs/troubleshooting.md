# Troubleshooting Notes

## CLIENT01 could not retrieve computer GPO result

Problem:
`gpresult /r /scope computer` returned Access Denied.

Cause:
The command was executed from a non-elevated shell.

Solution:
Opened PowerShell as Administrator using an administrative account and reran the command.

---

## CLIENT01 was still using a static IP

Problem:
DHCP was configured on SERVER01 but CLIENT01 showed `DHCP Enabled: No`.

Solution:
Enabled DHCP on the Ethernet adapter, reset DNS server configuration, and renewed the lease.

Result:
CLIENT01 received `192.168.30.20` from SERVER01.

---

## DNS server displayed as Unknown

Problem:
`nslookup` returned `Server: Unknown`.

Cause:
A reverse lookup / PTR record was missing.

Solution:
Created a Reverse Lookup Zone for `192.168.30.0/24` and PTR record for SERVER01.

Result:
`192.168.30.10` successfully resolved to `SERVER01.corp.local`.
