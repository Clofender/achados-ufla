export default function App() {
  return (
    <main className="welcome" aria-labelledby="page-title">
      <p className="eyebrow">Comunidade universitária</p>
      <h1 id="page-title">Achados UFLA</h1>
      <p className="intro">Um ponto de encontro para o que você perdeu.</p>
      <p>
        Nosso portal de objetos perdidos e encontrados está em desenvolvimento.
        A equipe já pode gerenciar os registros pela área administrativa.
      </p>
      <a className="admin-link" href="http://127.0.0.1:8000/admin/">
        Acessar administração
      </a>
    </main>
  )
}
