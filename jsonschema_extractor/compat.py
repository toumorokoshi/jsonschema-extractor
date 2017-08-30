import sys
is_py3 = sys.version_info[0] >= 3

if is_py3:
    string_type = str  # pragma: nocover
    all_string_types = [str]  # pragma: nocover
else:
    string_type = basestring  # pragma: nocover
    all_string_types = [basestring, str, unicode]  # pragma: nocover
