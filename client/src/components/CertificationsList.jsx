import { useEffect, useState } from "react"
import { getAllCertifications } from '../api/certifications.api'
import {CertificationsCard} from './CertificationsCard'

export function CertificationsList() {

  const [certifications, setCertifications] = useState([])

  useEffect(() => {
    async function loadCertifications(){
      const res = await getAllCertifications()
      setCertifications(res.data); 
    }
    loadCertifications()
  },[])


  return (
    <div className="grid grid-cols-3 gap-3">
      {certifications.map(certification=>(
        <CertificationsCard key={certification.id} certification={certification}/>
      ))}
    </div>
  )
}

export default CertificationsList