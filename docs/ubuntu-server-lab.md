# Ubuntu Server Administration Lab

Last evidence date: **2026-10-30**. Documentation updated: **2026-11-03**.

This is the completed basic Ubuntu administration scope for the portfolio lab. Validation is based on user-supplied VM screenshots, command output and an exported report, not direct execution by the reviewer. See the [report](evidence/ubuntu-report-2026-10-30.txt) and [supplementary validation record](evidence/ubuntu-validation-2026-10-30.md).

## Architecture and scope

The Ubuntu VM shares VMware **VMnet2 Host-only** with SERVER01 and CLIENT01. It uses Windows DNS and its static address is excluded from Windows DHCP. It remains a Linux host with local accounts: using the `corp.local` DNS zone does not join Ubuntu to Active Directory.

Cisco Packet Tracer is a separate simulation. The UBUNTU01 device in the Packet Tracer topology represents the design, not a live connection to this VM.

| Item | Observed value |
|---|---|
| Hostname | UBUNTU01 |
| OS / kernel | Ubuntu 26.04.1 LTS / Linux 7.0.0-42-generic, as reported by the VM |
| Interface / MAC | ens33 / 00:0c:29:d7:6a:f7 |
| IPv4 | 192.168.30.30/24, static |
| VMware network | Custom: VMnet2, Host-only, 192.168.30.0/24 |
| DNS / search domain | 192.168.30.10 / corp.local |
| Default IP route | None |
| Windows host VMnet2 address | 192.168.30.1, not a router |
| Windows Server | SERVER01, 192.168.30.10 |
| Windows client | CLIENT01, DHCP reservation 192.168.30.20 |
| SSH administration | sysadmin, TCP 22 |

## Restored static network

Ubuntu had temporarily been moved to NAT on VMnet8 with DHCP address `192.168.11.134` for separate Linux learning. That is historical, not the current project configuration.

The existing `/etc/netplan` directory was backed up to a timestamped `/root/netplan-backup-*` directory before editing. The file `/etc/netplan/00-installer-config.yaml` was replaced with the [verified configuration](../configs/ubuntu/00-installer-config.yaml), validated with `sudo netplan generate`, and applied on VMnet2. A later DNS change was tested using `sudo netplan try --timeout 120` and confirmed.

The interface/MAC in the repository copy is specific to this VM. Do not copy it to another VM without checking `ip link` and the existing Netplan files.

Verified commands and expected results:

```bash
ip -br -4 address
ip route
resolvectl status ens33
```

- ens33 UP, 192.168.30.30/24.
- Connected route for 192.168.30.0/24; no `default via` route.
- DNS 192.168.30.10 and search domain corp.local.

`Default Route: yes` in `resolvectl` describes DNS routing selection; it does not add an IP default gateway. The actual IP routes are shown by `ip route`.

## Windows DHCP exclusion and DNS records

The Windows DHCP scope is 192.168.30.20–192.168.30.100. Its lease list showed CLIENT01 at .20 and no .30 lease. A single-address exclusion `.30–.30` was added to prevent automatic allocation of the static Ubuntu address. CLIENT01's reservation was retained.

Windows DNS Manager initially had no UBUNTU01 host record. A Host (A) record for UBUNTU01 -> 192.168.30.30 was added with the associated PTR option. Both directions were then tested from Ubuntu:

```bash
resolvectl query SERVER01.corp.local
resolvectl query UBUNTU01.corp.local
resolvectl query 192.168.30.30
```

Results were .10, .30 and UBUNTU01.corp.local respectively. Ubuntu also reached SERVER01 using `ping -c 4 192.168.30.10`, with 4/4 replies.

## SSH and logs

Windows host command:

```powershell
ssh sysadmin@192.168.30.30
```

The user successfully opened new SSH sessions, including after UFW activation and reboot. The SSH output showed a port 22 listener and successful password authentication from 192.168.30.1.

```bash
systemctl status ssh.service ssh.socket --no-pager
sudo journalctl -u ssh.service -b -n 20 --no-pager
```

Both service and socket were reported enabled/active in the supplied output. No SSH port change, root login configuration or key-only authentication is claimed.

## Local users, groups and permissions

| Object | Configuration |
|---|---|
| labops | Local group, observed GID 1005 |
| labmember | Local user, member of labops |
| labguest | Local user, not a member of labops |
| /srv/system-lab | root:root, 0755 |
| /srv/system-lab/team | root:labops, 2770 (`drwxrws---`) |
| member.txt | labmember:labops, 0660; two lines of sample text |

Users were created with `adduser`; labmember was added using `usermod -aG labops labmember`. Neither test user was granted sudo by this exercise. Passwords are not recorded.

The member file was created under `umask 007`. Directory setgid preserves the directory group for new entries; it does not independently guarantee group write access for every future file.

Verified behavior:

- labmember created, read, appended to and copied the sample file, then deleted the temporary copy.
- labguest could neither read member.txt nor create a file in team.
- sysadmin's unprivileged `ls` also received Permission denied, consistent with the group restrictions.
- Member read and nonmember read denial still held after reboot.

Example read checks use the test identities, not root:

```bash
sudo -u labmember cat /srv/system-lab/team/member.txt
sudo -u labguest cat /srv/system-lab/team/member.txt
```

The second command is expected to fail. Do not widen permissions to make that test pass.

## UFW with a controlled connectivity test

Final policy: UFW active and enabled at startup, deny incoming, allow outgoing, with only TCP 22 allowed for IPv4 and IPv6. Rules allow SSH from any reachable source in this isolated lab; this is not a production security baseline.

The test used a Python HTTP listener bound to 0.0.0.0:8088 serving only `~/system-lab/http-test`, containing a sample index.html. Windows host checks used:

```powershell
Test-NetConnection 192.168.30.30 -Port 8088
```

| Listener running | Temporary UFW allow 8088 | Observed TCP result |
|---|---|---|
| Yes | No | False |
| Yes | Yes | True |
| Yes | Removed | False |

Afterward the Python process was stopped with Ctrl+C. `ss -lnt 'sport = :8088'` showed only its header, and `ufw status numbered` showed only the two SSH rules. This was a firewall exercise, not a deployed web application.

## systemd service exercise

The [unit file](../configs/ubuntu/system-lab-demo.service) was saved at `/etc/systemd/system/system-lab-demo.service`. It runs `logger` once and remains logically active; no continuous application process is expected.

```bash
sudo systemd-analyze verify /etc/systemd/system/system-lab-demo.service
sudo systemctl daemon-reload
sudo systemctl enable --now system-lab-demo.service
systemctl status system-lab-demo.service --no-pager
sudo journalctl -t system-lab-demo -b -n 5 --no-pager
```

Observed results: enabled, active (exited), exit status 0/SUCCESS and `Lab-service-started` in the journal. Stop/start was tested: inactive after stop, active after start. Following reboot, the unit ran again and generated a message in the new boot.

Verification printed CPUAccounting deprecation warnings for installed XFS units, not an error identifying this custom unit. Those vendor files were not modified; the warnings are recorded rather than described as repaired.

## Reboot and health checks

The final reboot verification covered fresh SSH login, Windows DNS lookup, UFW state/rules, automatic demo-service execution and retained file permissions.

The exported report was collected at **2026-10-30 07:58:55 UTC (14:58:55 Asia/Saigon)**. It shows `/` at 36% usage with 9.9 GB available, and no failed units. The user supplied empty output for `sudo dpkg --audit`, consistent with no reported incomplete package state.

The report combines command output without section labels or exit codes. An empty audit output is therefore supported by the separate transcript as well. It is not evidence of a successful current `apt update` or full patch compliance. The VM currently has no Internet route; do not add a fictitious gateway to make package downloads work.

## Evidence and limits

- [Exported report](evidence/ubuntu-report-2026-10-30.txt): original text with Machine ID, Boot ID, AF_VSOCK CID and service invocation ID removed. Original retained by the user outside the repo.
- [Supplementary record](evidence/ubuntu-validation-2026-10-30.md): explicitly marked excerpts and observations from user-provided screenshots/transcripts; not additional raw VM telemetry.
- Windows and Packet Tracer results in the original README remain historical validation, not a full rerun on this date.
- The VM console password-login problem was not conclusively diagnosed. SSH password login works; no console-login fix is claimed.
- AD membership, SMB access from Ubuntu, production hardening, a permanent web server, Internet routing, backup/restore and monitoring are outside this verified scope.

The basic Ubuntu scope is validated by the supplied evidence. Publishing additional screenshots or extending the lab can be done separately without changing what has actually been tested.
