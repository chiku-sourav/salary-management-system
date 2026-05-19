"use client"

import { EmployeeTable } from "@/components/employees/employee-table"
import { api } from "@/lib/api"
import { useEffect, useState } from "react"

export default function EmployeesPage() {
    const [employees, setEmployees] = useState([])

    useEffect(() => {
        api.get("/employees")
            .then((res) => setEmployees(res.data))
    }, [])

    return (
        <EmployeeTable employees={employees} />
    )
}