#!py

def run():
    rst = {}
    for item, opts in __opts__['confd'].items():
        src = opts.pop('src') or opts.pop('source')
        rst[opts['dest']] = {'file.managed': []}
        rst[opts['dest']]['file.managed'].append({'source': src})
        for opt, val in opts.items():
            rst[opts['dest']]['file.managed'].append({opt: val})
    return rst
