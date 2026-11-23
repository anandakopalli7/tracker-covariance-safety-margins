"""Figures of the v13 manuscript (package A). New file, 19 Nov 2026 (session A, Claude Opus 5.5).

Fig. 1 (method) carries no result. Figs. 2-4 are drawn only from the package exports; a figure whose inputs do not exist
yet is skipped, and the build prints a FIGURE PENDING marker in its place. Outputs: out\\figures\\<stem>.png and .pdf,
with a trace (<stem>_trace.json) naming every input file and its SHA-256.
Export keys (RESULTS_INTERFACE_v13.md): C: 'LB.frontier.<SRC>' = [[caution...], [wrong-go %...]] on the 201 levels, for
SRC in F0, E, E5, N, IMM, CK3; 'CI.frontier.<SRC>', F: 'F.frontier.<SRC>' likewise (insets). E: 'E3.<arm>.<lev>.dc', '.dc.ci',
'.dt', '.dt.ci'. B: 'B7.<r>.<L>.R', '.as_room'. C: 'LB.RS.<tau>.6.rel', '.rel.ci', 'LB.T<i>.rel'.
Usage: python -I make_figs_v13.py
"""
import json, pathlib, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'gen'))
import common_v13 as cm  # noqa: E402

OUT = cm.OUT / 'figures'
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 8,
                     'axes.linewidth': 0.6, 'pdf.fonttype': 42})
COL = {'F0': '#4d4d4d', 'E': '#1b9e77', 'E5': '#7570b3', 'N': '#d95f02', 'IMM': '#e7298a', 'CK3': '#1f78b4', 'TG': '#66a61e',
       'PS': '#a6761d', 'NIMM': '#e7298a'}


PNG_DPI = 800


def save(fig, stem, inputs):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / (stem + '.pdf'), bbox_inches='tight')
    # The template asks for at least 300 dpi for color and grayscale figures and at least 600 dpi for line art, and Fig. 1
    # is close to line art (22 Nov 2026; brief notes\CLASS_SWITCH_BRIEF_v13.md, section 7, item 3). What counts is the
    # resolution at the printed width: the tight bounding box crops a figure (Fig. 1 to about 5.75 in) and the converter
    # then sets it at the full text width (6.97 in), so a file saved at 600 dpi prints at 495 to 529 dpi for the three wide
    # figures (and one saved at 300 dpi, as until now, at 247 to 264). Saved at 800 dpi, every figure has at least 660 dpi
    # at its printed width; the converter records the lowest value at each build. The layout does not change.
    png = OUT / (stem + '.png')
    fig.savefig(png, dpi=PNG_DPI, bbox_inches='tight')
    plt.close(fig)
    # Plain RGB (template lines 360 to 364: "All color figures should be generated in RGB or CMYK color space"; brief
    # notes\CLASS_SWITCH_BRIEF_v13.md, section 8). Matplotlib writes RGBA (PNG color type 6), which pdfLaTeX embeds with a
    # soft mask, so the picture is flattened on white and written again as RGB (color type 2), same pixels and same dpi.
    from PIL import Image
    with Image.open(png) as im:
        rgba = im.convert('RGBA')
    flat = Image.new('RGB', rgba.size, (255, 255, 255))
    flat.paste(rgba, mask=rgba.getchannel('A'))
    flat.save(png, dpi=(PNG_DPI, PNG_DPI))
    tr = {'figure': stem, 'script': str(pathlib.Path(__file__).name), 'inputs': {str(p): cm.sha256(p) for p in inputs}}
    (OUT / (stem + '_trace.json')).write_text(json.dumps(tr, indent=1), encoding='utf-8')
    print('written', stem)


# Review of the author round (Q7-N, O-14): Fig. 1 prints at 1.21 times its drawn size (the tight box is 5.75 in wide, the
# text width 6.97 in), so 6.6 pt drawn is 8 pt printed; the boxes were re-sized so that every label fits at that size.
FIG1_BODY_PT = 6.6


def fig1():
    fig, ax = plt.subplots(figsize=(7.16, 1.95))
    ax.set_xlim(-1.5, 101.8); ax.set_ylim(-3, 23); ax.axis('off')
    # Labels as the text spells them ("nonbraking", "retuned"), and pedestrian crossing named with the other scenario
    # families (22 Nov 2026; brief notes\CLASS_SWITCH_BRIEF_v13.md, section 6). Measured in a scratch preview: the four lines
    # are 58.3 pt wide in the 64.2 pt box, at the same 6 pt size as before.
    boxes = [(0.0, 16.0, 'Recorded runs', 'CARLA: lead braking,\ncut-in, nonbraking\nleads, pedestrian\ncrossing;\nnuScenes logs'),
             (18.5, 11.0, 'Detector', 'CenterPoint\nlidar'),
             (32.0, 17.0, 'Tracker', 'CANMOT CV (online);\nretuned CV, CA,\nIMM, adaptive noise'),
             (51.5, 16.0, 'Margin sources', 'F0, N, E, E5 and E5p,\nCK3, TG, PS, NA, AM'),
             (70.0, 12.5, 'Speed planner', 'candidate rows;\nmargin scale g\nswept'),
             (85.0, 16.0, 'Scoring', 'open loop on the\nlogged future;\nclosed loop in CARLA')]
    for x0, w, head, body in boxes:
        ax.add_patch(FancyBboxPatch((x0, 3), w, 17, boxstyle='round,pad=0.3,rounding_size=1.0', fc='#f2f2f2', ec='#333333', lw=0.6))
        ax.text(x0 + w / 2, 16.8, head, ha='center', va='center', fontsize=7.5, fontweight='bold')
        ax.text(x0 + w / 2, 9.5, body, ha='center', va='center', fontsize=FIG1_BODY_PT, linespacing=1.25)
    for (x0, w, _, _), (x1, _, _, _) in zip(boxes[:-1], boxes[1:]):
        ax.annotate('', xy=(x1 - 0.4, 11.5), xytext=(x0 + w + 0.4, 11.5), arrowprops=dict(arrowstyle='-|>', lw=0.7,
                    color='#333333', mutation_scale=7))
    px = boxes[4][0] + boxes[4][1] / 2; rx = boxes[0][0] + boxes[0][1] / 2
    ax.plot([px, px, rx], [2.6, -0.8, -0.8], color='#777777', lw=0.6, ls='--')
    ax.annotate('', xy=(rx, 2.6), xytext=(rx, -0.8), arrowprops=dict(arrowstyle='-|>', lw=0.6, color='#777777', ls='--',
                mutation_scale=6))
    ax.text((px + rx) / 2, -0.4, 'closed loop: the selected row drives the car', ha='center', va='bottom', fontsize=FIG1_BODY_PT,
            color='#555555')
    save(fig, 'fig1_method_v13', [pathlib.Path(__file__)])


def _vals(pkg):
    v, m = cm.load_export(pkg)
    return v, (m or {}).get('_path')


FIG2_POPS = [('all', 'All'), ('mov', 'Ego moving'), ('pre', 'Before braking'), ('brk', 'Braking')]
FIG2_SRC = ['N', 'NA', 'IMM', 'E5', 'AM', 'TG', 'CK3']
FIG2_COL = {'NA': '#e6ab02', 'AM': '#666666'}   # sources that have no colour of their own in COL


def fig2_shares(v, path):
    """Fallback Fig. 2 (no frontier curves exported): each source's share of the room by the lead's phase on the fresh
    lead-braking runs, with 95% intervals, from C's LB.<pop>.RR_<src> keys. The stopped phase is left out (its room is a small
    fraction of a point, so its shares are unstable); Supplement S5 prints it."""
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    n = len(FIG2_SRC)
    for j, (pop, lab) in enumerate(FIG2_POPS):
        for i, s in enumerate(FIG2_SRC):
            k = 'LB.%s.RR_%s' % (pop, s)
            if v.get(k) is None or not v.get(k + '.ci'):
                continue
            x = j + (i - (n - 1) / 2) * 0.11
            y, (lo, hi) = v[k], v[k + '.ci']
            ax.errorbar(x, y, yerr=[[y - lo], [hi - y]], fmt='o', ms=3, color=FIG2_COL.get(s, COL.get(s, '#999999')), lw=0.8,
                        label=s if j == 0 else None)
    ax.axhline(0, color='#bbbbbb', lw=0.6)
    ax.set_xticks(range(len(FIG2_POPS)))
    ax.set_xticklabels(['%s\n(%s pp)' % (lab, cm.fnum(v['LB.%s.R' % pop], 2)) for pop, lab in FIG2_POPS], fontsize=6.5)
    ax.set_ylabel('Share of the room'); ax.tick_params(labelsize=7)
    ax.legend(fontsize=6, frameon=False, ncol=7, loc='lower center', bbox_to_anchor=(0.5, 1.0), handletextpad=0.1,
              columnspacing=0.8)
    save(fig, 'fig2_shares_v13', [p for p in (path,) if p])


def fig2():
    v, path = _vals('C')
    if v and 'LB.frontier.F0' not in v and cm.fig2_mode() == 'shares' and 'LB.all.RR_CK3' in v:
        return fig2_shares(v, path)
    if not v or 'LB.frontier.F0' not in v:
        print('Fig. 2 skipped: C export has no frontiers yet'); return
    fv, fpath = _vals('F')
    insets = [('CI', v, 'Cut-in, event window')] + ([('F', fv, 'Real logs')] if fv and 'F.frontier.F0' in fv else [])
    fig, axes = plt.subplots(1, 1 + len(insets), figsize=(7.16, 2.2), gridspec_kw={'width_ratios': [2] + [1] * len(insets)})
    axes = list(axes) if hasattr(axes, '__len__') else [axes]
    for ax, (pre, d, title) in zip(axes, [('LB', v, 'Lead braking, fresh runs')] + insets):
        f0 = d['%s.frontier.F0' % pre]; e = d['%s.frontier.E' % pre]
        ax.fill_between(f0[0], e[1], f0[1], color='#1b9e77', alpha=0.12, lw=0, step='post')
        for s in ('F0', 'E', 'E5', 'N', 'IMM', 'CK3'):
            k = '%s.frontier.%s' % (pre, s)
            if k in d:
                ax.step(d[k][0], d[k][1], where='post', color=COL[s], lw=0.9, label=s)
        k = '%s.frontier.F0_IMM' % pre          # the IMM is compared with its own class average, not with F0
        if k in d:
            ax.step(d[k][0], d[k][1], where='post', color='#7a0177', lw=0.9, ls=(0, (3, 2)), label='F0 (IMM)', zorder=5)
        top = max(max(d[k][1]) for k in d if k.startswith(pre + '.frontier.'))
        if top == 0:                            # e.g. the cut-in event window: no wrong go at any caution
            ax.set_ylim(-0.1, 1.0)
            ax.text(0.5, 0.55, 'No wrong goes\nat any caution', transform=ax.transAxes, ha='center', fontsize=7)
        ax.set_title(title, fontsize=8); ax.set_xlabel('Caution (% of desired speed)')
    for ax in axes:
        ax.set_ylabel('Wrong goes (% of decisions)', fontsize=7)
    axes[0].legend(fontsize=6.5, frameon=False, ncol=2)
    for ax, lab in zip(axes, ('(a)', '(b)', '(c)')):
        ax.text(0.5, -0.27, lab, transform=ax.transAxes, fontsize=8, ha='center', va='top')
    save(fig, 'fig2_frontiers_v13', [p for p in (path, fpath) if p])


def fig3():
    v, path = _vals('E')
    if not v or v.get('E.status') != 'ran' or 'E3.N.lo.dc' not in v:
        print('Fig. 3 skipped: no closed-loop comparison in the E export'); return
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    for lev, filled in (('lo', True), ('hi', False)):
        for a in ('N', 'CK3', 'TG', 'PS', 'NIMM'):
            k = 'E3.%s.%s' % (a, lev)
            if k + '.dc' not in v:
                continue
            x, y = v[k + '.dt'], v[k + '.dc']
            xe = [[x - v[k + '.dt.ci'][0]], [v[k + '.dt.ci'][1] - x]]; ye = [[y - v[k + '.dc.ci'][0]], [v[k + '.dc.ci'][1] - y]]
            ax.errorbar(x, y, xerr=xe, yerr=ye, fmt='o', ms=4, mfc=COL[a] if filled else 'white', mec=COL[a], ecolor=COL[a],
                        lw=0.7, label=('IMM' if a == 'NIMM' else a) if lev == 'lo' else None)
    ax.axhline(0, color='#999999', lw=0.5); ax.axvline(0, color='#999999', lw=0.5)
    ax.set_xlabel('Difference in time lost from F0 (s)'); ax.set_ylabel('Difference in contact share from F0')
    ax.legend(fontsize=7, frameon=False)
    save(fig, 'fig3_closedloop_v13', [path])


def fig4():
    """Values through the build's value store, so the rename map applies (B7 from CD; terciles from B)."""
    import values_v13 as vv
    s = vv.Store()
    g = lambda pkg, name: s(pkg, name)
    if g('B', 'B7.2.0.R') is None or g('C', 'LB.RS.1.0.6.rel') is None:
        print('Fig. 4 skipped: B7 or reaction-and-stop values missing'); return
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.16, 2.2))
    fig.subplots_adjust(wspace=0.55)   # room for (a)'s right-hand axis label (claim audit v02, finding 20)
    a1b = a1.twinx()
    for L, mk in (('0', 'o'), ('0.1', 's'), ('0.2', '^')):
        rs = [r for r in ('2', '5', '10') if g('B', 'B7.%s.%s.R' % (r, L)) is not None]
        a1.plot([int(r) for r in rs], [g('B', 'B7.%s.%s.R' % (r, L)) for r in rs], marker=mk, color='#1b9e77', lw=0.8,
                label='room, %s s' % L)
        a1b.plot([int(r) for r in rs], [g('B', 'B7.%s.%s.as_room' % (r, L)) for r in rs], marker=mk, color='#d95f02', lw=0.8,
                 ls='--', label='after-stop room, %s s' % L)
    a1.set_xlabel('Update rate (Hz)'); a1.set_ylabel('Room (percentage points)', color='#1b9e77')
    a1b.set_ylabel('After-stop room (decision-equivalents)', color='#d95f02')
    # Review of the author round (O-14, Q7-N): the legend is legible at the printed size (7.1 pt drawn is 8 pt printed): two
    # entries for the two quantities and three for the latencies' markers, in place of six small ones.
    from matplotlib.lines import Line2D
    hs = [Line2D([], [], color='#1b9e77', lw=0.8, label='room'),
          Line2D([], [], color='#d95f02', lw=0.8, ls='--', label='after-stop room'),
          Line2D([], [], color='#555555', lw=0, marker='o', ms=3.5, label='0 s'),
          Line2D([], [], color='#555555', lw=0, marker='s', ms=3.5, label='0.1 s'),
          Line2D([], [], color='#555555', lw=0, marker='^', ms=3.5, label='0.2 s latency')]
    a1.legend(handles=hs, fontsize=7.1, frameon=False, ncol=5, loc='upper center', bbox_to_anchor=(0.5, -0.27),
              columnspacing=0.7, handletextpad=0.3, handlelength=1.6)   # below the panel, off the data
    taus = [t for t in ('0.5', '0.75', '1.0', '1.25', '1.5', '1.8') if g('C', 'LB.RS.%s.6.rel' % t) is not None]
    y = [g('C', 'LB.RS.%s.6.rel' % t) for t in taus]
    ci = [g('C', 'LB.RS.%s.6.rel.ci' % t) or [v, v] for t, v in zip(taus, y)]
    a2.errorbar([float(t) for t in taus], y, yerr=[[v - c[0] for v, c in zip(y, ci)], [c[1] - v for v, c in zip(y, ci)]],
                fmt='o-', color='#333333', ms=3, lw=0.8, label='all')
    for i, col in zip(('1', '2', '3'), ('#a6cee3', '#1f78b4', '#08306b')):
        if g('C', 'LB.T%s.rel' % i) is not None:
            a2.plot([0.75], [g('C', 'LB.T%s.rel' % i)], 'D', color=col, ms=4, label='tercile %s' % i)
    a2.set_xlabel('Reaction time (s)'); a2.set_ylabel('Room relative to 3 s'); a2.legend(fontsize=6, frameon=False)
    for ax, lab in ((a1, '(a)'), (a2, '(b)')):
        # sub-figure labels centered below each panel, 8 pt, not bold (template line 424; final review, Q7-9, 22 Nov 2026)
        ax.text(0.5, -0.42, lab, transform=ax.transAxes, fontsize=8, ha='center', va='top')
    save(fig, 'fig4_conditions_v13', [p for p in (s.meta.get('B') or {}, s.meta.get('C') or {}) if p for p in [p.get('_path')] if p])

if __name__ == '__main__':
    fig1(); fig2(); fig3(); fig4()
