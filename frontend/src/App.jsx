import { useState } from 'react'

const items = [
  {
    id: 1,
    title: 'Carteira marrom',
    category: 'Documentos',
    location: 'Biblioteca Central',
    time: 'Hoje, 14:20',
    status: 'Encontrado',
    tone: 'green',
  },
  {
    id: 2,
    title: 'Notebook Dell',
    category: 'Eletrônicos',
    location: 'Prédio 5',
    time: 'Hoje, 10:45',
    status: 'Perdido',
    tone: 'orange',
  },
  {
    id: 3,
    title: 'Garrafa verde',
    category: 'Acessórios',
    location: 'Ginásio',
    time: 'Ontem, 18:10',
    status: 'Encontrado',
    tone: 'blue',
  },
]

const iconPaths = {
  search: 'M21 21l-4.35-4.35m1.35-5.15a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z',
  grid: 'M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z',
  box: 'M21 8l-9-5-9 5 9 5 9-5zm-18 0v9l9 5 9-5V8M12 13v9',
  compass: 'M12 22a10 10 0 100-20 10 10 0 000 20zm3.3-13.3l-2.1 5.2-5.2 2.1 2.1-5.2 5.2-2.1z',
  user: 'M20 21a8 8 0 00-16 0m12-13a4 4 0 11-8 0 4 4 0 018 0z',
  bell: 'M18 8a6 6 0 00-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9zm-8 13h4',
  plus: 'M12 5v14M5 12h14',
  moon: 'M20.4 15.5A9 9 0 118.5 3.6a7 7 0 0011.9 11.9z',
  sun: 'M12 3v2m0 14v2M3 12h2m14 0h2M5.64 5.64l1.42 1.42m9.88 9.88l1.42 1.42m0-12.72l-1.42 1.42M7.06 16.94l-1.42 1.42M16 12a4 4 0 11-8 0 4 4 0 018 0z',
  pin: 'M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1116 0zm-8 3a3 3 0 100-6 3 3 0 000 6z',
  clock: 'M12 22a10 10 0 100-20 10 10 0 000 20zm0-16v6l4 2',
  arrow: 'M5 12h14m-5-5l5 5-5 5',
  logout: 'M10 17l5-5-5-5m5 5H3m11-9h6a2 2 0 012 2v14a2 2 0 01-2 2h-6',
}

function Icon({ name, size = 20 }) {
  return (
    <svg
      aria-hidden="true"
      className="icon"
      fill="none"
      height={size}
      viewBox="0 0 24 24"
      width={size}
    >
      <path d={iconPaths[name]} stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" />
    </svg>
  )
}

export default function App() {
  const [theme, setTheme] = useState('light')
  const [query, setQuery] = useState('')
  const [filter, setFilter] = useState('Todos')
  const [menuOpen, setMenuOpen] = useState(false)

  const visibleItems = items.filter((item) => {
    const matchesQuery = `${item.title} ${item.location} ${item.category}`.toLowerCase().includes(query.toLowerCase())
    const matchesFilter = filter === 'Todos' || item.status === filter
    return matchesQuery && matchesFilter
  })

  return (
    <div className="app-shell" data-theme={theme}>
      <aside className={`sidebar ${menuOpen ? 'is-open' : ''}`}>
        <div className="brand">
          <div className="brand-mark">
            <Icon name="search" size={23} />
          </div>
          <div>
            <strong>Achados</strong>
            <span>UFLA</span>
          </div>
        </div>

        <nav className="nav-list" aria-label="Navegação principal">
          <a className="nav-item active" href="#dashboard">
            <Icon name="grid" />
            <span>Visão geral</span>
          </a>
          <a className="nav-item" href="http://127.0.0.1:8000/items/">
            <Icon name="box" />
            <span>Objetos</span>
            <b>12</b>
          </a>
          <a className="nav-item" href="http://127.0.0.1:8000/items/?status=found">
            <Icon name="compass" />
            <span>Encontrados</span>
          </a>
          <a className="nav-item" href="http://127.0.0.1:8000/accounts/profile/">
            <Icon name="user" />
            <span>Meu perfil</span>
          </a>
        </nav>

        <div className="sidebar-footer">
          <button className="theme-toggle" type="button" onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
            <Icon name={theme === 'light' ? 'moon' : 'sun'} />
            <span>{theme === 'light' ? 'Modo escuro' : 'Modo claro'}</span>
          </button>
          <a className="logout-link" href="http://127.0.0.1:8000/accounts/logout/">
            <Icon name="logout" />
            <span>Sair</span>
          </a>
        </div>
      </aside>

      {menuOpen && <button className="sidebar-backdrop" aria-label="Fechar menu" onClick={() => setMenuOpen(false)} />}

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <button className="menu-button" type="button" aria-label="Abrir menu" onClick={() => setMenuOpen(true)}>
            <span />
            <span />
            <span />
          </button>
          <form className="search-box" action="http://127.0.0.1:8000/items/" method="get">
            <Icon name="search" size={19} />
            <input
              aria-label="Pesquisar objetos"
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Pesquisar objetos ou locais..."
              name="q"
              type="search"
              value={query}
            />
            <kbd>⌘ K</kbd>
          </form>
          <button className="notification-button" type="button" aria-label="Notificações">
            <Icon name="bell" size={20} />
            <span />
          </button>
          <div className="profile-chip" id="profile">
            <div className="avatar">JV</div>
            <div>
              <strong>José Victor</strong>
              <span>Estudante</span>
            </div>
          </div>
        </header>

        <section className="dashboard">
          <div className="welcome-row">
            <div>
              <p className="eyebrow">QUARTA-FEIRA, 19 DE NOVEMBRO</p>
              <h1>Bom dia, José! <span>👋</span></h1>
              <p>Veja o que aconteceu com os objetos da comunidade.</p>
            </div>
            <a className="primary-button" href="http://127.0.0.1:8000/items/create/">
              <Icon name="plus" size={18} />
              Cadastrar objeto
            </a>
          </div>

          <section className="stats-grid" aria-label="Resumo">
            <article className="stat-card">
              <div className="stat-icon green"><Icon name="box" /></div>
              <div>
                <span>Total de objetos</span>
                <strong>12</strong>
              </div>
              <small className="positive">+3 esta semana</small>
            </article>
            <article className="stat-card">
              <div className="stat-icon orange"><Icon name="compass" /></div>
              <div>
                <span>Encontrados</span>
                <strong>8</strong>
              </div>
              <small>66% do total</small>
            </article>
            <article className="stat-card">
              <div className="stat-icon blue"><Icon name="clock" /></div>
              <div>
                <span>Pendentes</span>
                <strong>3</strong>
              </div>
              <small>Aguardando contato</small>
            </article>
            <article className="stat-card">
              <div className="stat-icon purple"><Icon name="user" /></div>
              <div>
                <span>Devolvidos</span>
                <strong>7</strong>
              </div>
              <small className="positive">58% de sucesso</small>
            </article>
          </section>

          <section className="content-grid">
            <article className="panel activity-panel" id="items">
              <div className="panel-header">
                <div>
                  <p className="panel-kicker">ATIVIDADE RECENTE</p>
                  <h2>Objetos atualizados</h2>
                </div>
                <a href="http://127.0.0.1:8000/items/">Ver todos <Icon name="arrow" size={16} /></a>
              </div>

              <div className="filter-row" role="group" aria-label="Filtrar objetos">
                {['Todos', 'Encontrado', 'Perdido'].map((option) => (
                  <button
                    className={filter === option ? 'active' : ''}
                    key={option}
                    onClick={() => setFilter(option)}
                    type="button"
                  >
                    {option}
                  </button>
                ))}
              </div>

              <div className="item-list">
                {visibleItems.map((item) => (
                  <article className="item-row" key={item.id}>
                    <div className={`item-thumb ${item.tone}`}>
                      <Icon name="box" size={22} />
                    </div>
                    <div className="item-info">
                      <strong>{item.title}</strong>
                      <span>{item.category}</span>
                    </div>
                    <div className="item-location">
                      <Icon name="pin" size={15} />
                      <span>{item.location}</span>
                    </div>
                    <span className={`status ${item.status.toLowerCase()}`}>{item.status}</span>
                    <time>{item.time}</time>
                    <button className="row-action" type="button" aria-label={`Abrir ${item.title}`}>•••</button>
                  </article>
                ))}
                {visibleItems.length === 0 && (
                  <div className="empty-state">
                    <Icon name="search" size={28} />
                    <strong>Nenhum objeto encontrado</strong>
                    <span>Tente outro termo ou filtro.</span>
                  </div>
                )}
              </div>
            </article>

            <aside className="panel overview-panel" id="found">
              <div className="panel-header">
                <div>
                  <p className="panel-kicker">ESTE MÊS</p>
                  <h2>Visão geral</h2>
                </div>
              </div>
              <div className="donut-wrap">
                <div className="donut">
                  <div>
                    <strong>58%</strong>
                    <span>devolvidos</span>
                  </div>
                </div>
              </div>
              <div className="legend">
                <div><i className="green-dot" /><span>Encontrados</span><strong>8</strong></div>
                <div><i className="orange-dot" /><span>Perdidos</span><strong>4</strong></div>
                <div><i className="blue-dot" /><span>Devolvidos</span><strong>7</strong></div>
              </div>
              <a className="admin-link" href="http://127.0.0.1:8000/">Abrir portal</a>
            </aside>
          </section>
        </section>
      </main>
    </div>
  )
}
