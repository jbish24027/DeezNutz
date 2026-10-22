"""Swap the vanilla hairline cap left in each vanilla-style graft for the live (VHR) hairline model's shape. Reads the installed graft, writes to staging/hairline/<plugin>/<file>."""
import json, os, sys, time, traceback
sys.path.insert(0, "C:/1. AUTHORIA/_tools/smp-coverage")
import hairgraft, nifrw
BS = chr(92)
sp = "C:/Users/User/AppData/Local/Temp/claude/C--1--AUTHORIA/8714b13a-8cba-4f6e-a284-eaf1cd40c73c/scratchpad"
J = [j for j in json.load(open(sp + "/staging/hairline_jobs.json")) if not j["same"]]
out_root = sp + "/staging/hairline"
def lp(p):
    p = os.path.normpath(p)
    return (BS + BS + "?" + BS + p) if len(p) > 240 and not p.startswith(BS + BS + "?") else p
done, failed, t0 = [], [], time.time()
logf = open(sp + "/s31_log.txt", "w", encoding="utf-8")
for k, j in enumerate(J):
    rel = os.path.join(j["plugin"], os.path.basename(j["bake"]))
    out = os.path.join(out_root, rel)
    try:
        rep = hairgraft.graft(lp(j["bake"]), out, [dict(name=j["hairline_eid"], hair=j["model"], companion=True, keep_bake_alpha=False)], log=lambda m: None)
        # verify: hairline shape now has the model's vertex count, hair shape + physics tag still present
        d = nifrw.Doc(lp(out))
        shp = {d.name_of(i): nifrw.parse_shape_hdr(d.blocks[i][1]).get("nvert") for i in hairgraft.shapes(d)}
        ok = shp.get(j["hairline_eid"]) == j["model_nverts"] and hairgraft.hair_physics_xml(d) and not any(n.startswith(j["hairline_eid"] + "_") for n in shp)
        if not ok:
            raise RuntimeError("verify failed: %s" % shp)
        done.append(dict(fid=j["fid"], rel=rel, removed=rep["removed"], replaced=rep["replaced"]))
    except Exception as e:
        failed.append(dict(fid=j["fid"], rel=rel, err=str(e)[:300]))
        logf.write("FAIL %s %s %s\n" % (j["fid"], j["name"], str(e)[:300])); logf.flush()
    if k % 200 == 0:
        logf.write("... %d/%d done=%d failed=%d %.0fs\n" % (k, len(J), len(done), len(failed), time.time() - t0)); logf.flush()
json.dump(dict(done=done, failed=failed), open(sp + "/staging/hairline_report.json", "w"))
logf.write("FINISHED done=%d failed=%d %.0fs\n" % (len(done), len(failed), time.time() - t0)); logf.close()
print("FINISHED done=%d failed=%d %.0fs" % (len(done), len(failed), time.time() - t0))
