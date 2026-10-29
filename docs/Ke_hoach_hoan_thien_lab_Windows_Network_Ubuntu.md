# HƯỚNG DẪN HOÀN THIỆN DỰ ÁN SYSTEM / NETWORK / UBUNTU

Tài liệu thực hành và nghiệm thu • Phiên bản 1.0 • Ngày 27/10/2026

Dành cho: Hoàng Công Minh. Mục tiêu: hoàn thiện lab cá nhân phục vụ portfolio Intern System / Network / IT Support, từ trạng thái đang có; có kiểm thử và bằng chứng trước khi nâng cấp.

## 1. Phạm vi, trạng thái và cách sử dụng

Tài liệu được xây dựng từ hồ sơ bàn giao, CV và repository local đã đọc. Những lệnh dưới đây là hướng dẫn để bạn thực hiện; chúng chưa được chạy trên VM của bạn. Không đánh dấu Pass chỉ vì tài liệu trước đây ghi đã hoàn thành.

Ba môi trường thuộc cùng hồ sơ dự án nhưng hoạt động độc lập:

| Môi trường | Vai trò | Trạng thái đầu vào |
| --- | --- | --- |
| Cisco Packet Tracer | VLAN, trunk, routing, Guest ACL, NAT/PAT | Có file .pkt, 4 cấu hình và ảnh; cần kiểm thử lại |
| VMware Windows | SERVER01 và CLIENT01, domain corp.local | Bạn xác nhận VM còn khởi động được; chức năng cần kiểm tra lại |
| VMware Ubuntu | UBUNTU01, quản trị Linux cơ bản | Báo cáo trước đây: NAT, DHCP, sysadmin, SSH đã kết nối; trạng thái hiện tại chưa xác minh |

Địa chỉ Windows: SERVER01 = 192.168.30.10/24; CLIENT01 reservation = 192.168.30.20; DNS nội bộ = 192.168.30.10; DHCP scope = .20–.100. Không đổi domain, IP hoặc cài lại VM chỉ để làm theo tài liệu này.

Ubuntu tiếp tục dùng NAT và DHCP nếu kiểm tra xác nhận cấu hình đó phù hợp. Không ép Ubuntu về IP cũ 192.168.30.30 hoặc DNS Windows. Không cài DHCP server trên Ubuntu trong phạm vi này. Không yêu cầu Ubuntu join domain.

### 1.1. Quy ước đọc lệnh

- Mỗi khối lệnh ghi rõ máy và quyền. Chạy từng nhóm nhỏ, đọc kết quả rồi mới sang nhóm tiếp theo.
- Lệnh trong khối Ubuntu chạy trên Ubuntu; lệnh Windows host chạy trên máy thật; PowerShell CLIENT01/SERVER01 chạy trong đúng VM.
- Các chuỗi IP_UBUNTU, IP_WINDOWS_HOST, TEN_INTERFACE, TEN_FILE.yaml là chỗ phải thay bằng thông tin đã xác minh. Không gõ nguyên các chuỗi này.
- Ubuntu phân biệt chữ hoa/thường. YAML dùng dấu cách, không dùng Tab. Không tự nối nhiều lệnh thành một dòng.
- Lệnh kiểm tra chạy trước. Lệnh cấu hình chỉ dùng khi kết quả cho thấy cần sửa, ngoại trừ bài thực hành tạo dữ liệu mẫu được ghi rõ.
- Khi kết quả khác dự kiến: ghi nguyên lệnh, output, máy đang dùng và bước hiện tại. Dừng phần phụ thuộc; không thử hàng loạt lệnh sửa ngẫu nhiên.

### 1.2. Pass, Fail và Blocked

Pass: đã chạy kiểm thử, kết quả phù hợp và có bằng chứng. Fail: đã chạy nhưng kết quả sai. Blocked: chưa thể kiểm tra vì phụ thuộc chưa đạt. Chưa làm: chưa thực hiện. N/A: không áp dụng, phải giải thích lý do.

Ghi kết quả sau mỗi chặng. File ảnh là bằng chứng bổ sung; output dạng text dễ chẩn đoán hơn. Không gửi mật khẩu, private key, token hoặc nội dung /etc/shadow.

### 1.3. Lộ trình theo phiên thực hành

| Phiên | Công việc | VM cần bật | Điều kiện chuyển tiếp |
| --- | --- | --- | --- |
| 1 | Chuẩn bị và kiểm tra server Windows | SERVER01 | AD, DNS, DHCP được kiểm tra |
| 2 | Kiểm tra client, GPO, file permissions | SERVER01 + CLIENT01 | Các test Windows đạt hoặc đã giải thích lỗi |
| 3 | Kiểm tra mô hình mạng | Không cần VM; mở Packet Tracer | VLAN/routing/ACL/NAT có bằng chứng |
| 4 | Ubuntu inventory, NAT/DHCP/DNS/Internet | UBUNTU01 | Mạng và apt update hoạt động |
| 5 | SSH, package và filesystem | UBUNTU01 | Kết nối lại được, dữ liệu lab tạo đúng |
| 6 | User/group, permissions, service/log | UBUNTU01 | Kiểm thử cho phép và từ chối đều đạt |
| 7 | Firewall, reboot, thu bằng chứng | UBUNTU01 | SSH vẫn vào được sau firewall và reboot |
| 8 | Nghiệm thu, tài liệu, chỉnh CV | Chỉ bật khi cần kiểm tra lại | Checklist và báo cáo tổng hợp đầy đủ |

Mỗi phiên có thể chia nhỏ. Đây không phải hạn hoàn thành; không cần chạy ba VM cùng lúc. Backup/restore nâng cao, automation, monitoring và tích hợp AD–Linux dành cho giai đoạn nâng cấp.

## 2. Chuẩn bị và lưu bằng chứng — P01 đến P04

### P01. Kiểm tra VM và tài nguyên

1. Trong VMware, ghi tên VM, vị trí file .vmx, RAM, CPU, ổ đĩa, network adapter và VMnet đang chọn của từng VM.
2. Ghi subnet và loại mạng của VMnet Windows hiện có. SERVER01 và CLIENT01 phải nằm trên cùng mạng ảo của lab. Không đổi sang NAT theo Ubuntu.
3. Với Ubuntu, ghi NAT hay Custom VMnet; nếu Custom, kiểm tra VMnet đó có thực sự là NAT. Chụp phần Network Adapter.
4. Kiểm tra dung lượng trống ổ host chứa VM. Không tự tăng RAM/CPU hoặc tạo VM mới khi chưa cần.

Pass: biết mỗi VM dùng mạng nào; hai Windows VM cùng mạng; xác định rõ Ubuntu riêng.

### P02. Điểm khôi phục trước thay đổi

Nếu VMware hỗ trợ và đủ dung lượng, tắt hẳn VM rồi tạo snapshot có tên pre-verification-YYYYMMDD. Snapshot chỉ là điểm quay lui thao tác, không thay thế backup ngoài VM. Nếu chọn copy VM, chỉ copy sau khi shutdown và VMware đã đóng VM; không copy đĩa đang chạy.

Không bắt buộc tạo snapshot nếu thiếu dung lượng. Khi đó lưu cấu hình text và chỉ sửa từng việc nhỏ. Không tùy tiện revert riêng domain controller sau khi client đã thay đổi; nếu cần quay lui môi trường domain, gửi tình huống để xem xét trước.

### P03. Thư mục bằng chứng

Trên Windows host, tạo một thư mục ngoài repository nếu chỉ lưu log thô. Ví dụ PowerShell trên host:

```powershell
$EvidenceRoot = 'D:\Lab-Evidence-System'
New-Item -ItemType Directory -Force -Path $EvidenceRoot
New-Item -ItemType Directory -Force -Path "$EvidenceRoot\windows","$EvidenceRoot\network","$EvidenceRoot\ubuntu"
```

Đặt tên file theo mã test: W03-dns.txt, W07-hr-denied.png, U03-network.txt. Giữ bản gốc; khi công khai GitHub, xem lại thông tin cá nhân trước. Không cần công khai toàn bộ log.

### P04. Bảng thông tin ban đầu

Ghi tên VM, OS/version, hostname, IP/prefix, gateway, DNS, network mode, username quản trị, ngày kiểm tra. Mật khẩu để trống. Các ô chưa biết ghi “Chưa xác minh”, không điền bằng thông tin cũ.

## 3. Kiểm tra Windows Server — W01 đến W04

### W01. Máy chủ, IP và dịch vụ

Bật SERVER01 trước, đăng nhập bằng tài khoản quản trị. Mở Windows PowerShell bằng Run as administrator. Dùng Windows PowerShell tích hợp sẵn để tránh khác biệt module.

```powershell
hostname
Get-Date
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version
Get-NetIPConfiguration
Get-Service NTDS,DNS,DHCPServer,Netlogon,DFSR
```

Mong đợi: SERVER01, Windows Server 2022, IPv4 192.168.30.10/24 và DNS trỏ về DNS nội bộ. Những dịch vụ đã cài tương ứng phải hoạt động. Không tự start một dịch vụ chưa cài hoặc sửa role chỉ vì tên hiển thị khác.

Gateway Windows lab cô lập có thể trống. Không có Internet trong lab này không đồng nghĩa AD/DNS/DHCP bị lỗi. Kiểm tra giờ server và client; lệch giờ đáng kể có thể ảnh hưởng xác thực.

Nếu IP khác: chụp cấu hình adapter và VMware trước khi chỉnh. Nếu service Stopped: lấy Event Viewer và lỗi khởi động, không cài lại AD DS.

### W02. AD, OU, user/group và chia sẻ domain

Trên SERVER01, PowerShell Administrator:

```powershell
Get-ADDomain | Select-Object DNSRoot,NetBIOSName,DomainMode
Get-ADOrganizationalUnit -Filter * | Select-Object Name,DistinguishedName
Get-ADGroupMember GG_IT | Select-Object Name,SamAccountName
Get-ADGroupMember GG_HR | Select-Object Name,SamAccountName
Get-SmbShare -Name SYSVOL,NETLOGON
dcdiag /test:Advertising /test:Services /test:NetLogons
```

Mong đợi: corp.local; OU CORP và Computers, Groups, Servers, Users; trong Users có IT, HR, Accounting, Sales. Kiểm tra GUI Active Directory Users and Computers để xác nhận CLIENT01 thuộc CORP\Computers và các user thuộc OU phòng ban tương ứng.

GG_IT có an.nguyen; các nhóm khác khớp hồ sơ thực tế. Kiểm tra thêm GG_Accounting, GG_Sales nếu cần. Không suy ra NetBIOS name chỉ từ DNS domain: ghi giá trị thực tế; tài liệu trước đây dùng CORP.

Pass: cấu trúc và membership đúng, SYSVOL/NETLOGON hiện diện, các test chọn ở trên thành công. Nếu dcdiag fail, lưu đầy đủ output, không bỏ qua bằng cách chỉ chụp dòng Pass.

### W03. DNS forward, reverse và bản ghi domain

Trên SERVER01:

```powershell
Resolve-DnsName SERVER01.corp.local -Server 192.168.30.10
Resolve-DnsName 192.168.30.10 -Type PTR -Server 192.168.30.10
Resolve-DnsName _ldap._tcp.dc._msdcs.corp.local -Type SRV -Server 192.168.30.10
Get-DnsServerZone
```

Mong đợi: A record về 192.168.30.10; PTR về SERVER01.corp.local; SRV tìm thấy domain controller tương ứng. Dùng DNS Manager để kiểm tra forward zone và reverse zone nếu lỗi.

Không dùng việc phân giải google.com làm tiêu chí bắt buộc cho Windows lab cô lập. Không đổi DNS client sang DNS công cộng để sửa lỗi join domain. Server: Unknown trong nslookup cần đối chiếu PTR; nếu truy vấn vẫn trả kết quả thì không thể chỉ từ dòng Unknown kết luận toàn bộ DNS hỏng.

### W04. DHCP scope, option và reservation

Trên SERVER01, PowerShell Administrator:

```powershell
Get-DhcpServerInDC
Get-DhcpServerv4Scope
Get-DhcpServerv4OptionValue -ScopeId 192.168.30.0
Get-DhcpServerv4Reservation -ScopeId 192.168.30.0
Get-DhcpServerv4Lease -ScopeId 192.168.30.0
```

Mong đợi: DHCP server được authorize trong AD; scope Active, range .20–.100; option 006 = 192.168.30.10, option 015 = corp.local; reservation .20 thuộc đúng MAC/ClientId của CLIENT01. Nếu scope thừa hưởng option cấp server, xem thêm Get-DhcpServerv4OptionValue và kiểm tra DHCP GUI để xác định giá trị thực sự áp dụng.

Option 003 trống phù hợp với lab Windows không có router. Không thêm 192.168.30.1 chỉ vì Packet Tracer dùng gateway này. Nếu client nhận DHCP từ nguồn khác, kiểm tra VMware DHCP trên VMnet Windows và dịch vụ DHCP khác; chỉ điều chỉnh đúng mạng ảo này, không tắt DHCP NAT đang phục vụ Ubuntu.

## 4. Kiểm tra Windows client và quyền truy cập — W05 đến W08

### W05. DHCP và domain trust

Bật CLIENT01 khi SERVER01 đã sẵn sàng. Đăng nhập tài khoản quản trị lab trên CLIENT01 và mở PowerShell Administrator:

```powershell
hostname
ipconfig /all
Get-CimInstance Win32_ComputerSystem | Select-Object Name,Domain,PartOfDomain
Test-ComputerSecureChannel -Verbose
Resolve-DnsName SERVER01.corp.local -Server 192.168.30.10
Test-NetConnection SERVER01.corp.local -Port 445
```

Pass: CLIENT01, PartOfDomain=True, domain corp.local, DHCP Enabled=Yes, IP .20, DHCP Server và DNS = .10, secure channel=True, TCP 445=True. Test-ComputerSecureChannel dùng ở member client, không lấy kết quả trên domain controller làm tiêu chí.

Nếu còn static IP: ghi adapter name rồi vào IPv4 Properties trên CLIENT01, chọn Obtain an IP address automatically và Obtain DNS server address automatically. Đây là thay đổi cấu hình, chỉ làm sau khi W04 đạt và đang có quyền vào VM console. Chạy ipconfig /renew rồi kiểm tra lại; không cần release trước. Không thực hiện thao tác này trên SERVER01.

Nếu 169.254.x.x: chưa nhận DHCP; kiểm tra đúng VMnet, scope Active, service DHCP và nguồn DHCP. Nếu secure channel lỗi: kiểm tra DNS và thời gian trước, không unjoin/rejoin domain ngay.

### W06. Domain login, GPO người dùng và máy tính

Đăng xuất CLIENT01, đăng nhập CORP\an.nguyen. Mở File Explorer để kiểm tra ổ I: và P:. Nếu shell được phép, chạy ở phiên chính user đó:

```powershell
whoami
$env:LOGONSERVER
gpresult /r /scope user
```

Mong đợi: corp\an.nguyen và logon server SERVER01; GPO-USER-BASELINE có trong Applied Group Policy Objects. Đăng nhập cache một mình chưa đủ chứng minh xác thực online; kết hợp W05 và truy cập share hiện tại.

Nếu CMD bị policy chặn, đó có thể chính là kết quả cần kiểm thử. Không tắt policy để lấy log. Dùng Group Policy Results Wizard trên SERVER01, chọn CLIENT01 và đúng user, hoặc ghi nhận giới hạn và dùng bằng chứng khác. Nếu wizard bị chặn kết nối quản trị, gửi lỗi; không mở firewall rộng để ép chạy.

Tại CLIENT01, mở PowerShell Administrator bằng tài khoản quản trị để kiểm tra computer scope:

```powershell
gpresult /r /scope computer
```

Lưu ý: shell nâng quyền bằng tài khoản khác có thể cho user scope của tài khoản quản trị, không phải an.nguyen. Không dùng báo cáo đó chứng minh policy user an.nguyen. Computer scope mong đợi GPO-CLIENT-BASELINE; “Access Denied” cần kiểm tra quyền chạy.

Kiểm thử trực tiếp dưới user thường: mở Control Panel, Command Prompt và Registry Editor. Ghi thông báo chặn, không chỉ kết luận từ tên GPO. Nếu policy chưa áp dụng, kiểm tra OU placement, GPO link, Security Filtering, user membership và đăng xuất/đăng nhập lại. Có thể gpupdate /force nếu shell cho phép; không dùng cập nhật policy để thay thế kiểm tra nguyên nhân.

### W07. File Server và ma trận quyền thực tế

Trên SERVER01, PowerShell Administrator, chỉ đọc cấu hình:

```powershell
Get-SmbShare -Name CORP-DATA
Get-SmbShareAccess -Name CORP-DATA
icacls D:\CORP-DATA
icacls D:\CORP-DATA\IT
icacls D:\CORP-DATA\HR
```

Đối chiếu cả share permissions và NTFS permissions: truy cập SMB chịu đồng thời hai lớp. Không chụp mỗi NTFS rồi kết luận truy cập mạng đúng. Kiểm tra inherited permissions; không cấp Everyone Full Control trên toàn cây để sửa nhanh và không thêm Deny khi chưa hiểu ảnh hưởng group membership.

Trên CLIENT01, dưới CORP\an.nguyen, dùng File Explorer truy cập đúng UNC; không dùng tài khoản admin vì sẽ làm sai ý nghĩa bài test:

| Test | Thao tác | Mong đợi |
| --- | --- | --- |
| IT được phép | Mở \\SERVER01\CORP-DATA\IT; tạo evidence-it.txt, sửa nội dung, đổi tên và xóa file vừa tạo | Thành công với quyền Modify |
| Public | Mở \\SERVER01\CORP-DATA\Public; thử thao tác theo quyền bạn định nghĩa | Kết quả phải khớp quyền Public được ghi rõ |
| HR bị chặn | Gõ trực tiếp \\SERVER01\CORP-DATA\HR | Access Denied khi truy cập nội dung theo thiết kế |
| Accounting/Sales bị chặn | Gõ trực tiếp UNC từng thư mục | Không đọc/ghi dữ liệu phòng ban khác |
| Mapped drive | Mở I: và P: | Đúng đường dẫn, truy cập phù hợp |

Public chưa được tài liệu cũ xác định rõ Read hay Modify. Trước tiên xem cấu hình rồi ghi quyết định; để nghiệm thu quyền đọc/ghi phải có thiết kế cụ thể. Khuyến nghị bài lab chọn CORP users được Modify trong Public, quản trị viên và SYSTEM giữ quyền quản trị; đây là lựa chọn cần cấu hình nếu hiện trạng khác, không phải điều đã xác nhận.

Thấy tên thư mục HR ở thư mục gốc không nhất thiết là lỗi phân quyền nếu chưa bật Access-Based Enumeration. Tiêu chí chính là không mở/đọc/ghi nội dung trái phép bằng UNC trực tiếp. Ẩn ổ đĩa hoặc không map ổ HR không chứng minh NTFS đã chặn.

Nên đăng xuất và test thêm CORP\lan.tran: HR được phép, IT bị chặn, H:/P: phù hợp. Dùng file mẫu, không xóa dữ liệu cũ. Không lưu credential admin trong phiên user thường.

### W08. Chốt Windows

Lưu ảnh DHCP, DNS, OU/GPO, drive mapping và hai chiều truy cập cho phép/từ chối. Ghi ba lỗi troubleshooting đã tái kiểm tra nếu gặp: client static, PTR thiếu, gpresult thiếu quyền. Nếu không gặp lại, chỉ ghi là bài học lịch sử, không dựng lỗi trên AD đang hoạt động.

Pass Windows khi W01–W07 đạt và mọi cảnh báo còn lại có giải thích. Đừng đánh dấu Pass toàn bộ vì đăng nhập được một lần.

## 5. Kiểm tra Cisco Packet Tracer — N01 đến N05

### N01. Mở bản lab đúng và lưu bản sao

Mở packet-tracer/Enterprise_Network_Lab.pkt. Save As một bản kiểm thử riêng trước khi sửa. Ghi phiên bản Packet Tracer; nếu file mở lỗi, chụp lỗi phiên bản thay vì xây lại ngay. Đối chiếu R1-EDGE, SW-CORE, SW-USERS, SW-SERVER và mạng ISP mô phỏng.

### N02. VLAN, trunk và routing

Chạy tại CLI switch tương ứng, vào enable khi cần:

```text
show vlan brief
show interfaces trunk
show ip interface brief
```

Mong đợi VLAN 10/20/30/40/99 tồn tại ở switch cần dùng; access port đúng VLAN. Trunk router–core cho 10,20,30,40,99; core–users cho 10,20,40,99; core–server cho 30,99. Cấu hình text hiện có không thay thế việc xác nhận VLAN database trong file .pkt.

Trên R1-EDGE:

```text
show ip interface brief
show ip route
show running-config
```

Mong đợi G0/0 và subinterface hoạt động; gateway mỗi VLAN là 192.168.VLAN.1, riêng VLAN99 = 192.168.99.1; có các route connected. Ghi IP thực tế của ít nhất một endpoint trong VLAN10, VLAN20, VLAN30, VLAN40. Không dùng IP VM Windows làm đích ping trong Packet Tracer.

### N03. Kiểm thử liên VLAN và Guest isolation

Từ PC Admin/Staff, ping gateway và endpoint nội bộ được phép. Lần đầu có thể timeout do ARP; thử lại rồi ghi kết quả. Từ Guest ping gateway VLAN40, sau đó ping endpoint VLAN10/20/30/99 và đích ngoài mô phỏng.

Trên router:

```text
show access-lists
show ip interface GigabitEthernet0/0.40
```

Pass: ACL GUEST-ISOLATION gắn inbound VLAN40; Guest bị chặn tới mạng nội bộ theo thiết kế; Admin/Staff không bị chặn ngoài dự kiến. Dùng deny hit counter trước/sau cùng kiểm thử đích đang hoạt động để phân biệt ACL chặn với máy đích mất kết nối. Ngoại lệ DHCP UDP 68→67 là chủ ý trong cấu hình, không phải cô lập tuyệt đối mọi gói.

### N04. NAT/PAT và mạng ngoài mô phỏng

Xác định IP đích công cộng trong file .pkt, kiểm tra gateway/default route của ISP và đích trước. Từ endpoint nội bộ gửi traffic ra đích này rồi xem router:

```text
show ip nat translations
show ip nat statistics
show ip route
```

Mong đợi inside local 192.168.x.x được dịch thành 203.0.113.1; default route đi 203.0.113.2. Nếu bảng translation trống, tạo traffic mới rồi xem ngay. VLAN99 không nằm trong NAT ACL hiện có nên không yêu cầu nó truy cập ngoài như các VLAN10/20/30/40.

### N05. Giới hạn DHCP relay và chốt Network

Cấu hình router có ip helper-address 192.168.30.10 ở một số VLAN. Đây chỉ là cấu hình trong mô phỏng, không chứng minh DHCP VMware phục vụ Packet Tracer. Nếu Packet Tracer có DHCP server mô phỏng, ghi rõ thiết bị và scope của nó; nếu endpoint static, ghi rõ static. DHCP liên VLAN chưa được kiểm thử thì đánh dấu chưa kiểm thử, không nâng thành thành tích.

Lưu ảnh VLAN/trunk, route, Guest bị chặn, NAT translation và bản cấu hình nếu đã thay đổi. Nếu sửa cấu hình thiết bị, copy running-config startup-config rồi lưu file .pkt. Không ghi đè bản chính khi chưa test lại.

## 6. Ubuntu: kiểm kê và mạng — U01 đến U04

### U01. Xác định hiện trạng, không sửa trước

Tắt các VM Windows nếu không cần nữa. Bật UBUNTU01, dùng VMware console đăng nhập sysadmin. Chạy từng nhóm:

```bash
whoami
hostnamectl
cat /etc/os-release
uname -r
date -Is
timedatectl status
```

```bash
ip -br link
ip -br -4 address
ip route
hostname -I
resolvectl status
```

```bash
df -hT
df -ih
free -h
lsblk -f
systemctl --failed --no-pager
```

Mục đích: biết Ubuntu phiên bản nào, hostname gì, interface thực tế, IPv4/default gateway/DNS, dung lượng và unit lỗi. hostname -I có thể trả nhiều IP; không mặc định IP đầu tiên là interface VMware.

Mong đợi: user sysadmin có thể sudo; hostname UBUNTU01 nếu đã đổi; interface Ethernet có IPv4 và default route ở mạng NAT. Interface có thể là ens33, ens160 hoặc tên khác: dùng tên thật. Nếu resolvectl không có, ghi lỗi và xem ls -l /etc/resolv.conf cùng cat /etc/resolv.conf. Không sửa /etc/resolv.conf để chữa DNS vội.

Nếu hostname vẫn ubuntu-server, việc đổi là tùy chọn để khớp tài liệu. Chỉ khi muốn chuẩn hóa mới chạy sudo hostnamectl set-hostname UBUNTU01, sau đó xem /etc/hosts và chỉnh dòng hostname local cũ cho phù hợp nếu có; giữ localhost. Không đổi hostname khi chưa ghi lại hiện trạng.

Lưu U01-os.txt, U01-network.txt, U01-resources.txt. Nếu Ubuntu release hết hỗ trợ hoặc apt báo repository không còn hợp lệ, gửi VERSION_ID và lỗi trước; không tự dùng do-release-upgrade hoặc đổi mirror sang bản Ubuntu khác.

### U02. Kiểm tra đúng NAT và địa chỉ DHCP

Trong VMware > VM Settings > Network Adapter: kiểm tra Connected và Connect at power on; xác nhận NAT hoặc Custom trỏ đúng VMnet NAT. Ghi cấu hình Virtual Network Editor nếu mở được: subnet, NAT gateway và DHCP range thực tế. Không mặc định NAT luôn là 192.168.30.0/24 hoặc gateway .1/.2.

Trên Ubuntu, thay TEN_INTERFACE bằng tên đã thấy, ví dụ ens33:

```bash
ip -4 addr show dev TEN_INTERFACE
ip route
networkctl status TEN_INTERFACE --no-pager
```

networkctl chủ yếu dùng khi systemd-networkd quản lý interface; nếu hiện unmanaged, kiểm tra renderer ở U03 và có thể dùng nmcli device show nếu NetworkManager đang quản lý. Unmanaged trong networkctl chưa đủ kết luận mất mạng.

Pass: interface có IPv4 đúng mạng NAT, default route đi qua gateway của mạng đó, không còn DNS cũ .10 ngoài ý muốn. IP DHCP có thể đổi sau reboot. Nếu không có IP: kiểm tra adapter, NAT VMnet và VMware DHCP trước; chưa sửa hàng loạt file trong Ubuntu.

### U03. Đọc Netplan và chỉ sửa khi cấu hình hiện tại sai

Trên Ubuntu console:

```bash
ls -la /etc/netplan
sudo cat /etc/netplan/*.yaml
sudo netplan get
systemctl is-active systemd-networkd
systemctl is-active NetworkManager
```

Nếu netplan get không được phiên bản hỗ trợ, đọc các YAML và ghi thông báo; không cài lại networking vì một lệnh thiếu. Netplan có thể hợp nhất nhiều YAML; đọc toàn bộ trước. Không tạo file 99 mới để che cấu hình cũ mà chưa biết cấu hình hợp nhất.

Nếu hiện trạng đã DHCP, đúng NAT, mạng hoạt động: bỏ qua chỉnh sửa, chuyển U04. Nếu còn static IP cũ hoặc DNS 192.168.30.10 và cần sửa, thực hiện tại VMware console, không chỉ qua SSH.

Sao lưu trước khi sửa; lệnh dưới tạo thư mục riêng mỗi lần chạy:

```bash
NETPLAN_BACKUP="$HOME/netplan-before-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$NETPLAN_BACKUP"
sudo cp -a /etc/netplan/. "$NETPLAN_BACKUP/"
printf '%s\n' "$NETPLAN_BACKUP"
```

Ghi đường dẫn backup vào báo cáo. Xác định đúng file đang quản lý interface; ví dụ TEN_FILE.yaml phải thay bằng tên thật:

```bash
sudo nano /etc/netplan/TEN_FILE.yaml
```

Ví dụ tối thiểu CHỈ dành cho VM một Ethernet do networkd quản lý, sau khi đã đối chiếu file thực tế và đổi ens33 nếu cần:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:
      dhcp4: true
```

Không thay toàn bộ file bằng mẫu nếu có nhiều interface, renderer khác, match/macaddress/set-name hoặc cấu hình cần giữ. Nếu có match/set-name, kiểm tra MAC bằng ip link rồi giữ cấu trúc phù hợp. Trong stanza interface đang sửa, loại bỏ addresses/routes/nameservers static cũ nếu chúng không còn thuộc thiết kế NAT/DHCP; dhcp4: true một mình không tự xóa cấu hình static ở nơi khác.

Nếu file ghi do cloud-init sinh ra, dừng và gửi nội dung đã che thông tin nhạy cảm để xác định nguồn quản lý; sửa file sinh tự động có thể mất sau reboot. Không tự vô hiệu cloud-init cả hệ thống.

Sau khi chỉnh đúng file:

```bash
sudo chmod 600 /etc/netplan/TEN_FILE.yaml
sudo netplan generate
sudo netplan try --timeout 120
```

generate thành công thường không có output. Nếu báo YAML error, sửa đúng dòng/cột trước; chưa chạy apply. Khi try đang chờ xác nhận, dùng console/phiên khác xem IP, route và thử kết nối; chỉ xác nhận khi cấu hình tốt. Không xác nhận thì công cụ được thiết kế để hoàn tác sau timeout, nhưng vẫn phải kiểm tra thực tế vì rollback có giới hạn theo phiên bản/tình huống.

Nếu mất mạng: ở VMware console xem ip -br -4 address và ip route; mở lại YAML, đối chiếu backup rồi phục hồi đúng file đã sửa. Không copy đè toàn bộ các file khi chưa biết file nào thay đổi. Chạy generate rồi try lại tại console. Không chạy netplan apply liên tục để đoán.

Pass: generate không lỗi, có IP/default route và U04 đạt; sau reboot U12 vẫn giữ đúng chế độ. Mẫu Netplan này không phải bằng chứng cấu hình thực tế của bạn.

### U04. Tách lỗi gateway, Internet, DNS và repository

Trên Ubuntu:

```bash
ip route
ping -c 4 IP_GATEWAY_NAT
ping -c 4 1.1.1.1
getent ahostsv4 archive.ubuntu.com
getent ahostsv4 security.ubuntu.com
resolvectl status
sudo apt update
```

Thay IP_GATEWAY_NAT bằng default gateway thật ở ip route. Ping có thể bị chặn ICMP; ping fail một mình không kết luận không Internet. getent kiểm tra phân giải; apt update kiểm tra đường tới repository đang cấu hình. Máy dùng mirror khác thì kiểm tra thêm hostname mirror trong lỗi apt.

| Triệu chứng | Kiểm tra tiếp | Cách xử lý có căn cứ |
| --- | --- | --- |
| Không IPv4 | Adapter, interface, VMware DHCP, YAML | Sửa đúng lớp bị lỗi; không đặt static ngẫu nhiên |
| Có IPv4 nhưng không default route | NAT mode, DHCP, routes static còn sót | Đối chiếu U02/U03 |
| IP ngoài truy cập được, hostname không phân giải | resolvectl, DNS DHCP, Netplan nameservers | Sửa nguồn cấp DNS; không ghi đè resolv.conf |
| DNS được nhưng apt timeout | Mirror, NAT, proxy/VPN host, TCP outbound | Ghi URL lỗi, thử lại sau khi xác định mạng |
| Certificate/not valid yet | date, timedatectl, giờ host | Đồng bộ giờ; không tắt kiểm tra TLS |
| Lock apt/dpkg | Package updater khác đang chạy | Chờ tiến trình hợp lệ; không xóa lock file |
| Repository 404/Release missing | VERSION_ID và repository suites | Gửi lỗi, không trộn repository khác release |

Muốn xem repository thực tế:

```bash
ls -l /etc/apt/sources.list /etc/apt/sources.list.d
grep -R -n -E '^(deb |URIs:|Suites:)' /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null
```

Ubuntu mới có thể dùng .sources thay vì chỉ sources.list. Khi chia sẻ output, che credential nếu repository/proxy riêng có chứa tài khoản. DNS 127.0.0.53 trong resolv.conf có thể là stub hợp lệ của systemd-resolved; xem upstream bằng resolvectl, không tự thay stub.

Pass: hostname repository phân giải được và apt update kết thúc không có lỗi fetch/index làm dùng metadata cũ. “All packages are up to date” không bắt buộc; có package mới để nâng cấp vẫn Pass. Warning về nguồn tải phải đọc và phân loại, không bỏ qua toàn bộ.

ĐIỂM GỬI KẾT QUẢ 1: gửi U01–U04 trước khi sửa SSH/firewall nếu bất kỳ bước nào lỗi.

## 7. Ubuntu: SSH và quản lý package — U05 đến U06

### U05. Kiểm tra SSH trước, cài nếu thực sự thiếu

Tại Ubuntu console:

```bash
dpkg-query -W openssh-server
systemctl status ssh.service ssh.socket --no-pager
sudo ss -lntp
sudo /usr/sbin/sshd -t
```

Mong đợi openssh-server được cài, có listener SSH trên port thực tế (thường 22), cấu hình sshd hợp lệ. Ubuntu có thể dùng socket activation: ssh.socket active là bình thường, ssh.service có thể chưa active trước khi có kết nối. Không ép chuyển service/socket chỉ để có một chữ active giống ảnh mẫu.

Nếu package chưa cài và U04 đạt:

```bash
sudo apt install openssh-server
```

Nếu đã cài nhưng chưa có listener, xem status và journal trước. Với hệ thống dùng service truyền thống, có thể bật bằng sudo systemctl enable --now ssh.service. Nếu socket activation đang được cấu hình, quản lý ssh.socket tương ứng; không bật/tắt cả hai theo phỏng đoán. Gửi output nếu không rõ.

Kiểm tra cấu hình hiệu lực và log:

```bash
sudo /usr/sbin/sshd -T | grep -E '^(port|permitrootlogin|passwordauthentication|pubkeyauthentication) '
sudo journalctl -u ssh.service -u ssh.socket -b -n 80 --no-pager
sudo ufw status verbose
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Lệnh ssh-keygen ở đây chỉ xem fingerprint public host key có sẵn, không tạo lại host key. Nếu file không tồn tại, xem các file *.pub trong /etc/ssh và dùng key đang có. Không gửi private key cùng thư mục.

Trên Windows HOST, PowerShell thường, thay IP_UBUNTU bằng IPv4 thật:

```powershell
Test-NetConnection IP_UBUNTU -Port 22
ssh sysadmin@IP_UBUNTU
```

Nếu SSH thực sự dùng port khác, thay cả Test-NetConnection và dùng ssh -p PORT. Đối chiếu fingerprint lần đầu với console trước khi chấp nhận. Mật khẩu khi gõ thường không hiện ký tự. Sau khi vào Ubuntu qua SSH:

```bash
whoami
hostname
ip -br -4 address
exit
```

Mở kết nối SSH thứ hai để xác nhận đăng nhập mới hoạt động. Nếu hostname Windows không phân giải UBUNTU01, kết nối bằng IP; chưa triển khai DNS cho tên đó không phải lỗi SSH.

| Lỗi SSH | Ý nghĩa thường gặp | Kiểm tra |
| --- | --- | --- |
| Timeout | Sai IP/route hoặc firewall chặn | IP console, VMnet host, UFW, TCP port |
| Connection refused | Không có listener hoặc bị reject | ss, ssh.service/socket, đúng port |
| Permission denied | Sai user/password hoặc phương thức auth | whoami, account status, sshd config, journal |
| Host identification changed | IP DHCP có thể thuộc VM khác hoặc host key đã đổi | Đối chiếu fingerprint tại console trước khi thay known_hosts |

Không xóa toàn bộ known_hosts hoặc tắt StrictHostKeyChecking. Không bật root login để sửa lỗi sysadmin. Nếu thiếu sudo, dùng tài khoản quản trị hợp lệ sẵn có; không thay quyền /etc/sudoers tùy tiện.

Pass: Windows host mở được phiên SSH mới và đúng user/hostname. Có log cùng listener chứng minh dịch vụ; không chỉ chụp terminal cũ còn mở.

### U06. Package, dung lượng và cập nhật

Trên Ubuntu, sau U04 đạt:

```bash
sudo apt update
apt list --upgradable
df -h /
sudo apt upgrade --simulate
```

Đọc số package, dung lượng tải và thay đổi dự kiến. Nếu đủ dung lượng và không có vấn đề cần làm rõ, thực hiện:

```bash
sudo apt upgrade
```

Đọc prompt thay vì thêm -y. Nếu hỏi thay file cấu hình đã chỉnh, dừng và gửi màn hình khi không chắc; không chọn ghi đè tất cả. Không dùng full-upgrade, autoremove hoặc nâng release trong quy trình cơ bản này. Không ngắt điện/tắt VM khi apt/dpkg đang chạy.

Kiểm tra sau cập nhật:

```bash
sudo dpkg --audit
test -f /var/run/reboot-required && cat /var/run/reboot-required
systemctl --failed --no-pager
```

dpkg --audit không có output thường nghĩa không phát hiện package cài dở. Lệnh test không in gì khi không có yêu cầu reboot là bình thường. Nếu có yêu cầu reboot, để chặng U12 sau khi đã lưu dữ liệu và có console.

Nếu package bị giữ lại/phased updates, ghi rõ danh sách; không ép cập nhật chỉ để danh sách trống. Với package bị lỗi cài dở, gửi output audit và lỗi apt trước khi chạy các lệnh repair. Pass: package manager hoạt động, không có lỗi cài đặt chưa xử lý; việc hoãn package có lý do được ghi lại.

## 8. Ubuntu: filesystem, user/group và phân quyền — U07 đến U08

### U07. Thao tác filesystem trong thư mục lab riêng

Đăng nhập sysadmin, không dùng sudo cho bài này:

```bash
mkdir -p ~/system-lab/files ~/system-lab/evidence
cd ~/system-lab/files
pwd
printf 'Ubuntu lab - first file\n' > note.txt
cat note.txt
cp -i note.txt note-copy.txt
mv -i note-copy.txt note-renamed.txt
ls -lah
stat note.txt
```

Nếu file đã tồn tại từ lần trước, xem nội dung trước khi chấp nhận ghi đè. Dùng nano note.txt để thêm một dòng; Ctrl+O, Enter để lưu, Ctrl+X để thoát. Dùng less note.txt, nhấn q để thoát. Thực hành đường dẫn tuyệt đối bằng ls "$HOME/system-lab/files" và đường dẫn tương đối bằng ls .

Xóa đúng file copy vừa tạo, có xác nhận:

```bash
rm -i ~/system-lab/files/note-renamed.txt
ls -lah ~/system-lab/files
```

Pass: giải thích được pwd, đường dẫn tuyệt đối/tương đối, cp/mv/rm và quyền hiện ở ls -l; note.txt gốc còn nguyên. Không thực hành rm -rf trên thư mục hệ thống.

### U08. Nhóm labops, thành viên được phép và người ngoài bị chặn

Mục tiêu: tạo /srv/system-lab/team cho một nhóm được đọc/ghi; user ngoài nhóm không đọc/ghi được. Đây là bài thực hành mới, chưa phải trạng thái đã có trên VM. Dùng tên lab riêng để không đụng user sysadmin.

Trước khi tạo, kiểm tra tên đã tồn tại chưa:

```bash
getent group labops
id labmember
id labguest
ls -ld /srv/system-lab /srv/system-lab/team
```

Nếu báo không tồn tại là bình thường trong lần đầu. Nếu đã có, xem membership/dữ liệu và tái sử dụng khi đúng bài lab; không chạy tạo lại hoặc đổi quyền dữ liệu có sẵn mà chưa xem.

Chỉ với các đối tượng chưa tồn tại, tạo lần lượt:

```bash
sudo groupadd labops
sudo adduser labmember
sudo adduser labguest
sudo usermod -aG labops labmember
```

Chọn mật khẩu riêng, không lưu vào báo cáo. Không thêm các user thực hành vào sudo. Cờ -aG là append supplementary group; thiếu -a có thể thay mất các nhóm bổ sung khác.

Tạo thư mục lab và gán quyền sau khi chắc chắn đúng đường dẫn:

```bash
sudo mkdir -p /srv/system-lab/team
sudo chown root:root /srv/system-lab
sudo chmod 755 /srv/system-lab
sudo chown root:labops /srv/system-lab/team
sudo chmod 2770 /srv/system-lab/team
id labmember
id labguest
ls -ld /srv/system-lab /srv/system-lab/team
```

Giải thích: 2770 = setgid + owner rwx + group rwx + other không quyền. Setgid làm đối tượng mới kế thừa group của thư mục; không tự bảo đảm mọi file mới đều group-writable, vì còn phụ thuộc mode/umask. Parent 755 cho phép traverse tới team, quyền của team mới quyết định truy cập nội dung. Không dùng chmod -R 777.

Test bằng danh tính thực sự khác qua sudo -u từ tài khoản sysadmin có quyền sudo. Các shell sau không có quyền root chỉ vì bạn chạy sudo; chúng chạy bằng user được chỉ định.

1. labmember tạo và đọc file:

```bash
sudo -u labmember sh -c 'umask 007; printf "created by labmember\n" > /srv/system-lab/team/member.txt'
sudo -u labmember cat /srv/system-lab/team/member.txt
ls -l /srv/system-lab/team/member.txt
```

Mong đợi owner labmember, group labops, thường mode 660 với umask 007; đọc thành công. Đây là umask cho phiên lệnh này, chưa cấu hình umask vĩnh viễn cho mọi user.

2. labguest không thuộc labops thử đọc và tạo file:

```bash
sudo -u labguest cat /srv/system-lab/team/member.txt
echo $?
sudo -u labguest touch /srv/system-lab/team/guest-should-not-exist.txt
echo $?
```

Mong đợi Permission denied và exit code khác 0 ở cả hai phép thử. Chạy echo $? ngay sau lệnh cần kiểm tra. Nếu labguest đọc được, kiểm tra id labguest, parent permissions, mode và ACL; chưa kết luận bài đạt.

3. Kiểm tra quyền sửa, đổi tên và xóa file mẫu của nhóm:

```bash
sudo -u labmember sh -c 'printf "second line\n" >> /srv/system-lab/team/member.txt'
sudo -u labmember mv /srv/system-lab/team/member.txt /srv/system-lab/team/member-renamed.txt
sudo -u labmember cp /srv/system-lab/team/member-renamed.txt /srv/system-lab/team/delete-test.txt
sudo -u labmember rm -i /srv/system-lab/team/delete-test.txt
ls -la /srv/system-lab/team
```

Không dùng root để kiểm thử từ chối: root có thể vượt qua nhiều quyền thông thường. Thay đổi group membership không cập nhật ngay mọi phiên đăng nhập cũ; sudo -u tạo tiến trình mới, còn phiên SSH cũ của user cần đăng xuất/đăng nhập lại.

Pass: có output id, mode/owner/group, thao tác thành công của labmember và hai phép bị từ chối của labguest. Biết giải thích r/w/x trên file và directory, chown, chmod, setgid, umask. Không bắt buộc ACL nâng cao trong giai đoạn cơ bản.

ĐIỂM GỬI KẾT QUẢ 2: gửi U05–U08, nhất là kết quả user ngoài nhóm. Không cần gửi mật khẩu tài khoản thực hành.

## 9. Ubuntu: service, logs và firewall — U09 đến U11

### U09. Hiểu service và journal bằng SSH đang có

Trên Ubuntu:

```bash
systemctl status ssh.service ssh.socket --no-pager
systemctl is-enabled ssh.service
systemctl is-enabled ssh.socket
sudo ss -lntp
sudo journalctl -u ssh.service -u ssh.socket -b -n 50 --no-pager
sudo journalctl -b -p err --no-pager
```

Phân biệt active (đang hoạt động) và enabled (cấu hình khởi động); static/indirect/socket activation cần xét theo unit thực tế. Không yêu cầu cả ssh.service và ssh.socket đều enabled.

Thực hiện một lần đăng nhập SSH mới từ host, xem journal để đối chiếu thời gian và user. Có thể xem live bằng sudo journalctl -u ssh.service -f, Ctrl+C để dừng xem; Ctrl+C không tắt SSH server.

Pass: chỉ ra unit/listener đang phục vụ SSH và log đăng nhập tương ứng. Lỗi lịch sử của boot cũ không tự động là lỗi hiện tại; ghi timestamp và khả năng tái diễn. Không xóa journal để tạo ảnh “sạch”.

### U10. Service thực hành độc lập, không dừng SSH

Để học start/stop/enable mà không mất kết nối quản trị, tạo một systemd oneshot unit lab chỉ ghi dòng log. Trước tiên kiểm tra chưa có unit cùng tên:

```bash
systemctl cat system-lab-demo.service
```

Nếu báo không có unit thì tạo file bằng sudo nano /etc/systemd/system/system-lab-demo.service. Nội dung:

```ini
[Unit]
Description=System lab harmless service demonstration

[Service]
Type=oneshot
ExecStart=/usr/bin/logger -t system-lab-demo System-lab-service-started
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Kiểm tra đường dẫn logger bằng command -v logger; nếu khác /usr/bin/logger thì sửa ExecStart cho đúng. Sau khi lưu:

```bash
sudo systemd-analyze verify /etc/systemd/system/system-lab-demo.service
sudo systemctl daemon-reload
sudo systemctl enable --now system-lab-demo.service
systemctl status system-lab-demo.service --no-pager
sudo journalctl -u system-lab-demo.service -b --no-pager
sudo journalctl -t system-lab-demo -b --no-pager
```

Mong đợi active (exited), enabled và thấy thông điệp log. Đây là hành vi đúng của oneshot có RemainAfterExit; không phải web server chạy nền. Nếu verify báo lỗi, sửa file trước khi enable.

Thử stop rồi start lại:

```bash
sudo systemctl stop system-lab-demo.service
systemctl is-active system-lab-demo.service
sudo systemctl start system-lab-demo.service
systemctl is-active system-lab-demo.service
```

Mong đợi inactive sau stop và active sau start. Giữ enabled tới kiểm thử reboot U12. Hoàn tác tùy chọn sau khi đã thu bằng chứng: sudo systemctl disable --now system-lab-demo.service, sau đó nếu muốn xóa unit thì chỉ xóa đúng file đã tạo và daemon-reload. Không dùng service SSH cho bài stop/start này.

### U11. Bật UFW mà vẫn giữ đường quản trị

Điều kiện bắt buộc: U05 đạt; có quyền vào VMware console; biết SSH port thật; đang giữ ít nhất một phiên SSH và có thể mở phiên thứ hai. Firewall chỉ làm sau khi mạng ổn định.

Kiểm tra trước:

```bash
dpkg-query -W ufw
sudo ufw status verbose
sudo ufw show added
sudo ss -lntp
```

Nếu ufw chưa cài, sudo apt install ufw sau khi U04 đạt. Nếu đang active và có rule cũ, lưu output rồi xem xét từng rule; không ufw reset. Rule được thêm trước đây vẫn có thể cho phép truy cập dù default là deny.

Với lab riêng NAT chưa có rule phức tạp và SSH dùng port 22, cấu hình cơ bản:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'Lab SSH management'
sudo ufw show added
sudo ufw enable
sudo ufw status verbose
```

Nếu SSH dùng port khác, thay 22 bằng port hiệu lực trước khi bật. Allow 22/tcp cho mọi nguồn tới VM phù hợp phạm vi lab NAT cơ bản; không mô tả là chính sách production. Chưa cần port forwarding trên VMware/router. Không đồng thời đổi SSH port và bật firewall.

Trên Windows host, mở phiên PowerShell mới:

```powershell
Test-NetConnection IP_UBUNTU -Port 22
ssh sysadmin@IP_UBUNTU
```

Chỉ phiên SSH cũ còn sống không đủ Pass; phải đăng nhập mới thành công. Nếu bị khóa, dùng console: sudo ufw status numbered, thêm đúng allow cho port SSH thật; nếu chưa chẩn đoán được, tạm sudo ufw disable tại console để khôi phục truy cập rồi ghi nguyên nhân. Không cần reboot để cứu lỗi UFW.

Kiểm chứng chặn bằng một dịch vụ mẫu CÓ listener, thay vì thử một port không có ứng dụng:

1. Kiểm tra command -v python3 và xem ss -lntp để chắc port 8088 chưa dùng. Nếu python3 không có, cài sudo apt install python3 sau U04 hoặc ghi Blocked cho test mẫu.
2. Tại Ubuntu console hoặc một phiên SSH riêng, tạo thư mục chỉ chứa dữ liệu mẫu rồi chạy HTTP tạm bằng user thường:

```bash
mkdir -p ~/system-lab/http-test
printf 'Ubuntu firewall test\n' > ~/system-lab/http-test/index.html
python3 -m http.server 8088 --bind 0.0.0.0 --directory "$HOME/system-lab/http-test"
```

Giữ terminal này mở. Dịch vụ mẫu chỉ phục vụ thư mục trên; không dùng home hoặc / làm web root. Không có dữ liệu nhạy cảm. Ở terminal Ubuntu khác:

```bash
ss -lntp | grep ':8088'
```

3. Khi UFW active, mặc định deny incoming và KHÔNG có rule cho 8088, Windows host chạy Test-NetConnection IP_UBUNTU -Port 8088. Mong đợi TcpTestSucceeded=False; ping thành công không thay đổi kết luận TCP.
4. Để đối chứng đường mạng, trên Ubuntu tạm cho phép rồi thử lại từ host:

```bash
sudo ufw allow 8088/tcp comment 'Temporary firewall verification'
```

Host thử Test-NetConnection lần mới, mong đợi True; trình duyệt http://IP_UBUNTU:8088 hiện nội dung mẫu. Nếu vẫn False, chưa chứng minh được UFW là nguyên nhân; kiểm tra listener, IP, route và rule.
5. Gỡ đúng rule tạm rồi thử kết nối TCP mới từ host, mong đợi False:

```bash
sudo ufw delete allow 8088/tcp
sudo ufw status numbered
```

6. Tại terminal đang chạy HTTP, Ctrl+C để dừng server. Kiểm tra ss -lntp: không còn listener 8088. Không để lại rule tạm. Kết nối SSH mới một lần nữa để xác nhận port quản trị vẫn được phép.

Pass: UFW active, rule SSH đúng, có kết quả chặn–cho phép–chặn trên dịch vụ mẫu, dọn dịch vụ/rule thử xong và SSH mới vẫn thành công. Nếu đã có rule rộng cho 8088 hoặc toàn bộ subnet, phải xử lý/giải thích trước khi nhận định test đạt.

## 10. Ubuntu: reboot, thu log và nghiệm thu — U12 đến U13

### U12. Kiểm tra tính bền vững sau reboot

Lưu các file đang mở; chắc apt/dpkg không chạy. Ghi IP hiện tại và trạng thái firewall/SSH. Tại Ubuntu:

```bash
sudo reboot
```

SSH bị ngắt là bình thường. Chờ VM boot xong, đăng nhập console để lấy IP mới nếu cần:

```bash
hostnamectl
ip -br -4 address
ip route
resolvectl status
systemctl status ssh.service ssh.socket --no-pager
sudo ufw status verbose
systemctl is-enabled system-lab-demo.service
systemctl status system-lab-demo.service --no-pager
sudo journalctl -t system-lab-demo -b --no-pager
systemctl --failed --no-pager
getent ahostsv4 archive.ubuntu.com
```

Trên Windows host, SSH vào IP hiện tại; không tiếp tục dùng IP DHCP cũ nếu đã đổi. Trong phiên mới:

```bash
whoami
hostname
sudo apt update
sudo -u labmember cat /srv/system-lab/team/member-renamed.txt
sudo -u labguest cat /srv/system-lab/team/member-renamed.txt
```

Pass: hostname và NAT/DHCP đúng, có default route và DNS, apt update được, SSH mới được, UFW vẫn active, unit demo đã chạy trong boot này, quyền thành viên/ngoài nhóm vẫn đúng. IP DHCP không cần giữ nguyên. Fail một phần thì ghi đúng phần đó, không cài lại Ubuntu.

### U13. Thu bằng chứng dạng text và chuyển về host

Trên Ubuntu, tạo thư mục bằng chứng và dùng tee để vừa xem vừa lưu. Thực hiện từng dòng:

```bash
mkdir -p ~/system-lab/evidence
hostnamectl | tee ~/system-lab/evidence/U01-hostname.txt
cat /etc/os-release | tee ~/system-lab/evidence/U01-os.txt
ip -br -4 address | tee ~/system-lab/evidence/U02-ip.txt
ip route | tee ~/system-lab/evidence/U02-route.txt
resolvectl status | tee ~/system-lab/evidence/U04-dns.txt
sudo ss -lntp | tee ~/system-lab/evidence/U05-listeners.txt
sudo ufw status verbose | tee ~/system-lab/evidence/U11-firewall.txt
systemctl --failed --no-pager | tee ~/system-lab/evidence/U12-failed-units.txt
```

Để lưu cả stderr của test bị chặn:

```bash
sudo -u labguest cat /srv/system-lab/team/member-renamed.txt > ~/system-lab/evidence/U08-denied.txt 2>&1
printf 'exit_code=%s\n' "$?" >> ~/system-lab/evidence/U08-denied.txt
```

Giữ nguyên thứ tự để exit_code là của phép thử vừa chạy. Đừng dùng pipe tới tee rồi lấy $? và tưởng đó chắc chắn là exit code của lệnh kiểm thử trước pipe.

Trên Windows host, thay IP_UBUNTU và dùng cùng tài khoản đã SSH thành công:

```powershell
scp -r sysadmin@IP_UBUNTU:/home/sysadmin/system-lab/evidence 'D:\Lab-Evidence-System\ubuntu'
```

Nếu home thực tế không phải /home/sysadmin, xác minh trên Ubuntu bằng printf '%s\n' "$HOME" rồi thay đường dẫn. Lệnh scp có thể tạo thư mục evidence bên trong ubuntu, đó là bình thường. Nếu SSH dùng port khác, scp dùng -P PORT (chữ P hoa).

Đối với apt update hoặc log lỗi, có thể copy text terminal hoặc dùng script để ghi phiên: script -a ~/system-lab/evidence/session.txt; làm một nhóm kiểm tra; gõ exit để dừng ghi. Đọc lại trước khi chia sẻ; không ghi phiên có secret hoặc nội dung riêng.

Ảnh nên có hostname/lệnh/kết quả trong cùng khung. Không gửi chỉ ảnh “Permission denied” mà thiếu danh tính user và đường dẫn.

## 11. Hoàn thiện repository và tài liệu — D01 đến D04

### D01. Tài liệu Ubuntu tối thiểu

Tạo docs/ubuntu-server-lab.md khi đã có kết quả thật, gồm: mục tiêu; Ubuntu VERSION_ID; cấu hình VM; NAT/DHCP/interface; kết nối SSH; user/group; quyền thư mục; service/log; UFW; kiểm thử reboot; troubleshooting; giới hạn. IP hiện tại ghi kèm ngày và nhãn DHCP, không gọi là IP cố định.

Đưa cấu hình mẫu đã kiểm chứng vào configs/ubuntu/ nếu cần. File mẫu phải ghi đúng phiên bản và tên interface thực tế; không đưa private key, shadow, mật khẩu hoặc toàn bộ home. Unit system-lab-demo.service có thể lưu như một ví dụ quản trị service.

### D02. Cập nhật README mà không làm sai kiến trúc

Giữ tên dự án hiện tại nếu muốn và thêm mục Ubuntu Server Administration Lab. Sơ đồ phải chỉ rõ ba môi trường độc lập; ghi VMware Windows không nối trực tiếp Packet Tracer. Nếu Ubuntu chưa có AD integration thì không mô tả đã tích hợp.

Chỉ chuyển test sang Pass sau khi có bằng chứng mới. Giữ test chưa hoàn thành thành Fail/Blocked/Chưa kiểm thử kèm lý do; không xóa test lỗi để bảng đẹp. Nếu ảnh cũ mâu thuẫn hiện trạng, cập nhật hoặc ghi ảnh lịch sử.

### D03. Nhật ký lỗi và cách khắc phục

Mỗi lỗi viết theo mẫu: ngày; mã test; hiện tượng; lệnh kiểm tra; nguyên nhân có bằng chứng; thay đổi đã làm; cách xác minh lại; kết quả. Phân biệt nguyên nhân đã xác định với giả thuyết. Không ghi một loạt lệnh sửa mà thiếu kết quả sau sửa.

### D04. CV sau nghiệm thu

Có thể mô tả dự án là lab quản trị Windows Server, mô phỏng mạng doanh nghiệp và quản trị Ubuntu cơ bản. Chỉ thêm Ubuntu khi các phần bạn nêu thực sự đạt. Có thể ghi user/group, permissions, SSH, systemd/journal và UFW nếu đã kiểm thử tương ứng.

Không ghi triển khai production hoặc phục vụ 30–50 người dùng thật. Không ghi web server production chỉ vì đã chạy Python HTTP tạm để test firewall. Không gọi snapshot là một giải pháp backup đã triển khai. AWS không được dự án này chứng minh.

## 12. Checklist nghiệm thu toàn bộ

Điền Kết quả bằng Pass / Fail / Blocked / Chưa làm / N/A và ghi file bằng chứng. Các hàng bắt buộc chưa đạt thì chưa kết luận toàn bộ lab hoàn thành.

| Mã | Tiêu chí | Bắt buộc | Kết quả / bằng chứng |
| --- | --- | --- | --- |
| P01–P04 | Biết trạng thái VM, mạng ảo, có nơi lưu bằng chứng | Có | Chưa làm |
| W01 | SERVER01 đúng IP/OS, dịch vụ cần thiết hoạt động | Có | Chưa làm |
| W02 | Domain/OU/group và SYSVOL/NETLOGON đúng | Có | Chưa làm |
| W03 | DNS A/PTR/SRV đạt | Có | Chưa làm |
| W04–W05 | DHCP/reservation, DNS client, domain trust và SMB TCP đúng | Có | Chưa làm |
| W06 | Đúng user domain; user/computer GPO và hạn chế thực tế | Có | Chưa làm |
| W07–W08 | Share/NTFS, mapped drives và truy cập chéo bị chặn | Có | Chưa làm |
| N01–N02 | File .pkt mở được, VLAN/trunk/routing đúng | Có | Chưa làm |
| N03 | Guest chặn nội bộ, kiểm chứng ACL hit | Có | Chưa làm |
| N04–N05 | NAT/PAT ra mạng ngoài mô phỏng, ghi rõ giới hạn DHCP relay | Có | Chưa làm |
| U01–U02 | OS/version, hostname, resource, NAT/DHCP/IP/route đã xác minh | Có | Chưa làm |
| U03 | Đọc Netplan và xác định nguồn quản lý; chỉ sửa nếu cần | Có | Chưa làm |
| U04 | DNS và apt update hoạt động | Có | Chưa làm |
| U05 | SSH mới từ Windows host thành công, biết unit/listener | Có | Chưa làm |
| U06 | Package manager không lỗi, cập nhật hoặc hoãn có lý do | Có | Chưa làm |
| U07 | Filesystem lab và thao tác cơ bản đạt | Có | Chưa làm |
| U08 | User/group, cho phép và từ chối bằng đúng danh tính | Có | Chưa làm |
| U09–U10 | Service status/start/stop/enable và đọc journal đạt | Có | Chưa làm |
| U11 | UFW active, SSH còn vào được, test chặn–cho phép–chặn đạt | Có | Chưa làm |
| U12 | Reboot xong mạng/SSH/firewall/service/permissions vẫn đúng | Có | Chưa làm |
| U13 | Log/ảnh đã lưu và chuyển về host | Có | Chưa làm |
| D01–D04 | Tài liệu phản ánh đúng hiện trạng, không lộ secret | Có | Chưa làm |
| X01 | Backup/restore nâng cao, scripting, monitoring, AD–Linux | Không | Giai đoạn nâng cấp |

Hoàn thành phạm vi cơ bản khi các mục bắt buộc Pass; trường hợp N/A phải được xem lại để chắc không che một yêu cầu chưa làm. Một lab có thể hoàn thành với giới hạn kiến trúc được ghi rõ, không cần thêm công nghệ để tăng số lượng.

## 13. Mẫu gửi kết quả để đánh giá

### 13.1. Gửi theo chặng, không cần đợi xong hết

Sau Windows: W01–W08 và ảnh mạng VMware Windows. Sau Network: N01–N05. Sau Ubuntu mạng: U01–U04. Sau quản trị Ubuntu: U05–U11. Sau reboot: U12–U13 và checklist tổng hợp. Có lỗi thì gửi ngay mã test đang lỗi, chưa cần làm các bước phụ thuộc.

### 13.2. Mẫu thông tin tổng hợp

```text
Ngày kiểm tra:
Chặng đang thực hiện:

SERVER01: OS / IP / DNS / VMnet:
CLIENT01: OS / IP / DHCP Server / DNS / VMnet:
Ubuntu: VERSION_ID / hostname / user:
Ubuntu: network mode / interface / IPv4 / gateway / upstream DNS:
SSH: port / service hoặc socket / kết nối mới có được không:

Mã test:
Máy thực hiện và quyền chạy:
Lệnh hoặc thao tác đã làm:
Kết quả mong đợi:
Output thực tế hoặc tên ảnh:
Kết luận tự đánh giá: Pass / Fail / Blocked / Chưa làm
Thay đổi cấu hình đã làm từ lần trước:
Lỗi còn tồn tại:
Điểm cần kiểm tra giúp:
```

### 13.3. Bộ bằng chứng Ubuntu nên gửi trước tiên

1. Ảnh VMware Network Adapter của Ubuntu; ảnh cấu hình NAT VMnet nếu có.
2. hostnamectl và cat /etc/os-release.
3. ip -br -4 address, ip route, resolvectl status.
4. Nội dung các YAML Netplan hiện tại, đã che thông tin nhạy cảm nếu có.
5. Output apt update có cả phần cuối và lỗi, không chỉ dòng đầu.
6. status ssh.service/ssh.socket, listener, kết quả SSH mới từ host.
7. id labmember/labguest, ls -ld team, đọc thành công và Permission denied.
8. UFW status và kết quả thử TCP 8088 trước/sau rule tạm.
9. Service demo, journal và kết quả sau reboot.

Đánh giá từ tài liệu/ảnh/log là xác minh trong phạm vi bằng chứng bạn cung cấp; chưa phải kiểm tra độc lập toàn bộ VM. Nếu bằng chứng thiếu hoặc mâu thuẫn, kết quả sẽ là cần kiểm tra thêm, không tự công nhận hoàn thành.

## 14. Nâng cấp sau khi đã chốt phần cơ bản

Ưu tiên 1: backup/restore dữ liệu mẫu, có kiểm thử khôi phục và kiểm tra quyền sau restore. Ưu tiên 2: PowerShell/Bash kiểm tra tình trạng lab. Ưu tiên 3: một dịch vụ Linux có mục tiêu rõ, ví dụ Nginx trang nội bộ, gồm service, firewall và logs. Ưu tiên 4: monitoring hoặc AD–Linux chỉ khi bạn hiểu nền tảng và máy đủ tài nguyên.

Các mục trên không phải điều kiện bắt buộc để hoàn thành checklist cơ bản. Chỉ triển khai khi bạn chủ động chọn phạm vi tiếp theo.

## 15. Nguồn kỹ thuật chính thức và cách đối chiếu

Đã tham chiếu ngày 27/10/2026. Nội dung là quy trình riêng cho lab, không sao chép nguyên một tài liệu nhà cung cấp. Khi giao diện/lệnh khác phiên bản, lấy output thực tế và tài liệu tương ứng làm căn cứ.

- Ubuntu — cấu hình mạng bằng Netplan: https://ubuntu.com/server/docs/explanation/networking/configuring-networks/
- Netplan — netplan try, xác nhận và giới hạn rollback: https://netplan.readthedocs.io/en/stable/netplan-try/
- Ubuntu — OpenSSH server, cấu hình và kiểm tra trước thay đổi: https://ubuntu.com/server/docs/how-to/security/openssh-server/
- Ubuntu — UFW: https://ubuntu.com/server/docs/how-to/security/firewalls/
- Ubuntu — quản lý package APT: https://ubuntu.com/server/docs/how-to/software/package-management/
- Microsoft — dcdiag: https://learn.microsoft.com/windows-server/administration/windows-commands/dcdiag
- Microsoft — Test-ComputerSecureChannel: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-computersecurechannel

Tài liệu đầu vào của dự án: hồ sơ bàn giao DOCX do bạn cung cấp; README.md; docs/project-notes.md; docs/troubleshooting.md; configs/*.txt. Các bản ghi trước đây được dùng làm kỳ vọng để kiểm tra lại, không thay thế kết quả kiểm thử hiện tại.
