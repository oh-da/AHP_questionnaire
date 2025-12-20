# AHP Questionnaire - React Frontend

A modern React frontend for the AHP (Analytic Hierarchy Process) questionnaire application, redesigned with Hebrew RTL support and a clean, card-based interface.

## Features

- 🎨 Modern, clean UI with Tailwind CSS
- 🇮🇱 Full Hebrew language support with RTL layout
- 📱 Responsive design
- ⚡ Fast development with Vite
- 🎯 Pairwise comparison interface

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
│   │   └── Layout.jsx
│   ├── pages/          # Page components
│   │   ├── AHPQuestionnaire.jsx
│   │   └── Results.jsx
│   ├── utils/          # Utility functions
│   │   └── cn.js
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

## Design Features

The interface follows the provided screenshot design:

- Centered card layout
- Hebrew RTL text direction
- Clean white cards on gray background
- Criteria displayed as pill badges
- Prominent call-to-action buttons
- Settings panel for customizing criteria

## Next Steps

- [ ] Implement the pairwise comparison flow
- [ ] Add results calculation and visualization
- [ ] Connect to Python backend API
- [ ] Add data persistence
- [ ] Implement export functionality
