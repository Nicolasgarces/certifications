import { useEffect } from 'react';
import { useForm } from 'react-hook-form'
import { createCertifications, deleteCertifications, updateCertifications, getCertification, getCertificationPdf } from '../api/certifications.api'
import { useNavigate, useParams } from "react-router-dom";
import { toast } from 'react-hot-toast'

export function CertificationsFormPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue
  } = useForm()

  const navigate = useNavigate()
  const params = useParams()

  const onSubmit = handleSubmit(async data => {
    if (params.id) {
      await updateCertifications(params.id, data)
      toast.success('Certificación Actualizada', {
        style: {
          background: "#101010",
          color: "#fff"
        }
      })
    } else {
      await createCertifications(data);
    }
    navigate("/certifications")
  });

  useEffect(() => {
    async function loadCertification() {
      if (params.id) {
        const { data } = await getCertification(params.id)
        setValue('name', data.name)
        setValue('id_number', data.id_number)
        setValue('city', data.city)
        setValue('position', data.position)
        setValue('start_date', data.start_date)
        setValue('salary', data.salary)
      }
    }
    loadCertification()
  }, [])

  const handleDownload = async () => {
    try {
      const response = await getCertificationPdf(params.id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `certificado_${params.id}.pdf`);
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
    <div className='max-w-xl mx-auto'>
      <form onSubmit={onSubmit}>
        <input type="text" placeholder="Nombre"
          {...register("name", { required: true })}
          className='bg-zinc-700 p-3 rounded-lg block w-full mb-3' />
        {errors.name && <span>El Nombre es requerido</span>}

        <input type="text" placeholder="Identificación"
          {...register("id_number", { required: true })}
          className='bg-zinc-700 p-3 rounded-lg block w-full mb-3' />
        {errors.id_number && <span>La Identificación es requerida</span>}

        <input type="text" placeholder="Ciudad"
          {...register("city", { required: true })}
          className='bg-zinc-700 p-3 rounded-lg block w-full mb-3' />
        {errors.city && <span>La Ciudad es requerida</span>}

        <input type="text" placeholder="Cargo"
          {...register("position", { required: true })}
          className='bg-zinc-700 p-3 rounded-lg block w-full mb-3' />
        {errors.position && <span>El Cargo es requerido</span>}

        <input type="date" placeholder="Fecha de Ingreso"
          {...register("start_date", { required: true })}
          className='bg-zinc-700 p-3 rounded-lg block w-full mb-3' />
        {errors.start_date && <span>La Fecha de Ingreso es requerida</span>}

        <input type="number" placeholder="Salario"
          {...register("salary", { required: true })}
          className='bg-zinc-700 p-3 rounded-lg block w-full mb-3' />
        {errors.salary && <span>El Salario es requerido</span>}

        <button
          className='bg-indigo-500 p-3 rounded-lg block w-full mt-3'>Guardar</button>
      </form>

      {params.id && (
        <>
          <button
            className='bg-red-500 p-3 rounded-lg block w-full mt-3'
            onClick={async () => {
              const acepted = window.confirm('¿Estás Seguro?')
              if (acepted) {
                await deleteCertifications(params.id)
                toast.success('Certificación Eliminada', {
                  style: {
                    background: "#101010",
                    color: "#fff"
                  }
                })
                navigate("/certifications")
              }
            }}
          >
            Borrar
          </button>

          <button
            className='bg-green-500 p-3 rounded-lg block w-full mt-3'
            onClick={handleDownload}
          >
            Descargar
          </button>
        </>
      )}
    </div>
  )
}

export default CertificationsFormPage