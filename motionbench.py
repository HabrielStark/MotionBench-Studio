#!/usr/bin/env python3
"""MotionBench Studio: evidence-first video inspection, no fabricated aesthetic scores."""
import argparse, json, subprocess, hashlib, pathlib, math

def run(args):
    p=subprocess.run(args,capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def inspect(path, out, reference=None):
    path=pathlib.Path(path).resolve(); out=pathlib.Path(out); out.mkdir(parents=True,exist_ok=True)
    meta=run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    vs=next(s for s in meta['streams'] if s['codec_type']=='video')
    w,h=int(vs['width']),int(vs['height']); fps=vs.get('avg_frame_rate','0/1')
    duration=float(meta['format'].get('duration',0)); issues=[]
    if not any(s['codec_type']=='audio' for s in meta['streams']):
        issues.append({'rule':'audio_absent','severity':'info','note':'Audio stream not present; may be intentional.'})
    filters='signalstats,metadata=print:file=-'
    proc=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-vf',filters,'-an','-f','null','-'],capture_output=True,text=True)
    # The frame scanner is independent of ffmpeg signalstats output availability.
    frame_info=run(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time,pict_type','-of','json',str(path)])['frames']
    times=[float(f['best_effort_timestamp_time']) for f in frame_info if 'best_effort_timestamp_time' in f]
    if len(times)<2: issues.append({'rule':'insufficient_frames','severity':'critical'})
    gaps=[(i,round(times[i]-times[i-1],6)) for i in range(1,len(times))]
    median=sorted(g for _,g in gaps)[len(gaps)//2] if gaps else 0
    for i,g in gaps:
        if median and g>median*1.8: issues.append({'rule':'timestamp_gap','severity':'major','frame':i,'time':times[i],'gap':g})
    cuts=[]
    scene=subprocess.run(['ffmpeg','-hide_banner','-i',str(path),'-vf',"select='gt(scene,0.32)',showinfo",'-an','-f','null','-'],capture_output=True,text=True)
    import re
    for line in scene.stderr.splitlines():
        m=re.search(r'pts_time:([\d.]+)',line)
        if m: cuts.append(float(m.group(1)))
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    report={'schema_version':1,'artifact':{'path':str(path),'sha256':sha,'width':w,'height':h,'fps':fps,'duration':duration,'decoded_frame_timestamps':len(times)},'coverage':{'timestamp_scan':True,'pixel_scan':False,'visual_review':False,'audio_listened':False},'candidate_cuts':cuts,'issues':issues,'aesthetic_score':None,'verdict':'UNASSESSED','note':'Automated checks do not certify aesthetic quality. A calibrated independent judge is required.'}
    if reference:
        ref=run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(reference)])
        rv=next(s for s in ref['streams'] if s['codec_type']=='video')
        report['reference']={'path':str(pathlib.Path(reference).resolve()),'width':int(rv['width']),'height':int(rv['height']),'duration':float(ref['format'].get('duration',0))}
        if (w,h)!=(report['reference']['width'],report['reference']['height']):issues.append({'rule':'reference_resolution_mismatch','severity':'major'})
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('video');ap.add_argument('--out',default='motionbench-report');ap.add_argument('--reference')
    a=ap.parse_args();print(json.dumps(inspect(a.video,a.out,a.reference),indent=2))
