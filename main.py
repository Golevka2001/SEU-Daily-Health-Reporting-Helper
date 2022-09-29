import smtplib, time, os, time
import yaml
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from random import random

from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class ReportingHelper:

    def __init__(self):
        # MODIFY: use absolute path
        config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   'config.yml')

        if not os.path.exists(config_file):
            raise Exception('no such file of directory: ' + config_file)
        else:
            # new style configuration
            # print("DEBUG: use new style configuration")
            # MODIFY: use utf-8 to encode:
            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f.read())

            # when an item is missing, use default value.
            class Config:
                user_id = config.get("user_id")  # str -> list
                password = config.get("password")  # str -> list
                chrome_driver_path = config.get("chrome_driver_path",
                                                "/usr/bin/chromedriver")
                notification = config.get("notification", "no")  # str -> list
                notify_failure_only = config.get("notify_failure_only",
                                                 "no")  # str -> list
                from_addr = config.get("from_addr", "USER_NAME@seu.edu.cn")
                email_password = config.get("email_password")
                smtp_server = config.get("smtp_server", "smtp.seu.edu.cn")
                # ADD: port of smtp server:
                port = config.get("port", 25)
                to_addr = config.get("to_addr",
                                     "name@example.com")  # str -> list

            self.cfg = Config

    def _random_temp(self) -> str:
        """Generate random normal body temperature. [36.2, 36.7]

        Returns:
            normal body temperature
        """
        lb = 36.2
        x = random() / 2  # [0, 0.5]
        return str(round(lb + x, 1))

    def run(self):
        # ADD: judgement for item number of the lists in settings:
        user_count = len(self.cfg.user_id)
        if not (user_count == len(self.cfg.password) == len(
                self.cfg.notification) == len(self.cfg.notify_failure_only) ==
                len(self.cfg.to_addr)):
            raise Exception(
                "check the config file, all lists should have the same number of items."
            )

        options = Options()
        options.add_argument("--headless")  # headless browser
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')

        # MODIFY: add loop for different users in the list:
        for i in range(user_count):
            driver = Chrome(service=Service(self.cfg.chrome_driver_path),
                            options=options)

            driver.get(
                'https://newids.seu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.seu.edu.cn%2Fqljfwapp2%2Fsys%2FlwReportEpidemicSeu%2Findex.do%3Ft_s%3D1594447890898%26amp_sec_version_%3D1%26gid_%3DSTZiVXZjRnhVSS9VNERWaFNNT1hXb2VNY3FHTHFVVHMwRC9jdTdhUlllcXVkZDNrKzNEV1ZxeHVwSEloRVQ4NHZFVzRDdHRTVlZ1dEIvczVvdzVpVGc9PQ%26EMAP_LANG%3Dzh%26THEME%3Dindigo%23%2FdailyReport'
            )
            driver.find_element(By.ID, 'username').send_keys(
                self.cfg.user_id[i])  # student ID
            driver.find_element(By.ID, 'password').send_keys(
                self.cfg.password[i])  # password
            driver.find_element(
                By.XPATH,
                '//*[@class="auth_login_btn primary full_width"]').click()

            status = ""
            try:
                WebDriverWait(driver, 15, 0.2).until(lambda x: x.find_element(
                    By.XPATH, '//*[@class="bh-btn bh-btn-primary"]'))
                driver.find_element(
                    By.XPATH, '//*[@class="bh-btn bh-btn-primary"]').click()
                WebDriverWait(driver, 15, 0.2).until(
                    lambda x: x.find_element(By.NAME, 'DZ_JSDTCJTW'))
                driver.find_element(By.NAME, 'DZ_JSDTCJTW').send_keys(
                    self._random_temp())
                driver.find_element(By.ID, 'save').click()
                WebDriverWait(driver, 15, 0.2).until(lambda x: x.find_element(
                    By.XPATH,
                    '//*[@class="bh-dialog-btn bh-bg-primary bh-color-primary-5"]'
                ))
                driver.find_element(
                    By.XPATH,
                    '//*[@class="bh-dialog-btn bh-bg-primary bh-color-primary-5"]'
                ).click()
                status = "successful"
            except Exception as e:
                status = "failed"
                print(str(e))

            if self.cfg.notification[i] == "yes":
                if self.cfg.notify_failure_only[i] == "no":
                    # MODIFY: add index:
                    self.send_email(status, i)
                elif status == "failed":
                    # MODIFY: add index:
                    self.send_email(status, i)

            driver.close()
            print(time.strftime("%Y-%m-%d %H:%M:%S -", time.localtime()),
                  status)

    # MODIFY: add index of the loop in run() as argument:
    def send_email(self, message: str, index):
        """Sand email to predefined mailbox.

        Args:
            msg: str.
        """
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = self._format_addr(
            "Physical condition reporter {}".format(self.cfg.from_addr))
        # MODIFY: index:
        msg['To'] = self._format_addr("Admin {}".format(
            self.cfg.to_addr[index]))
        msg['Subject'] = Header("SEU daily report", "utf-8").encode()

        # MODIFY: port of smtp server:
        server = smtplib.SMTP_SSL(self.cfg.smtp_server, self.cfg.port)
        server.login(self.cfg.from_addr, self.cfg.email_password)
        # MODIFY: index:
        server.sendmail(self.cfg.from_addr, [self.cfg.to_addr[index]],
                        msg.as_string())
        server.quit()

    def _format_addr(self, s: str) -> str:
        """Formatting address.

        Args:
            s: str, like "Physical condition reporter <xxx@seu.edu.cn>"

        Returns:
            str, like "'=?utf-8?q?Physical condition reporter?= <xxx@seu.edu.cn>'"
        """
        name, addr = parseaddr(s)

        return formataddr((Header(name, 'utf-8').encode(), addr))


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S -", time.localtime()), "start")
    rh = ReportingHelper()
    rh.run()
