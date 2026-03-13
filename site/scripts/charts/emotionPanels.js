// ═══════════════════════════════════════════════════════════════════
// emotionPanels.js — Planche 1.05 · Registres émotionnels
// 4 panneaux homologues (2×2) — un par bloc politique
// Forme justifiée : classement + proportion intra-bloc, 4 lectures parallèles
// Même échelle pour tous → comparaison directe entre panneaux possible
// Affect dominant = couleur du bloc · autres = gris · × = absent
// ═══════════════════════════════════════════════════════════════════

import * as d3 from 'd3';
import { CFG } from '../config.js';
import { makeSVG, hRule, parseNum } from '../utils.js';

export function renderEmotionPanels(containerId, rawData) {
  const { COL, FONT, STK, BLOCS, FMT, CW } = CFG;

  // ── Données ─────────────────────────────────────────────────────
  // rawData: [{emotion, GRAD, GMOD, CTR, DRT}, ...]
  const BLOC_KEYS = ['GRAD', 'GMOD', 'CTR', 'DRT'];

  // Ordre stable des émotions : trié par max global descendant
  const emotions = rawData.map(d => ({
    label: d.emotion,
    vals:  BLOC_KEYS.map(k => parseNum(d[k])),
    globalMax: Math.max(...BLOC_KEYS.map(k => parseNum(d[k]) || 0)),
  })).sort((a, b) => b.globalMax - a.globalMax);

  // Max dominant par bloc (pour identifier la barre dominante)
  const blocMax = BLOC_KEYS.map((_k, ci) =>
    Math.max(...emotions.map(e => e.vals[ci] || 0))
  );

  // ── Layout ──────────────────────────────────────────────────────
  const W         = CW;                      // 860
  const COL_GAP   = 20;                      // gouttière entre panneaux
  const PANEL_W   = Math.floor((W - COL_GAP) / 2); // 420px par panneau
  const ROW_GAP   = 24;                      // gouttière entre les 2 rangées
  const LPAD      = 88;                      // largeur labels émotion dans chaque panneau
  const BPAD      = 6;                       // padding gauche de la barre
  const BAR_MAX   = PANEL_W - LPAD - BPAD - 34; // largeur max de barre (~292px)
  const MAX_SCALE = 65;                      // domaine de l'échelle X (même pour tous)
  const xScale    = d3.scaleLinear().domain([0, MAX_SCALE]).range([0, BAR_MAX]);
  const BAR_H     = 12;                      // épaisseur de la barre
  const ROW_H     = 24;                      // hauteur d'une ligne
  const HDR_H     = 28;                      // hauteur en-tête (code bloc)
  const PANEL_H   = HDR_H + emotions.length * ROW_H + 14; // ~228px
  const H         = 2 * PANEL_H + ROW_GAP;  // ~480px

  const svg = makeSVG(containerId, W, H);

  // ── 4 panneaux ──────────────────────────────────────────────────
  BLOCS.forEach((bloc, bi) => {
    const csvKey = BLOC_KEYS[bi];
    const bColor = COL.bloc[bloc];

    // Position du panneau dans la grille 2×2
    const col    = bi % 2;
    const row    = Math.floor(bi / 2);
    const panX   = col * (PANEL_W + COL_GAP);
    const panY   = row * (PANEL_H + ROW_GAP);

    const g = svg.append('g').attr('transform', `translate(${panX}, ${panY})`);

    // ── Filet supérieur ─────────────────────────────────────────
    hRule(g, 0, PANEL_W, 0, STK.med, COL.ink);

    // ── Code du bloc (en-tête panneau) ──────────────────────────
    g.append('text')
      .attr('x', LPAD + BPAD).attr('y', HDR_H - 7)
      .attr('font-family', FONT.title).attr('font-size', 13)
      .attr('font-weight', 700).attr('fill', COL.ink)
      .attr('letter-spacing', '.04em').text(bloc);

    // Barre de couleur sous le titre (repère visuel du bloc)
    g.append('rect')
      .attr('x', LPAD + BPAD).attr('y', HDR_H - 4)
      .attr('width', BAR_MAX).attr('height', 1.5)
      .attr('fill', bColor).attr('opacity', .6);

    // ── Filet sous l'en-tête ────────────────────────────────────
    hRule(g, 0, PANEL_W, HDR_H, STK.light, COL.rule);

    // ── Barres émotions ─────────────────────────────────────────
    emotions.forEach((em, ri) => {
      const val   = em.vals[bi];    // peut être null
      const y     = HDR_H + ri * ROW_H;
      const cy    = y + ROW_H / 2;
      const isDom = (val !== null) && (val === blocMax[bi]);

      // Séparateur entre lignes
      if (ri > 0) {
        hRule(g, 0, PANEL_W, y, STK.ghost, COL.rule);
      }

      // Étiquette émotion (gauche du panneau)
      g.append('text')
        .attr('x', LPAD - 6).attr('y', cy + 4)
        .attr('text-anchor', 'end')
        .attr('font-family', FONT.body).attr('font-size', 9.5)
        .attr('fill', isDom ? COL.ink : COL.struct)
        .attr('font-weight', isDom ? 500 : 400)
        .text(em.label);

      if (val === null) {
        // × absent du bloc
        g.append('text')
          .attr('x', LPAD + BPAD + 6).attr('y', cy + 5)
          .attr('font-family', FONT.mono).attr('font-size', 15)
          .attr('fill', COL.cross).text('\u00D7');
        return;
      }

      const bw = xScale(val);

      // Barre : couleur du bloc si dominante, gris clair sinon
      g.append('rect')
        .attr('x', LPAD + BPAD).attr('y', cy - BAR_H / 2)
        .attr('width', bw).attr('height', BAR_H)
        .attr('fill', isDom ? bColor : '#C8C2BC');

      // Valeur (dans la barre si dominante et barre assez large, sinon après)
      if (isDom) {
        const insideFit = bw >= 36;
        if (insideFit) {
          g.append('text')
            .attr('x', LPAD + BPAD + bw - 5).attr('y', cy + 4)
            .attr('text-anchor', 'end')
            .attr('font-family', FONT.mono).attr('font-size', 9)
            .attr('font-weight', 700).attr('fill', COL.onDark)
            .text(Math.round(val) + '%');
        } else {
          g.append('text')
            .attr('x', LPAD + BPAD + bw + 5).attr('y', cy + 4)
            .attr('font-family', FONT.mono).attr('font-size', 9)
            .attr('font-weight', 700).attr('fill', COL.ink)
            .text(Math.round(val) + '%');
        }
      } else if (val >= 5) {
        g.append('text')
          .attr('x', LPAD + BPAD + bw + 5).attr('y', cy + 4)
          .attr('font-family', FONT.mono).attr('font-size', 8)
          .attr('fill', COL.struct)
          .text(Math.round(val) + '%');
      }
    });

    // ── Filet inférieur du panneau ──────────────────────────────
    hRule(g, 0, PANEL_W,
      HDR_H + emotions.length * ROW_H, STK.med, COL.ink);
  });
}
