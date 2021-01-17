import re
test = "https://www.oploverz.in/page/70/?s=naruto"

data = str(test.translate({ ord(c) : "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+" }))

print(int(re.sub(r"[\s||a-z]", "", data)))