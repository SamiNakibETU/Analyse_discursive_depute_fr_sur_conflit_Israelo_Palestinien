// ═══════════════════════════════════════════════════════════════════
// framesStacked.js — Planche 1.01 · Cadres discursifs
// 100% stacked horizontal bar chart
// Forme justifiée : données = composition d'un tout (somme = 100%/bloc)
// Chaque barre montre simultanément le tout et les parties
// ═══════════════════════════════════════════════════════════════════

import * as d3 from 'd3';
import { CFG } from '../config.js';
import { makeSVG, hRule, blocLabel } from '../utils.js';

export function renderFramesStacked(containerId, rawData) {
  const { COL, FONT, STK, FRAMES, FRAME_LABELS, BLOCS, FMT, CW, LBL } = CFG;

  // ── Layout ──────────────────────────────────────────────────────
  const W      = CW;          // 860 — largeur viewBox
  const iW     = W - LBL - 6; // 778 — zone de données
  const BAR_H  = 38;
  const GAP    = 11;
  const T      = 30;           // top : espace pour la légende
  const B      = 26;           // bottom : espace pour les ticks d'axe
  const ROWS   = BLOCS.length; // 4
  const chartH = ROWS * BAR_H + (ROWS - 1) * GAP; // 163px
  const H      = T + chartH + B; // 219px

  const svg = makeSVG(containerId, W, H);

  // ── Légende ─────────────────────────────────────────────────────
  // Disposée sur deux lignes si nécessaire : 3 + 3 frames
  const LEG_ROWS = [FRAMES.slice(0, 3), FRAMES.slice(3)];
  LEG_ROWS.forEach((row, ri) => {
    let lx = 0;
    row.forEach(fr => {
      const lg = svg.append('g')
        .attr('transform', `translate(${LBL + lx}, ${8 + ri * 12})`);
      lg.append('rect')
        .attr('y', -8).attr('width', 8).attr('height', 8)
        .attr('fill', COL.frame[fr]);
      lg.append('text')
        .attr('x', 12).attr('y', 0)
        .attr('font-family', FONT.mono).attr('font-size', 7.5)
        .attr('fill', COL.struct)
        .text(`${fr}  ${FRAME_LABELS[fr]}`);
      lx += 200;
    });
  });

  const g = svg.append('g').attr('transform', `translate(${LBL}, ${T})`);

  // ── Grille verticale (derrière les barres) ──────────────────────
  [25, 50, 75].forEach(v => {
    g.append('line')
      .attr('x1', iW * v / 100).attr('x2', iW * v / 100)
      .attr('y1', 0).attr('y2', chartH)
      .attr('stroke', COL.rule).attr('stroke-width', STK.ghost)
      .attr('stroke-dasharray', '2,5');
  });

  // ── Ticks axe X (bas) ───────────────────────────────────────────
  [0, 25, 50, 75, 100].forEach(v => {
    g.append('text')
      .attr('x', iW * v / 100).attr('y', chartH + 18)
      .attr('text-anchor', 'middle')
      .attr('font-family', FONT.mono).attr('font-size', 7.5)
      .attr('fill', COL.struct).text(v + '%');
    if (v === 0 || v === 100) {
      g.append('line')
        .attr('x1', iW * v / 100).attr('x2', iW * v / 100)
        .attr('y1', chartH).attr('y2', chartH + 5)
        .attr('stroke', COL.struct).attr('stroke-width', STK.ghost);
    }
  });

  // ── Filet supérieur ─────────────────────────────────────────────
  hRule(g, 0, iW, 0, STK.med, COL.ink);

  // ── Barres ──────────────────────────────────────────────────────
  BLOCS.forEach((bloc, bi) => {
    const y       = bi * (BAR_H + GAP);
    const rowData = rawData.find(d => d.bloc === bloc) || {};

    // Séparateur entre blocs
    if (bi > 0) {
      hRule(g, 0, iW, y, STK.ghost, COL.rule);
    }

    // Étiquette du bloc (rail gauche du chart)
    blocLabel(svg, LBL - 8, T + y + BAR_H / 2 + 4, bloc);

    // Calcul précis des largeurs de segments (entiers, somme = iW exacte)
    const pcts    = FRAMES.map(fr => +(rowData[fr]) || 0);
    const pxArr   = pcts.map(p => Math.round(iW * p / 100));
    const usedPx  = pxArr.slice(0, -1).reduce((a, b) => a + b, 0);
    pxArr[pxArr.length - 1] = iW - usedPx; // correction d'arrondi sur le dernier

    let cx = 0;
    FRAMES.forEach((fr, fi) => {
      const pw  = pxArr[fi];
      const pct = pcts[fi];
      if (pw <= 0) { cx += pw; return; }

      // Rectangle du segment
      g.append('rect')
        .attr('x', cx).attr('y', y)
        .attr('width', pw).attr('height', BAR_H)
        .attr('fill', COL.frame[fr]);

      // Label à l'intérieur selon la place disponible
      if (pct >= 18 && pw >= 52) {
        // Grand segment : code + valeur
        g.append('text')
          .attr('x', cx + pw / 2).attr('y', y + BAR_H / 2 + 4)
          .attr('text-anchor', 'middle')
          .attr('font-family', FONT.mono).attr('font-size', 10)
          .attr('font-weight', 700).attr('fill', COL.onDark)
          .text(`${fr}  ${pct}%`);
      } else if (pct >= 9 && pw >= 26) {
        // Segment moyen : code seul
        g.append('text')
          .attr('x', cx + pw / 2).attr('y', y + BAR_H / 2 + 4)
          .attr('text-anchor', 'middle')
          .attr('font-family', FONT.mono).attr('font-size', 8)
          .attr('font-weight', 700).attr('fill', 'rgba(255,255,255,.75)')
          .text(fr);
      }
      // < 9% : pas de label (segment trop étroit)

      cx += pw;
    });
  });

  // ── Filet inférieur ─────────────────────────────────────────────
  hRule(g, 0, iW, chartH, STK.med, COL.ink);
}
