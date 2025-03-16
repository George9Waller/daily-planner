def context(extra_context=None):
    common_context = {}
    return (extra_context or {}) | common_context
