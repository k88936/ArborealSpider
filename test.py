import re

from report import report


def test(message: str) -> int:
    pattern = r"我"
    # pattern = r"家教"
    if re.search(pattern, message) is not None:
        report()
        return 1
    else:
        return 0
