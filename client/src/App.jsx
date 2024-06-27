import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom'
import {CertificationsPage} from './pages/CertificationsPage'
import {CertificationsFormPage} from './pages/CertificationsFormPage'
import {Navigation} from './components/Navigation'

function App() {
  return (
    <BrowserRouter>
      <Navigation/>
      <Routes>
        {/* Con navigate redireccionamos a otras rutas  */}
        <Route path="/" element={<Navigate to="/certifications"/>} />
        <Route path="/certifications" element={<CertificationsPage/>} />
        <Route path="/certifications-create" element={<CertificationsFormPage/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App