import Nav from "../components/Nav";

export default function Docs() {
  return (
    <div className="shell">
      <Nav />
      <main className="content">
        <div className="page-header">
          <div>
            <h1>Documentação da API</h1>
            <p>Swagger / OpenAPI da RestAPIFurb.</p>
          </div>
        </div>
        <div className="hint" style={{ marginBottom: 20 }}>
          A documentação é gerada pelo FastAPI e está disponível em <strong>/docs</strong>.
        </div>
        <a className="btn-primary" href="http://localhost:8080/docs" target="_blank" rel="noreferrer">
          Abrir Swagger UI
        </a>
      </main>
    </div>
  );
}