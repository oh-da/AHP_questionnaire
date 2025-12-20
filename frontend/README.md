# AHP Questionnaire - React Frontend

A modern React frontend for the AHP (Analytic Hierarchy Process) questionnaire application, redesigned with Hebrew RTL support and a clean, card-based interface.

## Features

- 🎨 Modern, clean UI with Tailwind CSS
- 🇮🇱 Full Hebrew language support with RTL layout
- 📱 Responsive design
- ⚡ Fast development with Vite
- 🎯 Interactive pairwise comparison interface with slider
- 📊 Real-time AHP weight calculation
- ✅ Consistency ratio checking (CR, CI, Lambda Max)
- 📈 Visual results display with bar charts
- 💾 Download results as JSON
- 🔄 Reset and restart functionality

## Prerequisites

- Node.js 18+
- npm or yarn

## Installation

```bash
cd frontend
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   │   ├── Layout.jsx          # Header and navigation
│   │   └── ComparisonFlow.jsx  # Pairwise comparison interface
│   ├── pages/          # Page components
│   │   ├── AHPQuestionnaire.jsx  # Welcome screen and questionnaire
│   │   └── Results.jsx           # Results visualization
│   ├── utils/          # Utility functions
│   │   ├── cn.js              # Class name utility
│   │   └── ahpCalculator.js   # AHP calculation logic
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Technology Stack

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Lucide React** - Icons

## How It Works

1. **Welcome Screen** - Enter your name and review criteria
2. **Pairwise Comparisons** - Compare each pair of criteria using an interactive slider
3. **Results** - View calculated weights, consistency metrics, and download results

## Design Features

The interface follows modern design principles:

- **Welcome Screen**: Centered card layout with criteria badges and settings panel
- **Comparison Flow**: Clean slider interface with progress tracking and navigation
- **Results Page**: Visual bar charts showing priority weights and consistency status

All screens support:
- Hebrew RTL text direction
- Responsive layout
- Smooth transitions and animations
- Accessible color contrast

## AHP Calculation

The app implements the full Analytic Hierarchy Process:

- **Geometric Mean Method** for weight calculation
- **Consistency Ratio (CR)** checking (threshold: 0.1)
- **Consistency Index (CI)** calculation
- **Lambda Max** eigenvalue approximation

Scale conversion: -8 (left criterion strongly preferred) to +8 (right criterion strongly preferred)

## Next Steps

To enhance the application, you could:

- [ ] Connect to Python backend API for data persistence
- [ ] Add GitHub Gist integration for cloud storage
- [ ] Implement CSV export alongside JSON
- [ ] Add user authentication
- [ ] Create admin dashboard for viewing all submissions
