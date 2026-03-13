import fightingWords from './fighting_words.json';

export const blocColors: Record<string, string> = {
  'Gauche radicale': '#B42318',
  'Gauche moderee': '#B54708',
  'Centre / Majorite': '#175CD3',
  Droite: '#6941C6',
};

export const blocLabels: Record<string, string> = {
  'Gauche radicale': 'Gauche radicale',
  'Gauche moderee': 'Gauche moderee',
  'Centre / Majorite': 'Centre / Majorite',
  Droite: 'Droite',
};

export type FrameRow = {
  bloc: keyof typeof blocLabels;
  HUM: number;
  SEC: number;
  MOR: number;
  OTH: number;
};

export const frameRows: FrameRow[] = [
  { bloc: 'Gauche radicale', HUM: 77.22, SEC: 2.33, MOR: 8.13, OTH: 12.32 },
  { bloc: 'Gauche moderee', HUM: 64.05, SEC: 3.72, MOR: 8.88, OTH: 23.35 },
  { bloc: 'Centre / Majorite', HUM: 29.1, SEC: 30.58, MOR: 20.9, OTH: 19.42 },
  { bloc: 'Droite', HUM: 11.05, SEC: 44.81, MOR: 34.1, OTH: 10.04 },
];

export const lexicalContrast = fightingWords;

export const registerPositionCorrelation = 0.046;

export const tweetsPerDeputy = [
  { bloc: 'Gauche radicale', value: 122.1 },
  { bloc: 'Gauche moderee', value: 35.39 },
  { bloc: 'Droite', value: 19.83 },
  { bloc: 'Centre / Majorite', value: 16.86 },
] as const;

export const visibilityByQuintile = [
  { quintile: 'Q1 (moins visibles)', value: 1.0 },
  { quintile: 'Q2', value: 1.1 },
  { quintile: 'Q3', value: 1.01 },
  { quintile: 'Q4', value: 1.22 },
  { quintile: 'Q5 (plus visibles)', value: 1.57 },
] as const;

export const twitterVsAnByBloc = [
  { bloc: 'Centre / Majorite', delta: 0.03, p: 0.906, significant: false },
  { bloc: 'Droite', delta: -0.15, p: 0.517, significant: false },
  { bloc: 'Gauche moderee', delta: -0.42, p: 0.132, significant: false },
  { bloc: 'Gauche radicale', delta: 0.5, p: 0.011, significant: true },
] as const;

export const eventImpact = [
  { event: 'CIJ (janv. 2024)', bloc: 'Gauche radicale', delta: -0.05, p: 0.448 },
  { event: 'CIJ (janv. 2024)', bloc: 'Gauche moderee', delta: 0.33, p: 0.083 },
  { event: 'CIJ (janv. 2024)', bloc: 'Centre / Majorite', delta: -0.1, p: 0.339 },
  { event: 'CIJ (janv. 2024)', bloc: 'Droite', delta: 0.19, p: 0.4 },
  { event: 'Rafah (mai 2024)', bloc: 'Gauche radicale', delta: 0.12, p: 0.002 },
  { event: 'Rafah (mai 2024)', bloc: 'Gauche moderee', delta: 0.52, p: 0.001 },
  { event: 'Rafah (mai 2024)', bloc: 'Centre / Majorite', delta: 0.3, p: 0.031 },
  { event: 'Rafah (mai 2024)', bloc: 'Droite', delta: -0.22, p: 0.072 },
  { event: 'Cessez-le-feu (janv. 2025)', bloc: 'Gauche radicale', delta: -0.16, p: 0.037 },
  { event: 'Cessez-le-feu (janv. 2025)', bloc: 'Gauche moderee', delta: -0.33, p: 0.284 },
  { event: 'Cessez-le-feu (janv. 2025)', bloc: 'Centre / Majorite', delta: -0.59, p: 0.008 },
  { event: 'Cessez-le-feu (janv. 2025)', bloc: 'Droite', delta: -1.03, p: 0.008 },
] as const;

export const affectiveGap = [
  { month: '2023-10', value: 0.012 },
  { month: '2023-11', value: 0.02 },
  { month: '2023-12', value: 0.028 },
  { month: '2024-01', value: 0.027 },
  { month: '2024-02', value: 0.015 },
  { month: '2024-03', value: 0.017 },
  { month: '2024-04', value: 0.022 },
  { month: '2024-05', value: 0.027 },
  { month: '2024-06', value: 0.036 },
  { month: '2024-07', value: 0.035 },
  { month: '2024-08', value: 0.018 },
  { month: '2024-09', value: 0.018 },
  { month: '2024-10', value: 0.01 },
  { month: '2024-11', value: 0.019 },
  { month: '2024-12', value: 0.04 },
  { month: '2025-01', value: 0.04 },
  { month: '2025-02', value: 0.027 },
  { month: '2025-03', value: 0.017 },
  { month: '2025-04', value: 0.022 },
  { month: '2025-05', value: 0.029 },
  { month: '2025-06', value: 0.011 },
  { month: '2025-07', value: 0.022 },
  { month: '2025-08', value: 0.037 },
  { month: '2025-09', value: 0.024 },
  { month: '2025-10', value: 0.025 },
  { month: '2025-11', value: 0.034 },
  { month: '2025-12', value: 0.038 },
  { month: '2026-01', value: 0.067 },
];

export const mannKendallByBloc = [
  { bloc: 'Gauche radicale', tau: 0.19047619047619047, p: 0.16209473670855826 },
  { bloc: 'Gauche moderee', tau: -0.19098210422376907, p: 0.15472892348537853 },
  { bloc: 'Centre / Majorite', tau: 0.08994708994708994, p: 0.5179179428613762 },
  { bloc: 'Droite', tau: -0.11390738468263202, p: 0.39549402218646723 },
] as const;

export const wassersteinDriftSnapshots = [
  { month: '2023-10', gaucheRadicale: 0.0, gaucheModeree: 0.0, centreMajorite: 0.0, droite: 0.0 },
  { month: '2024-05', gaucheRadicale: 0.11546435128518973, gaucheModeree: 0.1425831202046036, centreMajorite: 0.0706636500754148, droite: 0.02896825396825395 },
  { month: '2024-12', gaucheRadicale: 0.13275005644615037, gaucheModeree: 0.11323529411764707, centreMajorite: 0.1014705882352941, droite: 0.21333333333333332 },
  { month: '2025-07', gaucheRadicale: 0.10086790429595871, gaucheModeree: 0.18823529411764706, centreMajorite: 0.05515496521189125, droite: 0.02716450216450214 },
  { month: '2025-12', gaucheRadicale: 0.09194437784703909, gaucheModeree: 0.2284313725490196, centreMajorite: 0.043977591036414576, droite: 0.029696969696969708 },
] as const;

export const entropicPolarizationSeries = [
  { month: '2023-10', value: 0.8382978873848583 },
  { month: '2023-11', value: 0.7741668149744538 },
  { month: '2023-12', value: 0.6055089246326147 },
  { month: '2024-01', value: 0.7154304554054514 },
  { month: '2024-02', value: 0.7206322806530361 },
  { month: '2024-03', value: 0.818690920825804 },
  { month: '2024-04', value: 0.7020726744884833 },
  { month: '2024-05', value: 0.627946305783156 },
  { month: '2024-06', value: 0.7862196981649714 },
  { month: '2024-07', value: 0.7951590107436803 },
  { month: '2024-08', value: 0.8832900974557781 },
  { month: '2024-09', value: 0.6218823102777602 },
  { month: '2024-10', value: 0.8124164530357971 },
  { month: '2024-11', value: 0.7050524956575235 },
  { month: '2024-12', value: 0.5081824233177212 },
  { month: '2025-01', value: 0.6554850036192769 },
  { month: '2025-02', value: 0.9030068174503602 },
  { month: '2025-03', value: 0.8317803819845829 },
  { month: '2025-04', value: 0.6238586581604644 },
  { month: '2025-05', value: 0.822316738222008 },
  { month: '2025-06', value: 0.7239525327471801 },
  { month: '2025-07', value: 0.707356026151066 },
  { month: '2025-08', value: 0.6968718894393049 },
  { month: '2025-09', value: 0.569500335870049 },
  { month: '2025-10', value: 0.7363509509347868 },
  { month: '2025-11', value: 0.6642164314792016 },
  { month: '2025-12', value: 0.7495209863092727 },
  { month: '2026-01', value: 0.732111787207598 },
] as const;

export const effectiveDimensionalitySeries = [
  { month: '2023-10', value: 2.559490257152955 },
  { month: '2023-11', value: 2.7319462683775653 },
  { month: '2023-12', value: 2.8371527533607517 },
  { month: '2024-01', value: 2.7196140792870986 },
  { month: '2024-02', value: 2.6952147843613323 },
  { month: '2024-03', value: 2.806815365465207 },
  { month: '2024-04', value: 2.7112995460670586 },
  { month: '2024-05', value: 2.8946130776745713 },
  { month: '2024-06', value: 2.8840033443032937 },
  { month: '2024-07', value: 2.895820782672112 },
  { month: '2024-08', value: 2.8653657119431526 },
  { month: '2024-09', value: 2.92617133605728 },
  { month: '2024-10', value: 2.8946290431428086 },
  { month: '2024-11', value: 2.8798753932855745 },
  { month: '2024-12', value: 2.9046362988438204 },
  { month: '2025-01', value: 2.929232275466596 },
  { month: '2025-02', value: 2.96265290259829 },
  { month: '2025-03', value: 2.8526600184645554 },
  { month: '2025-04', value: 2.912690442677865 },
  { month: '2025-05', value: 2.889354487818196 },
  { month: '2025-06', value: 2.8854507960413853 },
  { month: '2025-07', value: 2.914672650524401 },
  { month: '2025-08', value: 2.9101581982186246 },
  { month: '2025-09', value: 2.967394832385147 },
  { month: '2025-10', value: 2.864925950967949 },
  { month: '2025-11', value: 2.9326384959468816 },
  { month: '2025-12', value: 2.9308225052293615 },
  { month: '2026-01', value: 2.904124483723502 },
] as const;

export const emotionalRegisterByBloc = {
  'Gauche radicale': { indignation: 63.7, solidarite: 12.5, neutral: 11.4, grief: 7.4, anger: 4.1 },
  'Gauche moderee': { indignation: 37.1, neutral: 29.9, grief: 17.8, solidarite: 13.4, anger: 1.1 },
  'Centre / Majorite': { neutral: 43.9, indignation: 26.7, grief: 10.9, defiance: 9.4, solidarite: 5.5 },
  Droite: { defiance: 41.2, indignation: 36.5, neutral: 11.5, fear: 3.8, grief: 2.9 },
} as const;
