# Poker Equity Calculator

A modern web application for analyzing poker starting hand equities using Monte Carlo simulation. Built with Next.js, React, TypeScript, and Tailwind CSS.

**Live Demo:** [https://poker-equity-calculator-eta.vercel.app/](https://poker-equity-calculator-eta.vercel.app/)

## Features

- **Interactive Equity Heatmap**: Visualize all 169 starting hands with dynamic table size selection (2-6 players)
- **High-Precision Analysis**: Based on 100,000 Monte Carlo simulations per hand (±0.3% accuracy)
- **Equity Trends**: See how hand categories scale from heads-up to 6-max
- **Strategy Insights**: Data-driven recommendations for different positions

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Data**: Python Monte Carlo simulation (100k sims/hand, 84.5M total simulations)

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for running simulations)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/addice-Jeremy/poker-equity-calculator.git
cd poker-equity-calculator
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
poker-equity-calculator/
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── EquityHeatmap.tsx  # Interactive heatmap
│   ├── KeyInsights.tsx    # Insights cards
│   ├── EquityTrends.tsx   # Line chart
│   ├── HowToRead.tsx      # Guide section
│   ├── StrategyGuide.tsx  # Strategy cards
│   └── PokerOdds.tsx      # Odds calculator
├── python/                # Python simulation code
│   ├── poker_winrate_simulation.py
│   ├── generate_equity_data.py
│   └── equity_cache.json  # Pre-computed data
└── public/                # Static assets

```

## Data Generation

The equity data is pre-computed using Python Monte Carlo simulation:

```bash
cd python
python3 -m venv venv
source venv/bin/activate
pip install tqdm
python generate_equity_data.py --sims 100000
```

## Deployment

Deploy to Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/addice-Jeremy/poker-equity-calculator)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
