import EmployeesPage from "@/app/employees/page"
import { api } from "@/lib/api"
import { fireEvent, render, screen, waitFor } from "@testing-library/react"

jest.mock("@/lib/api", () => ({
    api: {
        get: jest.fn()
    }
}))

jest.mock("@/components/employees/employee-table", () => ({
    EmployeeTable: ({ employees }: any) => (
        <div data-testid="employee-table">
            {employees.length} employees
        </div>
    )
}))

const mockedGet = api.get as jest.Mock

const mockResponse = {
    data: {
        items: [
            {
                id: 1,
                full_name: "John Doe"
            }
        ],
        total: 100
    }
}

describe("EmployeesPage", () => {
    beforeEach(() => {
        jest.clearAllMocks()

        process.env.NEXT_PUBLIC_API_URL =
            "http://localhost:8000"
    })

    test("shows loading initially", () => {
        mockedGet.mockReturnValue(new Promise(() => { }))

        render(<EmployeesPage />)

        expect(
            screen.getByText(/loading employees/i)
        ).toBeInTheDocument()
    })

    test("renders employee table after successful fetch", async () => {
        mockedGet.mockResolvedValue(mockResponse)

        render(<EmployeesPage />)

        expect(
            await screen.findByTestId("employee-table")
        ).toBeInTheDocument()

        expect(
            screen.getByText("1 employees")
        ).toBeInTheDocument()
    })

    test("calls API with correct pagination params", async () => {
        mockedGet.mockResolvedValue(mockResponse)

        render(<EmployeesPage />)

        await waitFor(() => {
            expect(mockedGet).toHaveBeenCalledWith(
                "http://localhost:8000/employees?page=1&page_size=20"
            )
        })
    })

    test("shows error when API fails", async () => {
        mockedGet.mockRejectedValue(new Error())

        render(<EmployeesPage />)

        expect(
            await screen.findByText(
                "Failed to load employees"
            )
        ).toBeInTheDocument()
    })

    test("shows empty state", async () => {
        mockedGet.mockResolvedValue({
            data: {
                items: [],
                total: 1
            }
        })

        render(<EmployeesPage />)

        expect(
            await screen.findByText(
                "No employees found"
            )
        ).toBeInTheDocument()
    })

    test("previous button disabled on first page", async () => {
        mockedGet.mockResolvedValue(mockResponse)

        render(<EmployeesPage />)

        const previous =
            await screen.findByRole("button", {
                name: /previous/i
            })

        expect(previous).toBeDisabled()
    })

    test("next button disabled on last page", async () => {
        mockedGet.mockResolvedValue({
            data: {
                items: [{ id: 1 }],
                total: 1
            }
        })

        render(<EmployeesPage />)

        const next =
            await screen.findByRole("button", {
                name: /next/i
            })

        expect(next).toBeDisabled()
    })

    test("clicking next loads next page", async () => {
        mockedGet.mockResolvedValue(mockResponse)

        render(<EmployeesPage />)

        await screen.findByTestId("employee-table")

        fireEvent.click(
            screen.getByRole("button", {
                name: /next/i
            })
        )

        await waitFor(() => {
            expect(mockedGet).toHaveBeenLastCalledWith(
                "http://localhost:8000/employees?page=2&page_size=20"
            )
        })
    })

    test("updates page indicator", async () => {
        mockedGet.mockResolvedValue({
            data: {
                items: [{ id: 1 }],
                total: 60
            }
        })

        render(<EmployeesPage />)

        await screen.findByText("Page 1 of 3")

        fireEvent.click(
            screen.getByRole("button", {
                name: /next/i
            })
        )

        await screen.findByText("Page 2 of 3")
    })
})