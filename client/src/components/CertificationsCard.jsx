import { useNavigate } from "react-router-dom";
import { getCertificationPdf } from '../api/certifications.api';
import { toast } from 'react-hot-toast';
import { FaFileDownload } from "react-icons/fa";

export function CertificationsCard({ certification }) {
  const navigate = useNavigate();

  const handleDownload = async (event) => {
    event.stopPropagation();
    try {
      const response = await getCertificationPdf(certification.id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      // Cambia el nombre del archivo aquí
      const fileName = `Certificado_${certification.name.replace(/\s+/g, '_')}.pdf`;
      link.setAttribute('download', fileName);
      
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      toast.success('Certificado descargado correctamente', {
        style: {
          background: "#101010",
          color: "#fff"
        }
      });
    } catch (error) {
      console.error("Error al descargar el certificado:", error);
      toast.error('Error al descargar el certificado', {
        style: {
          background: "#101010",
          color: "#fff"
        }
      });
    }
  };

  return (
    <div 
      className="bg-zinc-800 p-3 hover:bg-zinc-700 hover:cursor-pointer"
      onClick={() => {
        navigate(`/certifications/${certification.id}`);
      }}
    >
      <div className="flex justify-between items-center">
        <h1 className="font-bold uppercase">{certification.name}</h1>
        <button
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded-lg"
          onClick={handleDownload}
        >
          <FaFileDownload />
        </button>
      </div>
    </div>
  );
}

export default CertificationsCard;