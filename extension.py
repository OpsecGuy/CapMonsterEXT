

class Extension:
    def __init__(self, driver_session):
        self.session = driver_session
        self.captcha_types = [
            "ReCaptcha2",
            "ReCaptcha3",
            "ReCaptchaEnterprise",
            "HCaptcha",
            "Turnstile",
            "GeeTest",
            "FunCaptcha",
            "ImageToText"
        ]
        
    def get_value(self, command: str):
        return self.session.execute_script(command)
    
    def set_value(self, command: str):
        self.session.execute_script(command)
    
    def extension_state(self):
        return self.get_value('return CMExtension.isEnabled;')
    
    def set_extension_state(self, value: bool):
        self.set_value(f'CMExtension.isEnabled = {str(value).lower()}')
    
    def get_global_var(self):
        return self.get_value('return CMExtension.globalVariable;')

    def set_global_var(self, value: str='CMExtension'):
        self.set_value(f"CMExtension.globalVariable = '{value}'")
        
    def get_client_key(self):
        return self.get_value('return CMExtension.clientKey;')
    
    def set_client_key(self, value: str):
        self.set_value(f"CMExtension.clientKey = '{value}'")
    
    def get_api_url(self):
        return self.get_value('return CMExtension.apiURL;')
    
    def set_api_url(self, value: str):
        # Default: https://api.capmonster.cloud
        self.set_value(f"CMExtension.apiURL = '{value}'")

    def get_enabled_solvers(self):
        return self.get_value('return CMExtension.captchaList;')

    def add_captcha_solver(self, solver: str):
        self.active_solvers = self.get_enabled_solvers()

        if solver in self.captcha_types and solver not in self.active_solvers:
            self.set_value(f"CMExtension.captchaList.push('{solver}')")
        else:
            print(f'Solver is not supported: {solver}\nAvailable list: {self.captcha_types}')

    def remove_captcha_solver(self, solver: str):
        self.active_solvers = self.get_enabled_solvers()

        if solver in self.captcha_types and solver not in self.active_solvers:
            self.set_value(f"CMExtension.captchaList.pop('{solver}')")
        else:
            print(f'Solver is not supported: {solver}\nAvailable list: {self.captcha_types}')
    
    def get_captcha_extra(self):
        """List of captchas that can be solved by clicks\n
        Token (SLOW) - 0\n
        Click (FAST) - 1)

        Returns:
            dict: {'FunCaptcha': 1, 'HCaptcha': 1, 'ReCaptcha2': 1}
        """

        return self.get_value('return CMExtension.captchaExtra')
    
    def set_captcha_extra(self, solver: str, value: int):
        """Enable token or by clicks solving mode for supported captcha types\n
        Token (SLOW) - 0\n
        Click (FAST) - 1)

        Example:
            ext.set_captcha_extra('FunCaptcha', 1)
        """

        self.set_value(f"CMExtension.captchaExtra['{solver}'] = {value}")
    
    def get_captcha_retry(self):
        return self.get_value('return CMExtension.repeatsCount')
    
    def set_captcha_retry(self, value: int):
        self.set_value(f'CMExtension.repeatsCount = {value}')
    
    def get_auto_clickable(self):
        """Shows the captchas that support auto start solver\n
        which automatically opens captcha window.

        Returns:
            dict: {FunCaptcha: true, HCaptcha: true, ReCaptcha2: true}
        """
        return self.get_value('return CMExtension.autoClick;')

    def set_auto_clickable(self, solver: str, value: bool):
        """Enables the ability to automatically open captcha window.

        Example:
            dict: {FunCaptcha: true, HCaptcha: true, ReCaptcha2: true}
        """
        self.set_value(f"CMExtension.autoClick['{solver}'] = {str(value).lower()}")

    def get_auto_solvable(self):
        """Shows the captchas that support auto solving\n

        Returns:
            dict: {FunCaptcha: true, HCaptcha: true, ReCaptcha2: true}
        """
        return self.get_value('return CMExtension.autoSolve;')
    
    def set_auto_solvable(self, solver: str, value: bool):
        """Enables ability to automatically start solver for given captcha.
        """
        self.set_value(f"CMExtension.autoSolve['{solver}'] = {str(value).lower()}")

    def get_solver_button(self):
        try:
            return self.session.find_element(by=By.XPATH, value="//span[contains(text(),'Solve captcha')]")
        except Exception:
            return False

    def click_solver_button(self):
        try:
            self.session.find_element(by=By.XPATH, value="//span[contains(text(),'Solve captcha')]").click()
        except Exception:
            return False

    def is_solver_running(self) -> bool:
        command = 'return document.documentElement.innerText.indexOf("In process...")'
        return False if int(self.session.execute_script(command)) == -1 else True


