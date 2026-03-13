// ═══════════════════════════════════════════════════════════════════
// utils.js — Helpers partagés par tous les modules de charts
// ═══════════════════════════════════════════════════════════════════

import * as d3 from 'd3';
import { CFG } from './config.js';

// Crée le SVG principal d'un chart avec viewBox fixe
export function makeSVG(containerId, viewW, viewH) {
  return d3.select('#' + containerId)
    .append('svg')
    .attr('viewBox', `0 0 ${viewW} ${viewH}`)
    .attr('class', 'chart-svg')
    .attr('role', 'img');
}

// Règle horizontale précise
export function hRule(sel, x1, x2, y, weight, color) {
  sel.append('line')
    .attr('x1', x1).attr('x2', x2)
    .attr('y1', y).attr('y2', y)
    .attr('stroke', color || CFG.COL.rule)
    .attr('stroke-width', weight || CFG.STK.light);
}

// Règle verticale précise
export function vRule(sel, x, y1, y2, weight, color) {
  sel.append('line')
    .attr('x1', x).attr('x2', x)
    .attr('y1', y1).attr('y2', y2)
    .attr('stroke', color || CFG.COL.rule)
    .attr('stroke-width', weight || CFG.STK.light);
}

// Étiquette de bloc (condensed bold, alignée à droite)
export function blocLabel(sel, x, y, code) {
  sel.append('text')
    .attr('x', x).attr('y', y)
    .attr('text-anchor', 'end')
    .attr('font-family', CFG.FONT.title)
    .attr('font-size', 11)
    .attr('font-weight', 700)
    .attr('letter-spacing', '.04em')
    .attr('fill', CFG.COL.ink)
    .text(code);
}

// Texte mono (chiffres, codes, sources)
export function monoText(sel, x, y, txt, opts = {}) {
  return sel.append('text')
    .attr('x', x).attr('y', y)
    .attr('text-anchor', opts.anchor || 'start')
    .attr('font-family', CFG.FONT.mono)
    .attr('font-size', opts.size || 10)
    .attr('font-weight', opts.bold ? 700 : 400)
    .attr('fill', opts.color || CFG.COL.ink)
    .attr('letter-spacing', opts.spacing || 0)
    .text(txt);
}

// Convertit les clés CSV (GRAD, GMOD) en labels d'affichage (G.RAD, G.MOD)
export function csvToBloc(key) {
  return CFG.CSV_BLOC_MAP[key] || key;
}

// Valeur numérique depuis CSV (vide → null, sinon float)
export function parseNum(v) {
  if (v === '' || v === null || v === undefined) return null;
  const n = +v;
  return isNaN(n) ? null : n;
}
