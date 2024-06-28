import {Link} from 'react-router-dom'

export function Navigation() {
  return (
    <div className='flex justify-between py-3'>
        <Link to="/certifications">
            <h1 className='font-bold text-3xl mb-4'>Certificaciones App</h1>
            </Link>
        <button className='bg-indigo-500 px-3 py-2 rounded-lg' >
          <Link to="/certifications-create">Crear Certificación</Link>
        </button>   
        
    </div>
  )
}

export default Navigation