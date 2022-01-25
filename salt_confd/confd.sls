#!py


def run():
    rst = {}
    for dest, opts in __opts__['confd'].items():
        src = opts.pop('src') or opts.pop('source')
        rst[dest] = {'file.managed': []}
        rst[dest]['file.managed'].append({'source': src})
        for opt, val in opts.items():
            rst[dest]['file.managed'].append({opt: val})
    return rst
