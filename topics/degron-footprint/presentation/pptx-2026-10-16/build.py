import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import part1, part1b, part2, part3, part4, part5

d = Deck()
for fn in [part1.s01, part1.s02, part1.s03, part1.s04, part1.s05, part1b.s06, part1b.s07, part1b.s08, part1b.s09,
           part2.s10, part2.s11, part2.s12, part2.s13, part2.s14, part3.s15, part3.s16, part3.s17, part3.s18,
           part4.s19, part4.s20, part4.s21, part4.s22, part5.s23, part5.s24, part5.s25, part5.s26, part5.a1, part5.a2]:
    fn(d)
d.finish()
cp = d.prs.core_properties
cp.title = "Residue-Level Prediction of Degron Mutation Effects: progress report, week 6"
cp.author = "Nguyễn Thế Trọng"
cp.subject = "CT553H thesis, Can Tho University"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "degron-footprint-2026-10-16.pptx")
d.prs.save(out)
print("saved", out, "slides:", d.n)
for w in WARNINGS:
    print("WARN", w)
