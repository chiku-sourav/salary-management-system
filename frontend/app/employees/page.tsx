"use client"

import { EmployeeTable } from "@/components/employees/employee-table"
import { api } from "@/lib/api"
import { Employee, EmployeeResponse } from "@/types/employee"
import { useEffect, useState } from "react"

export default function EmployeesPage() {
    const [employees, setEmployees] = useState<Employee[]>([])
    const [page, setPage] = useState(1)

    const [totalPages, setTotalPages] = useState(1)

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const pageSize = 20

    useEffect(() => { fetchEmployees() }, [page])

    async function fetchEmployees() {
        try {
            setLoading(true)
            setError("")

            const response = await api.get<EmployeeResponse>(
                `${process.env.NEXT_PUBLIC_API_URL}/employees?page=${page}&page_size=${pageSize}`
            )

            setEmployees(response.data.items)
            setTotalPages(Math.ceil(response.data.total / pageSize))

        } catch {
            setError("Failed to load employees")
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return <div className="p-4">Loading employees...</div>
    }

    if (error) {
        return <div className="p-4 text-red-500">{error}</div>
    }

    if (!employees?.length) {
        return <div className="p-4">No employees found</div>
    }

    return (
        <div className="space-y-4 p-4">

            <EmployeeTable employees={employees} />

            <div className="flex items-center gap-4">

                <button
                    className="border px-3 py-1 rounded disabled:opacity-50"
                    disabled={page === 1}
                    onClick={() => setPage((prev) => prev - 1)}
                >
                    Previous
                </button>

                <span>
                    Page {page} of {totalPages}
                </span>

                <button
                    className="border px-3 py-1 rounded disabled:opacity-50"
                    disabled={page === totalPages}
                    onClick={() => setPage((prev) => prev + 1)}
                >
                    Next
                </button>

            </div>
        </div>
    )
}