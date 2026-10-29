"""Build a self-contained Word guide from the adjacent Markdown, using stdlib only."""
from pathlib import Path
import re
import zipfile
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'Ke_hoach_hoan_thien_lab_Windows_Network_Ubuntu.md'
DEST = SOURCE.with_suffix('.docx')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}

def run(text, code=False):
    props = '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr>' if code else ''
    return '<w:r>' + props + '<w:t xml:space="preserve">' + escape(text) + '</w:t></w:r>'

def paragraph(text='', style='Normal', extra='', bookmark=None):
    start = f'<w:bookmarkStart w:id="{bookmark}" w:name="section_{bookmark}"/>' if bookmark is not None else ''
    end = f'<w:bookmarkEnd w:id="{bookmark}"/>' if bookmark is not None else ''
    return '<w:p><w:pPr><w:pStyle w:val="' + style + '"/>' + extra + '</w:pPr>' + start + run(text, style == 'Code') + end + '</w:p>'

def table(rows):
    count = len(rows[0])
    widths = ([1450, 3550, 5100] if count == 3 else [1200, 4250, 1000, 3650] if count == 4 else [10100 // count] * count)
    out = ['<w:tbl><w:tblPr><w:tblW w:w="10100" w:type="dxa"/><w:tblLayout w:type="fixed"/><w:tblBorders>']
    for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        out.append(f'<w:{side} w:val="single" w:sz="4" w:color="D4DDE5"/>')
    out.append('</w:tblBorders><w:tblCellMar><w:top w:w="85" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:bottom w:w="85" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>')
    out.extend(f'<w:gridCol w:w="{width}"/>' for width in widths)
    out.append('</w:tblGrid>')
    for idx, row in enumerate(rows):
        out.append('<w:tr><w:trPr><w:cantSplit/>' + ('<w:tblHeader/>' if idx == 0 else '') + '</w:trPr>')
        for width, cell in zip(widths, row):
            shade = '163B55' if idx == 0 else ('F0F5F8' if idx % 2 == 0 else 'FFFFFF')
            out.append(f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:shd w:fill="{shade}"/><w:vAlign w:val="top"/></w:tcPr>')
            out.append(paragraph(cell, 'TableHead' if idx == 0 else 'TableBody'))
            out.append('</w:tc>')
        out.append('</w:tr>')
    out.append('</w:tbl>')
    return ''.join(out)

lines = SOURCE.read_text(encoding='utf-8').splitlines()
sections = [s[3:] for s in lines if s.startswith('## ')]
body = [paragraph('HỒ SƠ THỰC HÀNH & NGHIỆM THU', 'Subtitle'), paragraph('Hoàn thiện lab\nWindows • Network • Ubuntu'.replace('\n', ' — '), 'Title'), paragraph('Hoàng Công Minh | Phiên bản 1.0 | 27/10/2026', 'Subtitle'), paragraph('Làm theo từng chặng • Kiểm tra trước khi sửa • Có bằng chứng để kết luận', 'Lead'), paragraph('Ubuntu được hướng dẫn từ kiểm kê hiện trạng, NAT/DHCP/DNS, SSH đến phân quyền, systemd, firewall và kiểm thử sau reboot.'), paragraph('Trạng thái ban đầu: CHƯA KIỂM THỬ LẠI. Tài liệu này không xác nhận VM đã hoàn thành.', 'Notice'), paragraph('Nội dung', 'Heading1', '<w:pageBreakBefore/>')]
for idx, title in enumerate(sections, 1):
    body.append('<w:p><w:pPr><w:pStyle w:val="Contents"/></w:pPr><w:hyperlink w:anchor="section_' + str(idx) + '">' + run(title) + '</w:hyperlink></w:p>')
body.append(paragraph('Trong Word: dùng View → Navigation Pane để di chuyển theo đề mục. Có thể nhấn Ctrl và bấm mục ở trên để đến phần tương ứng.', 'Caption'))
i = 0
section_idx = 0
code = False
code_lines = []
while i < len(lines):
    line = lines[i]
    if line.startswith('```'):
        if not code:
            code = True
            code_lines = []
        else:
            for k, value in enumerate(code_lines):
                # Keep each small command block together when it fits a page.
                extra = '<w:keepNext/>' if k < len(code_lines) - 1 and len(code_lines) <= 12 else ''
                body.append(paragraph(value, 'Code', extra))
            body.append(paragraph('', 'Spacer'))
            code = False
        i += 1
        continue
    if code:
        code_lines.append(line)
        i += 1
        continue
    if line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            row = [x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', x) for x in row):
                rows.append(row)
            i += 1
        body.append(table(rows))
        body.append(paragraph('', 'Spacer'))
        continue
    if line.startswith('# '):
        i += 1
        continue
    if line.startswith('## '):
        section_idx += 1
        body.append(paragraph(line[3:], 'Heading1', '<w:pageBreakBefore/>', section_idx))
    elif line.startswith('### '):
        body.append(paragraph(line[4:], 'Heading2'))
    elif line.startswith('- '):
        body.append(paragraph('• ' + line[2:], 'Bullet'))
    elif line:
        body.append(paragraph(line, 'Notice' if line.startswith('ĐIỂM GỬI KẾT QUẢ') else 'Normal'))
    i += 1
assert not code, 'Unclosed code fence'

def style(name, size, color='243746', bold=False, extra='', ppr=''):
    return f'<w:style w:type="paragraph" w:styleId="{name}"><w:name w:val="{name}"/><w:basedOn w:val="Normal"/><w:pPr>{ppr}</w:pPr><w:rPr><w:sz w:val="{size}"/><w:color w:val="{color}"/>{"<w:b/>" if bold else ""}{extra}</w:rPr></w:style>'

styles = f'''<w:styles xmlns:w="{W}"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:lang w:val="vi-VN"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="110" w:line="275" w:lineRule="auto"/><w:widowControl/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'''
styles += style('Title', 48, '163B55', True, ppr='<w:spacing w:before="1200" w:after="400"/>')
styles += style('Subtitle', 24, '527489', ppr='<w:spacing w:before="200" w:after="200"/>')
styles += style('Lead', 28, '163B55', True, ppr='<w:spacing w:before="400" w:after="300"/>')
styles += style('Heading1', 32, '163B55', True, ppr='<w:keepNext/><w:outlineLvl w:val="0"/><w:spacing w:before="120" w:after="220"/>')
styles += style('Heading2', 26, '1B657B', True, ppr='<w:keepNext/><w:outlineLvl w:val="1"/><w:spacing w:before="260" w:after="130"/>')
styles += style('Code', 18, '192F40', extra='<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>', ppr='<w:shd w:fill="EEF3F6"/><w:ind w:left="110" w:right="110"/><w:spacing w:after="0" w:before="0" w:line="235" w:lineRule="auto"/>')
styles += style('TableHead', 20, 'FFFFFF', True, ppr='<w:spacing w:after="0" w:line="240"/>')
styles += style('TableBody', 20, ppr='<w:spacing w:after="0" w:line="240"/>')
styles += style('Notice', 22, '85470C', True, ppr='<w:shd w:fill="FFF2DC"/><w:spacing w:before="140" w:after="170"/>')
styles += style('Bullet', 22, ppr='<w:ind w:left="180" w:hanging="180"/>')
styles += style('Contents', 23, '1B657B', ppr='<w:spacing w:after="125"/>')
styles += style('Caption', 19, '627786', ppr='<w:spacing w:before="100" w:after="140"/>')
styles += style('Spacer', 8, ppr='<w:spacing w:after="30" w:line="100" w:lineRule="exact"/>')
styles += '</w:styles>'
sect = '<w:sectPr><w:headerReference w:type="default" r:id="rIdHeader"/><w:footerReference w:type="default" r:id="rIdFooter"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1000" w:right="900" w:bottom="1000" w:left="900" w:header="400" w:footer="450"/></w:sectPr>'
document = f'<w:document xmlns:w="{W}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>' + ''.join(body) + sect + '</w:body></w:document>'
header = f'<w:hdr xmlns:w="{W}">' + paragraph('SYSTEM / NETWORK / UBUNTU LAB  •  HƯỚNG DẪN THỰC HÀNH', 'Caption') + '</w:hdr>'
footer = f'<w:ftr xmlns:w="{W}"><w:p><w:pPr><w:jc w:val="right"/></w:pPr>' + run('Hoàng Công Minh | v1.0 | Trang ') + '<w:fldSimple w:instr="PAGE"/>' + run(' / ') + '<w:fldSimple w:instr="NUMPAGES"/></w:p></w:ftr>'
types = '''<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>'''
rels = '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>'
docrels = '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rIdHeader" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/><Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>'
core = '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Hướng dẫn hoàn thiện lab Windows Network Ubuntu</dc:title><dc:creator>Hoàng Công Minh — tài liệu thực hành hỗ trợ bởi Codex</dc:creator><dc:description>Hướng dẫn kiểm tra, cấu hình và nghiệm thu lab; không xác nhận trạng thái VM hiện tại.</dc:description></cp:coreProperties>'
parts = {'[Content_Types].xml': types, '_rels/.rels': rels, 'docProps/core.xml': core, 'word/document.xml': document, 'word/styles.xml': styles, 'word/_rels/document.xml.rels': docrels, 'word/header1.xml': header, 'word/footer1.xml': footer}
for name, xml in parts.items():
    ET.fromstring(xml)
with zipfile.ZipFile(DEST, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, xml in parts.items():
        z.writestr(name, '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + xml)
with zipfile.ZipFile(DEST) as z:
    assert z.testzip() is None
    root = ET.fromstring(z.read('word/document.xml'))
    alltext = ''.join(t.text or '' for t in root.findall('.//w:t', NS))
    for required in ['U01.', 'U13.', 'W01.', 'N01.', 'netplan try --timeout 120', 'UFW', 'Permission denied', 'Mẫu gửi kết quả']:
        assert required in alltext, required
    assert '\ufffd' not in alltext
    assert len(root.findall('.//w:bookmarkStart', NS)) == len(sections)
print(f'Created {DEST.name}: {DEST.stat().st_size:,} bytes; {len(sections)} sections; {len(root.findall(".//w:tbl", NS))} tables; {len(alltext):,} text characters.')
