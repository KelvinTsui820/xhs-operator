import json

with open(r'C:\Users\tsuik\.gemini\antigravity\brain\47a12f03-0147-490c-9d76-2640e056e6b3\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            d = json.loads(line)
            if d.get('type') == 'USER_INPUT':
                idx = d.get('step_index')
                c = d.get('content', '')
                if '<USER_REQUEST>' in c:
                    req = c.split('<USER_REQUEST>')[1].split('</USER_REQUEST>')[0].strip()
                else:
                    req = c[:120].strip()
                print(f"[{idx}] {req}")
        except Exception as e:
            pass
