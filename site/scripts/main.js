// ═══════════════════════════════════════════════════════════════════
// main.js — Chargement des données et initialisation des planches
// Charge les 5 CSV en parallèle, puis délègue le rendu à chaque module.
// ═══════════════════════════════════════════════════════════════════

import * as d3 from 'd3';

import { renderFramesStacked } from './charts/framesStacked.js';
import { renderVolumeDotplot  } from './charts/volumeDotplot.js';
import { renderStanceSeries   } from './charts/stanceSeries.js';
import { renderEventMatrix    } from './charts/eventMatrix.js';
import { renderEmotionPanels  } from './charts/emotionPanels.js';

// Attendre que les fontes soient chargées pour éviter les décalages métriques
document.fonts.ready.then(async () => {
  try {
    // Chargement parallèle des 5 datasets
    const [frames, volume, stance, events, emotions] = await Promise.all([
      d3.csv('data/frames_par_bloc.csv'),
      d3.csv('data/vue_ensemble.csv'),
      d3.csv('data/stance_mensuel.csv'),
      d3.csv('data/event_impact_diff_in_diff.csv'),
      d3.csv('data/emotional_register.csv'),
    ]);

    // Rendu de chaque planche
    renderFramesStacked('chart-frames',   frames);
    renderVolumeDotplot ('chart-volume',  volume);
    renderStanceSeries  ('chart-stance',  stance);
    renderEventMatrix   ('chart-events',  events);
    renderEmotionPanels ('chart-emotions', emotions);

  } catch (err) {
    console.error('Erreur de chargement des données :', err);
    document.querySelectorAll('.chart-container').forEach(el => {
      el.innerHTML = '<p class="load-error">Données non chargées — serveur requis.</p>';
    });
  }
});
