const themeKey = 'achados-theme'
const storedTheme = window.localStorage.getItem(themeKey)

if (storedTheme === 'dark' || storedTheme === 'light') {
  document.body.dataset.theme = storedTheme
}

document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
  const updateLabel = () => {
    const isDark = document.body.dataset.theme === 'dark'
    const label = button.querySelector('[data-theme-label]')
    if (label) label.textContent = isDark ? 'Modo claro' : 'Modo escuro'
    button.setAttribute('aria-pressed', String(isDark))
  }

  updateLabel()
  button.addEventListener('click', () => {
    const nextTheme = document.body.dataset.theme === 'dark' ? 'light' : 'dark'
    document.body.dataset.theme = nextTheme
    window.localStorage.setItem(themeKey, nextTheme)
    updateLabel()
  })
})

const menuToggle = document.querySelector('[data-menu-toggle]')
const menuClose = document.querySelector('[data-menu-close]')

if (menuToggle && menuClose) {
  const closeMenu = () => {
    document.body.classList.remove('menu-open')
    menuToggle.setAttribute('aria-expanded', 'false')
  }

  menuToggle.addEventListener('click', () => {
    const isOpen = document.body.classList.toggle('menu-open')
    menuToggle.setAttribute('aria-expanded', String(isOpen))
  })
  menuClose.addEventListener('click', closeMenu)
  document.querySelectorAll('.side-link').forEach((link) => {
    link.addEventListener('click', closeMenu)
  })
}
