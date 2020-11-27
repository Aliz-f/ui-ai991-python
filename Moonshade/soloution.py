def recursive_soloution(node, seq):
    try:
        seq.append(node.action)
    except:
        pass
    if not node.parent:
        return seq
    else:
        return recursive_soloution(node.parent, seq)


def soloution(node):
    seq = []
    return recursive_soloution(node, seq)
