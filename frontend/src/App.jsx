import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import AHPQuestionnaire from './pages/AHPQuestionnaire';
import Results from './pages/Results';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/questionnaire" replace />} />
        <Route path="questionnaire" element={<AHPQuestionnaire />} />
        <Route path="results" element={<Results />} />
      </Route>
    </Routes>
  );
}

export default App;
