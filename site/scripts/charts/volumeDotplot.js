// ═══════════════════════════════════════════════════════════════════
// volumeDotplot.js — Planche 1.02 · Volume de production
// Double lollipop : textes/élu + ratio tweets/interventions
// Forme justifiée : quantités absolues comparées entre blocs identifiés
// Deux panels alignés → le lecteur lit la même structure deux fois
// ═══════════════════════════════════════════════════════════════════

import * as d3 from 'd3';
import { CFG } from '../config.js';
import { makeSVG, hRule, blocLabel, monoText } from '../utils.js';

export function renderVolumeDotplot(containerId, rawData) {
  const { COL, FONT, STK, BLOCS, FMT, CW, LBL } = CFG;

  // ── Données des deux panneaux ────────────────────────────────────
  const PANELS = [
    {
      label: 'TEXTES PARLEMENTAIRES · ÉLU',
      unit:  'textes / élu',
      vals:  BLOCS.map(b => ({ bloc: b, v: +(rawData.find(d => d.bloc === b) || {}).textes_elu || 0 })),
      maxDomain: 55,
      ticks: [0, 10, 20, 30, 40, 50],
    },
    {
      label: 'RATIO TWEETS · INTERVENTION AN',
      unit:  'tweets / intervention',
      vals:  BLOCS.map(b => ({ bloc: b, v: +(rawData.find(d => d.bloc === b) || {}).tweets_int || 0 })),
      maxDomain: 12,
      ticks: [0, 3, 6, 9, 12],
    },
  ];

  // ── Layout ──────────────────────────────────────────────────────
  const W        = CW;
  const iW       = W - LBL - 90;   // 694 — zone de données (90px pour valeur à droite)
  const ROW_H    = 30;
  const PANEL_H  = BLOCS.length * ROW_H; // 120px
  const PANEL_GAP = 48;
  const T        = 12;
  const B        = 10;
  const H        = T + PANELS.length * PANEL_H + (PANELS.length - 1) * PANEL_GAP + B; // 310px

  const svg = makeSVG(containerId, W, H);

  PANELS.forEach((pan, pi) => {
    const panY  = T + pi * (PANEL_H + PANEL_GAP);
    const xScale = d3.scaleLinear().domain([0, pan.maxDomain]).range([0, iW]);
    const g = svg.append('g').attr('transform', `translate(${LBL}, ${panY})`);

    // ── Label du panneau ──────────────────────────────────────────
    g.append('text')
      .attr('x', 0).attr('y', -10)
      .attr('font-family', FONT.mono).attr('font-size', 7.5)
      .attr('letter-spacing', '.09em').attr('fill', COL.struct)
      .text(pan.label);

    // ── Filet supérieur ───────────────────────────────────────────
    hRule(g, 0, iW + 85, 0, STK.med, COL.ink);

    // ── Ticks axe X (graduations légères en haut) ─────────────────
    pan.ticks.forEach(v => {
      const x = xScale(v);
      g.append('line')
        .attr('x1', x).attr('x2', x)
        .attr('y1', -5).attr('y2', PANEL_H)
        .attr('stroke', v === 0 ? COL.rule : COL.rule)
        .attr('stroke-width', v === 0 ? STK.light : STK.ghost)
        .attr('stroke-dasharray', v === 0 ? '' : '2,5');
      g.append('text')
        .attr('x', x).attr('y', -12)
        .attr('text-anchor', 'middle')
        .attr('font-family', FONT.mono).attr('font-size', 7)
        .attr('fill', COL.struct).text(v);
    });

    // ── Lollipops ─────────────────────────────────────────────────
    pan.vals.forEach((d, di) => {
      const cy     = di * ROW_H + ROW_H / 2;
      const bx     = xScale(d.v);
      const bColor = COL.bloc[d.bloc];

      // Séparateur horizontal entre blocs
      if (di > 0) {
        hRule(g, 0, iW + 85, di * ROW_H, STK.ghost, COL.rule);
      }

      // Étiquette du bloc
      blocLabel(svg, LBL - 8, panY + cy + 4, d.bloc);

      // Stem (tige mince du lollipop)
      g.append('line')
        .attr('x1', 0).attr('x2', bx - 7)
        .attr('y1', cy).attr('y2', cy)
        .attr('stroke', bColor).attr('stroke-width', 1.2)
        .attr('opacity', .35);

      // Point principal
      g.append('circle')
        .attr('cx', bx).attr('cy', cy)
        .attr('r', 7)
        .attr('fill', bColor);

      // Valeur numérique (à droite du point)
      g.append('text')
        .attr('x', bx + 14).attr('y', cy + 4)
        .attr('font-family', FONT.mono).attr('font-size', 13)
        .attr('font-weight', 700).attr('fill', bColor)
        .text(FMT.val1(d.v));

      // Unité en gris discret (1ère ligne seulement)
      if (di === 0) {
        g.append('text')
          .attr('x', iW + 85).attr('y', cy + 4)
          .attr('text-anchor', 'end')
          .attr('font-family', FONT.mono).attr('font-size', 7.5)
          .attr('fill', COL.struct).text(pan.unit);
      }
    });

    // ── Filet inférieur ───────────────────────────────────────────
    hRule(g, 0, iW + 85, PANEL_H, STK.med, COL.ink);
  });
}
