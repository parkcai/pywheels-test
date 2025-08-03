import re

matched = re.compile(
    # r"\s*List.Mem\s+\(\s*(\d+)\s*\^\s*(\w+)\s*%\s*(\d+)\)\s+\[([\d\s,]+)\]\s*, "
    r"\s*(\d+)\s*\^(\w+)\s*\+\s*(\d+)\s*",
).fullmatch("2 ^ x + 1")

print(matched)