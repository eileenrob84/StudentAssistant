from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import getpass  # this does not work in PyCharm
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

'''
Install PhantomJS before running this.
Run this ONLY in a terminal, NOT in IDE.
Currently this program only print scrapped info.
'''


class ScrapStevensCourses:

    def __init__(self):
        self.driver = webdriver.PhantomJS("C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
        self.driver.implicitly_wait(10)  # second
        self.driver.get("https://mystevens.stevens.edu/sso/web4student.php")
        self.raw_courses = open('all_courses_raw.txt', 'w+')
        self.errors = open('errors.txt', 'w+')
        # self.course_page_cache = ''
        # self.major_page_cache = ''

    def get_login_info(self):
        user = input("Enter the User Name:")
        password = input("Enter the Password:") # uncomment this line if you are using IDE
        # password = getpass.getpass()  # uncomment this line if you are using terminal
        print("got password")
        return user, password

    def go_to_courses_description_page(self, course_id):
        select1 = Select(self.driver.find_element_by_xpath('//select[option/@value="%s"]' % course_id))
        select1.select_by_value(course_id)

        self.driver.find_element_by_name("submitbutton").submit()
        # time.sleep(2)

    def go_to_courses_page(self, major_id):
        select = Select(self.driver.find_element_by_xpath('//select[option/@value="%s"]' % major_id))
        select.select_by_value(major_id)
        self.driver.find_element_by_name("submitbutton").submit()
        # time.sleep(2)

    def go_to_majors_page(self):
        hover1_element = self.driver.find_element_by_id("menuHeading5")
        hover2_element = self.driver.find_element_by_xpath("//div[a/@title='Course Sections']")
        ActionChains(self.driver).move_to_element(hover1_element).move_to_element(hover2_element).click(
            hover2_element).perform()
        time.sleep(2)

    def login(self):
        info = self.get_login_info()
        self.driver.find_element_by_name("j_username").send_keys(info[0])
        self.driver.find_element_by_name("j_password").send_keys(info[1])
        self.driver.find_element_by_name('submit').submit()

    def get_raw_majors(self):
        f = open('majors_raw.txt', 'w+')
        f.write(self.driver.page_source)
        f.close()

    def parse_raw_majors(self):
        self.get_raw_majors()
        target = "<option value="
        file = open('majors_raw.txt')
        # majors = {}
        majors = []
        for line in file:
            if target in line:
                words = line.strip().split("\"")
                majors.append(words[1])
                # majors[words[1]] = words[2][1:]
                # print(words[1], words[2][1:])
        return majors

    def get_raw_courses(self, major):
        f = open('%s_raw.txt' % major, 'w+')
        f.write(self.driver.page_source)
        f.close()

    def parse_raw_courses(self, major):
        self.get_raw_courses(major)
        target = "<option value="
        file = open('%s_raw.txt' % major)
        # courses = {}
        courses = []
        for line in file:
            if target in line:
                words = line.strip().split("\"")
                courses.append(words[1])
                # courses[words[1]] = words[2][1:]
        return courses

    def save_tables(self):

        dfs = pd.read_html(self.driver.page_source)
        # print(type(dfs))  # <class 'list'>
        # print(len(dfs[4]))  # normally this is the table we need
        try:
            line = dfs[4].to_csv(sep=' ', index=False, header=False)
            line = line.replace(u'\xa0', u' ')
            self.raw_courses.write(line)
        except IndexError:
            for line in dfs:
                line = line.replace(u'\xa0', u' ')
                self.errors.write(line.to_csv(sep=' ', index=False, header=False))

    def parse_tables(self):

        self.login()

        self.go_to_majors_page()
        majors = self.parse_raw_majors()

        for major in majors:
            self.go_to_courses_page(major)
            # self.major_page_cache = self.driver.page_source
            courses = self.parse_raw_courses(major)

            for course in courses:
                self.go_to_courses_description_page(course)
                # self.course_page_cache = self.driver.page_source
                self.save_tables()
                self.driver.back()  # due to the stability of connections, this may not success
                # while self.back_not_success():
                #     self.driver.back()
                #     time.sleep(2)

            self.driver.back()
            # while self.back_not_success():
            #     self.driver.back()
            #     time.sleep(2)

        self.driver.quit()
        self.raw_courses.close()
        self.errors.close()

    # def back_not_success(self):
    #     if self.driver.page_source == self.course_page_cache:
    #         return True
    #     return False

# class SaveIntoDatabase:
    # TODO : save information in database


def main():
    demo = ScrapStevensCourses()
    demo.parse_tables()


if __name__ == '__main__':
    main()