import json, sys, os
src = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\91294a0d-ce03-47eb-8c5f-7425e9bd2ed4\tasks\wy9xrnnzh.output"
out = os.path.dirname(os.path.abspath(__file__))
raw = open(src, encoding='utf-8').read()
start = 0
data = json.loads(raw)["result"]
for r in data:
    p = os.path.join(out, f"map_{r['lens']}.json")
    json.dump(r, open(p, 'w', encoding='utf-8'), indent=1)
    print(r['lens'], len(json.dumps(r)), p)
