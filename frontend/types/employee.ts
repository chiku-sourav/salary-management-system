export interface Employee {
    id: number
    full_name: string
    country: string
    salary: number
    department: string
    job_title: string
}

export interface EmployeeResponse {
    items: Employee[]
    total: number
    page: number
    page_size: number
    total_pages: number
}