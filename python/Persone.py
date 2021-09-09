from posixpath import abspath
from linkedin_scraper.objects import Interest, Accomplishment, Contact
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from linkedin_scraper import Person, Experience, Education
from linkedin_scraper import selectors


class Persone(Person):
    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(
            self,
            linkedin_url=None,
            name=None,
            about=None,
            experiences=None,
            educations=None,
            interests=None,
            accomplishments=None,
            company=None,
            job_title=None,
            contacts=None,
            driver=None,
            get=True,
            scrape=True,
            close_on_complete=True,
    ):
        super().__init__(linkedin_url, name, about, experiences, educations, interests, accomplishments,
                         company, job_title, contacts, driver, get, scrape, close_on_complete)

    def scrape_logged_in(self, close_on_complete=True):
        print("Goes for the new")
        driver = self.driver
        duration = None

        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    self.__TOP_CARD,
                )
            )
        )

        self.name = root.find_element_by_class_name(selectors.NAME).text.strip()

        # get about
        try:
            print(1)
            # see_more = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            #     EC.presence_of_element_located(
            #         (
            #             By.XPATH,
            #             "//*[@class='lt-line-clamp__more']",
            #         )
            #     )
            # )
            # print(2)
            # driver.execute_script("arguments[0].click();", see_more)
            print(3)
            about = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-about-section artdeco-card p5 mt4 ember-view']"
                    )
                )
            )
            about.click()

            child = about.find_element_by_xpath('./div')
            aboutText = child.text.strip()
            if "…" in aboutText:
                aboutText = aboutText.split("…")[0]
            print(aboutText)
            about = aboutText
            print(4)
        except Exception as ex:
            print(f"Por el error {str(ex)}")
            about = None
        if about:
            self.add_about(about)

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )

        # get experience
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/5));"
        )

        ## Click SEE MORE
        self._click_see_more_by_class_name("pv-experience-section__see-more")

        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "experience-section"))
            )
            exp = driver.find_element_by_id("experience-section")
        except:
            exp = None

        if exp is not None:
            for position in exp.find_elements_by_class_name("pv-position-entity"):
                position_title = position.find_element_by_tag_name("h3").text.strip()

                try:
                    company = position.find_elements_by_tag_name("p")[1].text.strip()
                    times = str(
                        position.find_elements_by_tag_name("h4")[0]
                            .find_elements_by_tag_name("span")[1]
                            .text.strip()
                    )
                    from_date = " ".join(times.split(" ")[:2])
                    to_date = " ".join(times.split(" ")[3:])
                    duration = (
                        position.find_elements_by_tag_name("h4")[1]
                            .find_elements_by_tag_name("span")[1]
                            .text.strip()
                    )
                    location = (
                        position.find_elements_by_tag_name("h4")[2]
                            .find_elements_by_tag_name("span")[1]
                            .text.strip()
                    )
                except:
                    company = None
                    from_date, to_date, duration, location = (None, None, None, None)

                experience = Experience(
                    position_title=position_title,
                    from_date=from_date,
                    to_date=to_date,
                    duration=duration,
                    location=location,
                )
                experience.institution_name = company
                self.add_experience(experience)

        # get location
        location = driver.find_element_by_class_name(f"{self.__TOP_CARD}--list-bullet")
        location = location.find_element_by_tag_name("li").text
        self.add_location(location)

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));"
        )

        # get education
        ## Click SEE MORE
        self._click_see_more_by_class_name("pv-education-section__see-more")
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "education-section"))
            )
            edu = driver.find_element_by_id("education-section")
        except:
            edu = None
        if edu:
            for school in edu.find_elements_by_class_name(
                    "pv-profile-section__list-item"
            ):
                university = school.find_element_by_class_name(
                    "pv-entity__school-name"
                ).text.strip()

                try:
                    degree = (
                        school.find_element_by_class_name("pv-entity__degree-name")
                            .find_elements_by_tag_name("span")[1]
                            .text.strip()
                    )
                    times = (
                        school.find_element_by_class_name("pv-entity__dates")
                            .find_elements_by_tag_name("span")[1]
                            .text.strip()
                    )
                    from_date, to_date = (times.split(" ")[0], times.split(" ")[2])
                except:
                    degree = None
                    from_date, to_date = (None, None)
                education = Education(
                    from_date=from_date, to_date=to_date, degree=degree
                )
                education.institution_name = university
                self.add_education(education)

        # get interest
        try:

            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            interestContainer = driver.find_element_by_xpath(
                "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']"
            )
            for interestElement in interestContainer.find_elements_by_xpath(
                    "//*[@class='pv-interest-entity pv-profile-section__card-item ember-view']"
            ):
                interest = Interest(
                    interestElement.find_element_by_tag_name("h3").text.strip()
                )
                self.add_interest(interest)
        except:
            pass

        # get accomplishment
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            acc = driver.find_element_by_xpath(
                "//*[@class='pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view']"
            )
            for block in acc.find_elements_by_xpath(
                    "//div[@class='pv-accomplishments-block__content break-words']"
            ):
                category = block.find_element_by_tag_name("h3")
                for title in block.find_element_by_tag_name(
                        "ul"
                ).find_elements_by_tag_name("li"):
                    accomplishment = Accomplishment(category.text, title.text)
                    self.add_accomplishment(accomplishment)
        except:
            pass

        # get connections
        try:
            driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mn-connections"))
            )
            connections = driver.find_element_by_class_name("mn-connections")
            if connections is not None:
                for conn in connections.find_elements_by_class_name("mn-connection-card"):
                    anchor = conn.find_element_by_class_name("mn-connection-card__link")
                    url = anchor.get_attribute("href")
                    name = conn.find_element_by_class_name("mn-connection-card__details").find_element_by_class_name(
                        "mn-connection-card__name").text.strip()
                    occupation = conn.find_element_by_class_name(
                        "mn-connection-card__details").find_element_by_class_name(
                        "mn-connection-card__occupation").text.strip()

                    contact = Contact(name=name, occupation=occupation, url=url)
                    self.add_contact(contact)
        except:
            connections = None

        if close_on_complete:
            driver.quit()
