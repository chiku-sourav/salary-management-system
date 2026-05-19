"use client"

import { Employee } from "@/types/employee"

interface Props {
    employees: Employee[]
}

export function EmployeeTable({ employees }: Props) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Country</th>
                    <th>Salary</th>
                    <th>Department</th>
                    <th>Title</th>
                </tr>
            </thead>

            <tbody>
                {employees.map((employee) => (
                    <tr key={employee.id}>
                        <td>{employee.full_name}</td>
                        <td>{employee.country}</td>
                        <td>{employee.salary}</td>
                        <td>{employee.department}</td>
                        <td>{employee.job_title}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    )
}