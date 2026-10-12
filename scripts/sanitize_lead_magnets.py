import zipfile
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def sanitize_xlsx(filepath, replacements):
    with zipfile.ZipFile(filepath, 'r') as zin:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                if item.filename == 'xl/sharedStrings.xml':
                    text = content.decode('utf-8')
                    for old_str, new_str in replacements.items():
                        if old_str in text:
                            print(f"Replacing in {filepath}: '{old_str}' -> '{new_str}'")
                            text = text.replace(old_str, new_str)
                    content = text.encode('utf-8')
                zout.writestr(item, content)
        buffer.seek(0)
    with open(filepath, 'wb') as f:
        f.write(buffer.read())
    print("Sanitized successfully:", filepath)

if __name__ == "__main__":
    # 1. Sanitize template 1
    r1 = {
        "（联系创始人微信可免费协助跑测一份复杂询盘）": "（如需协助跑测复杂询盘，可在官方粉丝群内交流）"
    }
    sanitize_xlsx(r"F:\xhs_operator\lead_magnets\2026_外贸精准核价Excel模板.xlsx", r1)

    # 2. Sanitize template 2
    r2 = {
        '微信: KelvinFlow (备注“小红书群友”)': '欢迎在官方粉丝群内交流反馈',
        '小红书群友终身享受限时首月 ¥39 破冰特权，免审开通 7 天试用！': '小红书群友可在官方交流群内随时提需求，我来为你免审开通体验！'
    }
    sanitize_xlsx(r"F:\xhs_operator\lead_magnets\2026_外贸防泄露自动核价模板_Kelvin极客版.xlsx", r2)
