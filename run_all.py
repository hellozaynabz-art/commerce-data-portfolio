"""Download verified sources, run three projects, and export the website data."""
import runpy
from common import ROOT, dump
out={}
for slug in ['revenue-retention','demand-planning','conversion-intelligence']:
 out[slug]=runpy.run_path(str(ROOT/slug/'analysis.py'))['run']()
dump(ROOT/'portfolio-data.json',out)
