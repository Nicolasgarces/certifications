import axios from 'axios'

const certificationsApi = axios.create({
    baseURL: 'http://localhost:8000/certifications/api/certifications/',
})

export const getAllCertifications = () => certificationsApi.get("/")
export const createCertifications = (certification) => certificationsApi.post("/", certification)

