import {Link} from 'react-router-dom'

export function Navigation() {
  return (
    <div>
        <Link to="/certifications">
            <h1>Certificacion App</h1>
            </Link>
        <Link to="/certifications-create">Create Certification</Link>
        
    </div>
  )
}

export default Navigation