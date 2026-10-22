"""#RRGGBB:metin;  →  :metin; <<#RRGGBB>>   (PlantUML 1.2026 yeni aktivite renk sözdizimi)"""
import re, sys
for f in sys.argv[1:]:
    s = open(f).read()
    s = re.sub(r'#([0-9A-Fa-f]{6}):(.*?);', lambda m: f':{m.group(2)}; <<#{m.group(1)}>>', s, flags=re.S)
    open(f, 'w').write(s)
