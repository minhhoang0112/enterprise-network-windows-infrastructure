# Ubuntu supplementary validation — 2026-10-30

This is a curated record of user-supplied screenshots and terminal output from guided validation. It is not a raw automatic test run and does not imply the reviewer connected to the VM. Screenshot originals were supplied in the conversation and have not been exported into this repository.

The accompanying [exported report](ubuntu-report-2026-10-30.txt) covers host/network/firewall/service/health state. The checks below supply evidence missing from that report.

| Check | Supplied result | Evidence form |
|---|---|---|
| VMware placement | SERVER01 and Ubuntu use VMnet2 Host-only, subnet 192.168.30.0/24 | VMware settings screenshots and subsequent network output |
| Server connectivity | 4 packets transmitted, 4 received, 0% loss to 192.168.30.10 | Ubuntu ping screenshot |
| DHCP protection | .30 was not leased; exclusion .30–.30 added within scope .20–.100; CLIENT01 .20 reservation retained | DHCP Manager screenshots |
| SERVER01 DNS | SERVER01.corp.local -> 192.168.30.10 | resolvectl text, repeated after reboot |
| Ubuntu A record | UBUNTU01.corp.local -> 192.168.30.30 | DNS Manager screenshot and resolvectl text |
| Ubuntu PTR | 192.168.30.30 -> UBUNTU01.corp.local | resolvectl text |
| Member permissions | Create/read/append/copy/delete sample data succeeded | User-supplied terminal text |
| Nonmember permissions | Read and file creation denied | User-supplied terminal text |
| SSH and journal | New password login from 192.168.30.1, including after UFW/reboot | Screenshots and journal output |
| UFW control test | TCP 8088 False -> True -> False while listener running | Windows Test-NetConnection screenshots/text |
| Cleanup | Rule 8088 deleted; Python exited; no listener 8088 | UFW and ss screenshots/text |
| Service lifecycle | Stop -> inactive; start -> active; boot -> log message | Terminal text; final boot also in report |
| Health | dpkg --audit empty; 0 failed units; root 36% used | Terminal text and report |

## Selected transcript excerpts

DNS, collected after flushing the resolver cache:

```text
UBUNTU01.corp.local: 192.168.30.30 -- link: ens33
192.168.30.30: UBUNTU01.corp.local -- link: ens33
```

Local identities and permissions:

```text
labops:x:1005:
uid=1006(labmember) gid=1006(labmember) groups=1006(labmember),100(users),1005(labops)
uid=1007(labguest) gid=1007(labguest) groups=1007(labguest),100(users)
drwxr-xr-x 3 root root   4096 Oct 30 05:34 /srv/system-lab
drwxrws--- 2 root labops 4096 Oct 30 05:34 /srv/system-lab/team
-rw-rw---- 1 labmember labops 33 Oct 30 05:38 member.txt
```

Member output after append, repeated after reboot:

```text
Created by labmember
Second line
```

Nonmember read denial, repeated after reboot:

```text
cat: /srv/system-lab/team/member.txt: Permission denied
```

Nonmember file-creation denial:

```text
touch: setting times of '/srv/system-lab/team/guest-test.txt': Permission denied
```

Final listener check after Ctrl+C:

```text
sysadmin@UBUNTU01:~$ ss -lnt 'sport = :8088'
State          Recv-Q          Send-Q                   Local Address:Port                   Peer Address:Port
```

No failed units and no output between audit invocation and the next prompt were supplied. The final combined report does not label individual commands or preserve their exit codes, so it should be read together with this record.

## Remaining boundaries

These results establish the basic Ubuntu scope only. No AD join, permanent application deployment, backup recovery, monitoring, latest-update status, comprehensive Windows retest, or Packet Tracer retest is asserted. Console keyboard/password login behavior remains undiagnosed; SSH access was successful.
