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

---

## Ubuntu Netplan YAML was appended to the previous configuration

Observed during restoration from NAT/DHCP to static VMnet2 networking. `netplan generate` reported inconsistent indentation at a joined `set-name: ens33network:` line. The editor contained both the new and old network blocks.

The file was corrected to a single complete YAML document after backing up `/etc/netplan`. `netplan generate` then completed without an error. The final network was validated after startup; see [the verified configuration](../configs/ubuntu/00-installer-config.yaml).

## Ubuntu could reach Windows DNS by IP but not resolve corp.local

`resolvectl query SERVER01.corp.local` returned `No appropriate name servers or networks for name found`, although ens33 listed DNS 192.168.30.10. A temporary routing domain `~corp.local` made the query succeed. The permanent Netplan configuration added `search: [corp.local]` under nameservers. After reboot, resolvectl listed `corp.local` and the query succeeded without reapplying the temporary setting.

## Static Ubuntu IP overlapped the Windows DHCP pool

Ubuntu .30 lay inside the .20–.100 scope, which initially had no exclusion. No .30 lease was present. An exclusion of 192.168.30.30–192.168.30.30 was added; CLIENT01's .20 reservation was retained. No actual duplicate-IP outage was observed or claimed.

## Ubuntu hostname was absent from Windows DNS

Forward lookup of UBUNTU01.corp.local returned name not found. DNS Manager confirmed no UBUNTU01 entry. A Host (A) record and associated PTR were added; Ubuntu then resolved both name -> .30 and .30 -> name.

## Permission denied for sysadmin on the group-only lab directory

Unprivileged sysadmin could not list the root:labops directory with mode 2770. The member identity successfully read and modified data, while labguest was denied. This was expected permission enforcement, not repaired by widening rights.

## Python firewall-test listener remained after the UFW rule was removed

The firewall rule had been deleted but ss still showed a port 8088 listener. Ctrl+C was sent in the terminal actually running Python. A subsequent ss check had no listener rows. Firewall rules and application processes were verified separately.

## systemd verification printed XFS CPUAccounting warnings

The warnings named installed XFS units, not system-lab-demo.service. The custom unit started successfully, was enabled, supported stop/start, and ran again after reboot. Vendor unit files were not edited; the deprecation warnings were not claimed as resolved.

## Console login failed while SSH password login worked

The user could authenticate as sysadmin over SSH but reported failed VM-console logins. A keyboard-layout/input difference was suspected, not established. No password reset or confirmed console fix was performed.
