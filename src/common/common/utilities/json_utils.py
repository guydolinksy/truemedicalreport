def json_to_dot_notation(new):
    def _convert(obj):
        if not isinstance(obj, dict) or not obj:
            return {(): obj}
        return {(k,) + a: v for k in obj for a, v in _convert(obj[k]).items()} or {}

    return {'.'.join((a,) + k): v for a in new for k, v in _convert(new[a]).items()}
