import { useEffect } from 'react'

export default function App() {
  const portalUrl = `${window.location.protocol}//${window.location.hostname}:8000/`

  useEffect(() => {
    window.location.replace(portalUrl)
  }, [portalUrl])

  return (
    <main className="portal-redirect">
      <a className="redirect-brand" href={portalUrl}>
        <span className="redirect-mark">A</span>
        <span>
          <strong>Achados</strong>
          <small>UFLA</small>
        </span>
      </a>
      <div className="redirect-copy">
        <p className="redirect-eyebrow">PORTAL DA COMUNIDADE</p>
        <h1>Levando você ao Achados UFLA.</h1>
        <p>O portal completo está abrindo. Se o redirecionamento não acontecer, use o botão abaixo.</p>
        <a className="redirect-button" href={portalUrl}>Abrir portal <span aria-hidden="true">→</span></a>
      </div>
      <span className="redirect-foot">Objetos, ocorrências e sua conta em um só lugar.</span>
    </main>
  )
}
