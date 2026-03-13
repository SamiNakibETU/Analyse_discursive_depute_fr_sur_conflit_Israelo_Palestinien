// ═══════════════════════════════════════════════════════════════════
// eventMatrix.js — Planche 1.04 · Matrice des chocs
// Table analytique : lignes = événements, colonnes = blocs
// Forme justifiée : présence/absence (sig/non-sig) + amplitude + direction
// Le × gris EST la donnée principale — l'absence de réaction est le message
// ═══════════════════════════════════════════════════════════════════

import * as d3 from 'd3';
import { CFG } from '../config.js';
import { makeSVG, hRule } from '../utils.js';

export function renderEventMatrix(containerId, rawData) {
  const { COL, FONT, STK, BLOCS, FMT, CW, LBL } = CFG;

  // ── Données ─────────────────────────────────────────────────────
  // rawData: [{event, code, GRAD_diff, GRAD_sig, GMOD_diff, ...}, ...]
  const BLOC_KEYS = ['GRAD', 'GMOD', 'CTR', 'DRT'];

  // ── Layout ──────────────────────────────────────────────────────
  const W      = CW;
  const LBLW   = 100;             // colonne labels événements
  const cW     = Math.floor((W - LBLW) / BLOCS.length); // 190px par bloc
  const ROW_H  = 44;
  const HDR_H  = 42;
  const B      = 4;
  const H      = HDR_H + rawData.length * ROW_H + B;

  const svg = makeSVG(containerId, W, H);

  // ── Filet supérieur ──────────────────────────────────────────────
  hRule(svg, 0, W, 0, STK.heavy, COL.ink);

  const g = svg.append('g').attr('transform', `translate(${LBLW}, 0)`);

  // ── En-têtes colonnes (codes de blocs) ───────────────────────────
  BLOCS.forEach((bloc, ci) => {
    const cx = ci * cW + cW / 2;

    // Séparateur vertical entre colonnes
    if (ci > 0) {
      g.append('line')
        .attr('x1', ci * cW).attr('x2', ci * cW)
        .attr('y1', 0).attr('y2', HDR_H + rawData.length * ROW_H)
        .attr('stroke', COL.rule).attr('stroke-width', STK.ghost);
    }

    // Code du bloc
    g.append('text')
      .attr('x', cx).attr('y', HDR_H - 8)
      .attr('text-anchor', 'middle')
      .attr('font-family', FONT.title).attr('font-size', 11)
      .attr('font-weight', 700).attr('fill', COL.ink)
      .attr('letter-spacing', '.05em').text(bloc);

    // Annotation synthèse (nombre de réactions significatives)
    const nSig = rawData.filter(d => d[`${BLOC_KEYS[ci]}_sig`] !== '').length;
    g.append('text')
      .attr('x', cx).attr('y', HDR_H - 22)
      .attr('text-anchor', 'middle')
      .attr('font-family', FONT.mono).attr('font-size', 7.5)
      .attr('fill', nSig > 0 ? COL.ruleHeavy : COL.struct)
      .text(nSig + ' / 6 sig.');
  });

  // ── Filet sous les en-têtes ──────────────────────────────────────
  hRule(g, -LBLW, BLOCS.length * cW, HDR_H, STK.med, COL.ink);

  // ── Lignes de données ────────────────────────────────────────────
  rawData.forEach((row, ei) => {
    const y  = HDR_H + ei * ROW_H;
    const cy = y + ROW_H / 2;

    // Séparateur entre événements
    if (ei > 0) {
      hRule(g, -LBLW, BLOCS.length * cW, y, STK.ghost, COL.rule);
    }

    // Étiquette événement (2 lignes : code + nom)
    g.append('text')
      .attr('x', -8).attr('y', cy - 4)
      .attr('text-anchor', 'end')
      .attr('font-family', FONT.mono).attr('font-size', 9)
      .attr('font-weight', 700).attr('fill', COL.ink)
      .text(row.code);
    g.append('text')
      .attr('x', -8).attr('y', cy + 8)
      .attr('text-anchor', 'end')
      .attr('font-family', FONT.mono).attr('font-size', 8.5)
      .attr('fill', COL.struct).text(row.event);

    // ── Cellules ──────────────────────────────────────────────────
    BLOC_KEYS.forEach((key, ci) => {
      const cx   = ci * cW + cW / 2;
      const diff = row[`${key}_diff`];
      const sig  = row[`${key}_sig`] || '';

      if (sig === '') {
        // × NON-SIGNIFICATIF — gris, grand format, clairement lisible
        g.append('text')
          .attr('x', cx).attr('y', cy + 7)
          .attr('text-anchor', 'middle')
          .attr('font-family', FONT.mono).attr('font-size', 22)
          .attr('fill', COL.cross).text('\u00D7'); // ×
      } else {
        // Valeur SIGNIFICATIVE : signe typographique + chiffre + étoiles
        const n    = +diff;
        const sign = n > 0 ? '+' : '\u2212'; // + ou − unicode
        const abs  = Math.abs(n).toFixed(2);

        g.append('text')
          .attr('x', cx).attr('y', cy + 5)
          .attr('text-anchor', 'middle')
          .attr('font-family', FONT.mono).attr('font-size', 14)
          .attr('font-weight', 700).attr('fill', COL.ink)
          .text(sign + abs);

        // Étoiles de significativité (en exposant, légèrement décalées)
        g.append('text')
          .attr('x', cx + 22).attr('y', cy - 2)
          .attr('font-family', FONT.mono).attr('font-size', 9)
          .attr('fill', COL.ink).text(sig);
      }
    });
  });

  // ── Filet inférieur ──────────────────────────────────────────────
  hRule(g, -LBLW, BLOCS.length * cW,
    HDR_H + rawData.length * ROW_H, STK.med, COL.ink);
}
