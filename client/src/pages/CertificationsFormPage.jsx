import {useForm} from 'react-hook-form'
import { createCertifications } from '../api/certifications.api'

export function CertificationsFormPage() {

  const {
    register,
    handleSubmit,
    formState:{
      errors
    }
  } = useForm()

  const onSubmit = handleSubmit(async data => {
   const res = await createCertifications(data)
   console.log(res);
  })

  return (
    <div>
      <form onSubmit={onSubmit}>
        <input type="text" placeholder="Nombre"
        {...register("nombre", {required: true})}
        />
        {errors.nombre && <span>El Nombre es requerido</span>}
        
        <input type="text" placeholder="Identificación"{...register("identificación", {required: true})}
        />
        {errors.identificación && <span>La Identificación es requerida</span>}

        <input type="text" placeholder="Ciudad"{...register("ciudad", {required: true})}
        />
        {errors.ciudad && <span>La Ciudad es requerida</span>}

        <input type="text" placeholder="Cargo"{...register("cargo", {required: true})}
        />
        {errors.cargo && <span>El Cargo es requerido</span>}

        <input type="date" placeholder="Fecha de Ingreso"{...register("fecha_ingreso", {required: true})}
        />
        {errors.fecha_ingreso && <span>La Fecha de Ingreso es requerida</span>}

        <input type="number" placeholder="Salario"{...register("salario", {required: true})}
        />
        {errors.salario && <span>El Salario es requerido</span>}

        <button>Guardar</button>
      </form>
    </div>
  )
}

export default CertificationsFormPage