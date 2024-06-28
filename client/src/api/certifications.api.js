import axios from 'axios'

const certificationsApi = axios.create({
    baseURL: 'http://localhost:8000/certifications/api/certifications/',
})

export const getAllCertifications = () => certificationsApi.get("/")
export const getCertification = (id) => certificationsApi.get(`/${id}/`)
export const getCertificationPdf = (id) => certificationsApi.get(`/${id}/generate_certificate/`)
export const createCertifications = (certification) => certificationsApi.post("/", certification)
export const deleteCertifications = (id) => certificationsApi.delete(`/${id}`)
export const updateCertifications = (id, certifications) => certificationsApi.put(`/${id}/`, certifications)