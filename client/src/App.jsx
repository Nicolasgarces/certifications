import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom'
import {CertificationsPage} from './pages/CertificationsPage'
import {CertificationsFormPage} from './pages/CertificationsFormPage'
import {Navigation} from './components/Navigation'
import {Toaster} from 'react-hot-toast'

function App() {
  return (
    <BrowserRouter>
      <div className='container mx-auto'>
      <Navigation/>
      <Routes>
        {/* Con navigate redireccionamos a otras rutas  */}
        <Route path="/" element={<Navigate to="/certifications"/>} />
        <Route path="/certifications" element={<CertificationsPage/>} />
        <Route path="/certifications-create" element={<CertificationsFormPage/>} />
        <Route path="/certifications/:id" element={<CertificationsFormPage/>} />
      </Routes>
      <Toaster/>
      </div>
    </BrowserRouter>
  )
}

export default App