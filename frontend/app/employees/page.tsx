"use client"

import { EmployeeTable } from "@/components/employees/employee-table";
import { api } from "@/lib/api";
import { useEffect, useState } from "react";

export default function EmployeesPage() {
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api.get("/employees")
            .then((res) => setEmployees(res.data))
            .catch(() => {
                setError("Failed to load employees")
            })
            .finally(() => setLoading(false))
    }, []);

    if (loading) {
        return <div>Loading employees...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (!employees.length) {
        return <div>No employees found</div>;
    }

    return (
        <EmployeeTable employees={employees} />
    );
}