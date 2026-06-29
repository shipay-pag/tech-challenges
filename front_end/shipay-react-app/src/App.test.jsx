import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

describe("App", () => {
  it("renderiza inicialmente a lista de produtos", () => {
    render(<App />);

    expect(screen.getByText("Cash In - COB")).toBeInTheDocument();
    expect(screen.getByText("Cash In - COBV")).toBeInTheDocument();
    expect(screen.getByText("Cash In - DUEDATE")).toBeInTheDocument();
    expect(screen.getByText("Cash In - CHARGE")).toBeInTheDocument();
    expect(screen.getByText("Cash Out - PAYMENT")).toBeInTheDocument();
  });

  it("filtra dinamicamente os produtos conforme o usuário digita", async () => {
    const user = userEvent.setup();

    render(<App />);

    const searchInput = screen.getByLabelText("Buscar produto");

    await user.type(searchInput, "payment");

    expect(screen.getByText("Cash Out - PAYMENT")).toBeInTheDocument();

    expect(screen.queryByText("Cash In - COB")).not.toBeInTheDocument();
    expect(screen.queryByText("Cash In - COBV")).not.toBeInTheDocument();
    expect(screen.queryByText("Cash In - DUEDATE")).not.toBeInTheDocument();
    expect(screen.queryByText("Cash In - CHARGE")).not.toBeInTheDocument();
  });

  it("filtra produtos sem diferenciar maiúsculas e minúsculas", async () => {
    const user = userEvent.setup();

    render(<App />);

    const searchInput = screen.getByLabelText("Buscar produto");

    await user.type(searchInput, "payment");

    expect(screen.getByText("Cash Out - PAYMENT")).toBeInTheDocument();
  });

  it("não renderiza produtos quando a busca não encontra resultados", async () => {
    const user = userEvent.setup();

    render(<App />);

    const searchInput = screen.getByLabelText("Buscar produto");

    await user.type(searchInput, "xyz");

    expect(screen.queryByText("Cash In - COB")).not.toBeInTheDocument();
    expect(screen.queryByText("Cash In - COBV")).not.toBeInTheDocument();
    expect(screen.queryByText("Cash In - DUEDATE")).not.toBeInTheDocument();
    expect(screen.queryByText("Cash In - CHARGE")).not.toBeInTheDocument();
    expect(screen.queryByText("Cash Out - PAYMENT")).not.toBeInTheDocument();
  });
});
