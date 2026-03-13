
/** @type {import('tailwindcss').Config} */
export default {
  content: [
  './index.html',
  './src/**/*.{js,ts,jsx,tsx}'
],
  theme: {
    extend: {
      colors: {
        deep: 'var(--bg-deep)',
        card: 'var(--bg-card)',
        subtle: 'var(--bg-subtle)',
        border: 'var(--border)',
        'text-primary': 'var(--text-primary)',
        'text-secondary': 'var(--text-secondary)',
        'text-muted': 'var(--text-muted)',
        'gauche-radicale': 'var(--gauche-radicale)',
        'gauche-moderee': 'var(--gauche-moderee)',
        centre: 'var(--centre)',
        droite: 'var(--droite)',
        'bloc-gauche': 'var(--bloc-gauche)',
        'bloc-droite': 'var(--bloc-droite)',
        accent: 'var(--accent)',
        positive: 'var(--positive)',
        negative: 'var(--negative)',
      },
      fontFamily: {
        sans: ['IBM Plex Sans', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        'card': '12px',
      },
      transitionDuration: {
        '150': '150ms',
        '200': '200ms',
      }
    },
  },
  plugins: [],
}
