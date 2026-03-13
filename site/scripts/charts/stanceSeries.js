// ═══════════════════════════════════════════════════════════════════
// stanceSeries.js — Planche 1.03 · Trajectoires temporelles du stance
// 4 bandes small-multiples empilées, même axe X et Y partagé
// Forme justifiée : évolution dans le temps → profil = trajectoire
// Stabilité des extrêmes lisible d'un coup, oscillation du Centre visible
// ═══════════════════════════════════════════════════════════════════

import * as d3 from 'd3';
import { CFG } from '../config.js';
import { makeSVG, hRule, blocLabel, vRule } from '../utils.js';

// Événements à marquer sur toutes les bandes
const EVENTS = [
  { mois: '2024-01', code: 'E1', label: 'Ord. CIJ'   },
  { mois: '2024-05', code: 'E2', label: 'Off. Rafah' },
  { mois: '2024-10', code: 'E3', label: 'M. Sinwar'  },
  { mois: '2025-01', code: 'E5', label: 'CLF'        },
];

export function renderStanceSeries(containerId, rawData) {
  const { COL, FONT, STK, BLOCS, CW, LBL } = CFG;

  // ── Données ─────────────────────────────────────────────────────
  // rawData: [{mois, GRAD, GMOD, CTR, DRT}, ...]
  const MONTHS   = rawData.map(d => d.mois);
  const BLOC_KEYS = ['GRAD', 'GMOD', 'CTR', 'DRT']; // clés CSV

  // ── Layout ──────────────────────────────────────────────────────
  const W       = CW;
  const VAL_R   = 42;                  // espace valeur finale (droite)
  const iW      = W - LBL - VAL_R;    // 742 — zone de données
  const BAND_H  = 70;                  // hauteur d'une bande
  const EV_TOP  = 22;                  // espace au-dessus pour codes événements
  const B       = 28;                  // espace bas (ticks mois)
  const totalH  = BLOCS.length * BAND_H;
  const H       = EV_TOP + totalH + B;

  // Scales communs à toutes les bandes
  const xScale = d3.scalePoint()
    .domain(MONTHS)
    .range([0, iW])
    .padding(0.04);

  const yScale = d3.scaleLinear()
    .domain([-2.4, 2.4])
    .range([BAND_H, 0]);

  const svg = makeSVG(containerId, W, H);

  // ── Filet supérieur de la planche ─────────────────────────────
  hRule(svg, 0, W, 0, STK.heavy, COL.ink);

  const gMain = svg.append('g')
    .attr('transform', `translate(${LBL}, ${EV_TOP})`);

  // ── Codes événements (en-tête, au-dessus des bandes) ─────────
  EVENTS.forEach(ev => {
    const x = xScale(ev.mois);
    if (x == null) return;
    svg.append('text')
      .attr('x', LBL + x).attr('y', EV_TOP - 6)
      .attr('text-anchor', 'middle')
      .attr('font-family', FONT.mono).attr('font-size', 7.5)
      .attr('fill', COL.ruleHeavy).text(ev.code);
  });

  // ── Labels mois partagés (tous les 4 mois, en haut) ──────────
  MONTHS.filter((_, i) => i % 6 === 0).forEach(m => {
    svg.append('text')
      .attr('x', LBL + xScale(m)).attr('y', EV_TOP - 14)
      .attr('text-anchor', 'middle')
      .attr('font-family', FONT.mono).attr('font-size', 7)
      .attr('fill', COL.struct)
      .text(m.slice(2).replace('-', '.'));
  });

  // ── Traits événements (traversent toutes les bandes) ──────────
  EVENTS.forEach(ev => {
    const x = xScale(ev.mois);
    if (x == null) return;
    gMain.append('line')
      .attr('x1', x).attr('x2', x)
      .attr('y1', 0).attr('y2', totalH)
      .attr('stroke', COL.ruleHeavy).attr('stroke-width', STK.ghost)
      .attr('stroke-dasharray', '2,3');
  });

  // ── Bandes ────────────────────────────────────────────────────
  BLOCS.forEach((bloc, bi) => {
    const csvKey = BLOC_KEYS[bi];
    const offY   = bi * BAND_H;
    const bColor = CFG.COL.bloc[bloc];

    // Données de stance pour ce bloc
    const stData = rawData.map(d => ({ m: d.mois, s: +d[csvKey] }));

    // ── Filet haut de bande ──────────────────────────────────────
    hRule(gMain, 0, iW, offY, bi === 0 ? STK.med : STK.light,
          bi === 0 ? COL.ink : COL.rule);

    // ── Zéro (référence neutre, pointillé discret) ───────────────
    gMain.append('line')
      .attr('x1', 0).attr('x2', iW)
      .attr('y1', offY + yScale(0)).attr('y2', offY + yScale(0))
      .attr('stroke', COL.ink).attr('stroke-width', STK.ghost)
      .attr('stroke-dasharray', '1.5,5').attr('opacity', .35);

    // ── Graduation Y (première bande uniquement) ─────────────────
    if (bi === 0) {
      [-2, 0, 2].forEach(v => {
        gMain.append('text')
          .attr('x', -6).attr('y', offY + yScale(v) + 3)
          .attr('text-anchor', 'end')
          .attr('font-family', FONT.mono).attr('font-size', 7)
          .attr('fill', COL.struct)
          .text(v === 0 ? '0' : (v > 0 ? '+' + v : '\u2212' + Math.abs(v)));
      });
    }

    // ── Zone de remplissage (très légère, fonctionnelle) ─────────
    // Positive : légèrement coloré avec la couleur du bloc
    const areaPos = d3.area()
      .x(d => xScale(d.m))
      .y0(offY + yScale(0))
      .y1(d => offY + yScale(Math.max(d.s, 0)))
      .curve(d3.curveMonotoneX);

    // Négative : gris neutre
    const areaNeg = d3.area()
      .x(d => xScale(d.m))
      .y0(offY + yScale(0))
      .y1(d => offY + yScale(Math.min(d.s, 0)))
      .curve(d3.curveMonotoneX);

    gMain.append('path')
      .datum(stData).attr('d', areaPos)
      .attr('fill', bColor).attr('opacity', .08);

    gMain.append('path')
      .datum(stData).attr('d', areaNeg)
      .attr('fill', COL.ink).attr('opacity', .06);

    // ── Profil (ligne fine noire — la donnée principale) ─────────
    const line = d3.line()
      .x(d => xScale(d.m))
      .y(d => offY + yScale(d.s))
      .curve(d3.curveMonotoneX);

    gMain.append('path')
      .datum(stData).attr('d', line)
      .attr('fill', 'none')
      .attr('stroke', COL.ink).attr('stroke-width', 1.1);

    // ── Code bloc (gauche) ────────────────────────────────────────
    svg.append('text')
      .attr('x', LBL - 7).attr('y', EV_TOP + offY + BAND_H / 2 + 4)
      .attr('text-anchor', 'end')
      .attr('font-family', FONT.title).attr('font-size', 10)
      .attr('font-weight', 700).attr('fill', COL.ink)
      .attr('letter-spacing', '.04em').text(bloc);

    // ── Valeur finale (droite, précise) ───────────────────────────
    const lastPt = stData[stData.length - 1];
    svg.append('text')
      .attr('x', LBL + iW + 5)
      .attr('y', EV_TOP + offY + yScale(lastPt.s) + 3)
      .attr('font-family', FONT.mono).attr('font-size', 9)
      .attr('font-weight', 700).attr('fill', COL.ink)
      .text((lastPt.s > 0 ? '+' : '') + lastPt.s.toFixed(2));
  });

  // ── Filet inférieur ────────────────────────────────────────────
  hRule(gMain, 0, iW, totalH, STK.med, COL.ink);

  // ── Ticks mois (bas, tous les 4 mois) ────────────────────────
  MONTHS.filter((_, i) => i % 4 === 0).forEach(m => {
    gMain.append('line')
      .attr('x1', xScale(m)).attr('x2', xScale(m))
      .attr('y1', totalH).attr('y2', totalH + 5)
      .attr('stroke', COL.rule).attr('stroke-width', STK.light);
    gMain.append('text')
      .attr('x', xScale(m)).attr('y', totalH + 14)
      .attr('text-anchor', 'middle')
      .attr('font-family', FONT.mono).attr('font-size', 6.5)
      .attr('fill', COL.struct)
      .text(m.slice(2).replace('-', '.'));
  });
}
