from selenium import webdriver
from selenium.webdriver.firefox import service, options

geckodriver_path = '/usr/local/bin/geckodriver' # Firefox's driver path


# Configurações opcionais
options = options.Options()
#options.add_argument("--headless") # executa sem abrir janela

# Inicializa o driver do Firefox
service = service.Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

# Abre a página
driver.get("http://localhost:3000/")

# Fecha o browser
#driver.quit()
