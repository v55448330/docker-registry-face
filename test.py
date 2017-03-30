
def toTree(treeStr):
    tree = {}
    s=treeStr.split('/')
    tree['text'] = s[0]
    tree['nodes'] = []
    for i in s:
        prefix = treeStr[treeStr.find(i):]

        if i != s[0]:
            tree['nodes'].append(toTree(prefix))

    return tree

print toTree("aaa/bbb/ccc/ddd")
