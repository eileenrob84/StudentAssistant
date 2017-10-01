import re


class Parse:
    def __init__(self):
        self.f = self.open_file()
        self.count_title_call_number = 0
        self.count_title_call_number_control = 0
        self.count_status = 0
        self.preprocessed = self.open_stage1()

    def open_file(self):
        return open(r'test.txt')  # row courses file

    def open_stage1(self):
        return open(r'stage1.txt', 'w+')

    def parse_line1(self, txt):
        """
        SectionTitle, CallNumber
        :param txt: self.preprocessed
        :return: tuple
        """
        course_name = call_number = "NA"
        re1 = '(")'  # Any Single Character 1
        re2 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1
        re3 = '(\\s+)'  # White Space 1
        re4 = '(-)'  # Any Single Character 2
        re5 = '(\\d+)'  # Integer Number 1
        re6 = '(-)'  # Any Single Character 3
        re7 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 2
        re8 = '.*?'  # Non-greedy match on filler
        re9 = '((?:[a-z][a-z0-9_]*))'
        re10 = '(")'  # Any Single Character 4

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10, re.IGNORECASE | re.DOTALL)
        m = rg.search(txt)
        if m:
            words = txt.split("\" \"")
            course_name = words[0][1:].split(" - ")[0]  # this is the course name. like this: TM -616-W0
            print(course_name)
            call_number = words[1][0:5]
            print(call_number)  # this is the call number, like this: 10086
            self.count_title_call_number += 1
        return course_name, call_number

    def parse_line2(self, txt):
        """
        status_seats_available, days_time_location, instructor, session_and_dates, credits
        :param txt:
        :return: tuple
        """
        words = txt.split('cart" ')
        partition = words[1]  # contains StatusSeatsAvailable, DaysTimeLocation, Instructor, SessionAndDates, Credits
        status_seats_available = days_time_location = instructor = session_and_dates = credit = "NA"
        if partition.startswith('"Open'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 7 9 11
            if length == 7:
                status_seats_available = t[1]
                days_time_location = t[3]
                instructor = t[4][1:]
                session_and_dates = t[5]
                credit = t[6].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            elif length == 9:
                status_seats_available = t[1]
                days_time_location = t[3]
                if " STAFF " in t:
                    instructor = t[4][1:-1]
                else:
                    instructor = t[5]
                session_and_dates = t[7]
                credit = t[8].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            elif length == 11:
                status_seats_available = t[1]
                days_time_location = t[3]
                instructor = t[5]
                session_and_dates = t[7]
                credit = t[9]
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            else:
                print("AAAAAAAAAAAAAWWWWWWWWWWWWWWGGGGGGGGGGGGGGGGG")
            self.count_status += 1
        elif partition.startswith('Cancelled'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 3 5 7
            if length == 3:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                credit = t[2][-5:].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(credit)
                # NO instructor
                # NO session_and_dates
            elif length == 5:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                session_and_dates = t[3]
                credit = t[4][-5:].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(session_and_dates)
                print(credit)
                # NO instructor
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1][len('CANCELLED '):]
                session_and_dates = t[3]
                credit = t[5].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(session_and_dates)
                print(credit)
                # NO instructor
            else:
                print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
            self.count_status += 1
        elif partition.startswith('Closed'):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 5 7 9
            if length == 5:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[2][1:]
                session_and_dates = t[3]
                credit = t[4].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[6].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            elif length == 9:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[7]
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            else:
                print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
            self.count_status += 1
        elif partition.startswith('Open '):
            t = partition.split('"')
            length = len(t)  # only 3 cases: 5 7 9
            if length == 5:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[2][1:-1]
                session_and_dates = t[3]
                credit = t[4].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            elif length == 7:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[6].strip()
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            elif length == 9:
                status_seats_available = t[0]
                days_time_location = t[1]
                instructor = t[3]
                session_and_dates = t[5]
                credit = t[7]
                print(t)  # TODO: remove prints
                print(status_seats_available)
                print(days_time_location)
                print(instructor)
                print(session_and_dates)
                print(credit)
            else:
                print("AAAAAAAAAWWWWWWWWWWWWWWWWWGGGGGGGGGGGGGG")
            # TODO: fill available variables
            self.count_status += 1
        else:
            print("\n\n\nthis line is not matched", partition)
        return status_seats_available, days_time_location, instructor, session_and_dates, credit

    def get_days_time_location(self):
        pass

    def get_instructor(self):
        pass

    def get_session_and_dates(self):
        pass

    def get_credits(self):
        pass

    def populate_stage1(self, txt):
        re1 = '(")'  # Any Single Character 1
        re2 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 1
        re3 = '(\\s+)'  # White Space 1
        re4 = '(-)'  # Any Single Character 2
        re5 = '(\\d+)'  # Integer Number 1
        re6 = '(-)'  # Any Single Character 3
        re7 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 2
        re8 = '.*?'  # Non-greedy match on filler
        re9 = '(\\s+)'  # White Space 2
        re10 = '((?:[a-z][a-z0-9_]*))'  # Variable Name 3

        rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10, re.IGNORECASE | re.DOTALL)
        m = rg.search(txt)
        if m:
            self.preprocessed.write(txt)
            self.count_title_call_number_control += 1

    def file_works(self):
        for line in self.f:
            self.populate_stage1(line)

        self.preprocessed.close()
        self.preprocessed = open(r'stage1.txt')

        for line in self.preprocessed:
            self.parse_line1(line)
            self.parse_line2(line)

        # print(self.count_title_call_number)
        print()
        print(self.count_title_call_number_control)
        print(self.count_status)

    def get_course_dependency(self):
        pass
        # TODO: parse dependencies from PDF file using regex, dependencies have 2 or more types, 1 pre, 2 coreq
        '''
        A prerequisite is a requirement that must be met before you take a course, 
        while a corequisite is a course that must be taken at the same time.
        '''


def main():
    demo = Parse()
    demo.file_works()
    demo.f.close()
    demo.preprocessed.close()


if __name__ == '__main__':
    main()
