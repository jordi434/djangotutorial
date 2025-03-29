
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException

class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    #fixtures = ['testdb.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # comprovem que el títol de la pàgina és el què esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
        
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
        #print(self.selenium.page_source)
        # comprovem si hem aconseguit entrar a l'admin panel pel títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin")
       
        #a partir d'aquí és nou, anterior igual que activitat + el canvi enunciat EAC2

        # Anar a Users i afegir un nou usuari 
        #selenium.find_element(By.LINK_TEXT, "Users").click()
        #selenium.find_element(By.LINK_TEXT, "ADD USER").click()
        self.selenium.find_element(By.LINK_TEXT, "Users").click()
        self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()
        # Crear un nou usuari amb contrasenya
        self.selenium.find_element(By.NAME, "username").send_keys("jordi_staff")
        self.selenium.find_element(By.NAME, "password1").send_keys("jordi123")
        self.selenium.find_element(By.NAME, "password2").send_keys("jordi123")
        self.selenium.find_element(By.NAME, "_save").click()
        # Afegir permisos staff
        staff_checkbox = self.selenium.find_element(By.NAME, "is_staff")
        if not staff_checkbox.is_selected():
            staff_checkbox.click()
        # Guarda els canvis
        self.selenium.find_element(By.NAME, "_save").click()
        # Sortir del panell
        #self.selenium.find_element(By.LINK_TEXT, "Log out").click()

        try:
            #self.selenium.find_element(By.LINK_TEXT, "Log out")
            self.selenium.find_element(By.XPATH, "//button[text()='Log out']").click()

        except NoSuchElementException:
            assert False, "Error: no s'ha trobat l'enllaç de Log out. El login ha fallat."
        #logout
        self.selenium.get(f"{self.live_server_url}/admin/logout/")
        # Entrar amb el nou usuari crear de nom jordi_staff
        self.selenium.get(f"{self.live_server_url}/admin/login/")
        self.selenium.find_element(By.NAME, "username").send_keys("jordi_staff")
        self.selenium.find_element(By.NAME, "password").send_keys("jordi123")
        self.selenium.find_element(By.XPATH, "//input[@value='Log in']").click()
        # Comprovar accés al panell administració
        self.assertIn("Site administration", self.selenium.page_source)
        # Canviar la contrasenya
        self.selenium.get(f"{self.live_server_url}/admin/password_change/")
        self.assertIn("Change password", self.selenium.page_source)
        # Comprovar que no té altres permisos, per exemple, la gestió dels usuaris
        try:
            self.selenium.find_element(By.LINK_TEXT, "Users")
            assert False, "No hauria de veure el menú d'usuaris"
        except NoSuchElementException:
            pass

