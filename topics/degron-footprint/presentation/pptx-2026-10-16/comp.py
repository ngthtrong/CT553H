"""Reusable slide components built on lib.Deck."""
from lib import *


def chip(d, x, y, w, text, fill=AMBER_T, color=INK, size=11, h=0.3, line=None, bold=True, nm=None, dash=False):
    return d.rect(x, y, w, h, fill=fill, line=line, shape="round", radius=0.5, dash=dash,
                  paras=[P(text, size=size, bold=bold, color=color, align="c")], margin=0.06, nm=nm or f"chip: {text[:20]}")


def card(d, x, y, w, h, head, body, accent=STEEL, tint=None, hsize=14, bsize=12, nm=None):
    """Rounded card: tinted panel with a bold coloured heading and body text."""
    shp = d.rect(x, y, w, h, fill=tint or PANEL, shape="round", nm=nm or f"card: {head[:20]}")
    d.text(x + 0.15, y + 0.1, w - 0.3, h - 0.15, [P(head, size=hsize, bold=True, color=accent)] +
           ([P(body, size=bsize, space=3)] if isinstance(body, str) else body), nm=f"card text: {head[:20]}")
    return shp


def strip(d, x, y, n, cell, gap=0.03, coral=(), fills=None, labels=None, size=9, nm="peptide"):
    shapes = []
    for i in range(n):
        col = CORAL if i in coral else (fills[i] if fills else LINE)
        shapes.append(d.rect(x + i * (cell + gap), y, cell, cell, fill=col, shape="rect", nm=f"{nm} {i + 1}",
                             paras=[P(labels[i], size=size, bold=True, mono=True, align="c", color=BG if i in coral else INK)] if labels else None,
                             margin=0.0))
    return shapes


def source(d, text, y=6.72, x=MX, w=W - 2 * MX, color=MUTED, size=10):
    return d.text(x, y, w, 0.34, [P(text, size=size, color=color)], nm="evidence label")


def legend_evidence(d, y=6.72):
    pass
