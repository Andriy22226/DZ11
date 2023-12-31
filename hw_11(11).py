from collections import UserDict
import re 
from datetime import datetime


class Field:
    def __init__(self):
        self._value = None


class Name(Field):
    def __init__(self, value):
        self.value=value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value



class Phone(Field):
    def __init__(self, value):
        self.value=value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if re.search(r'^\+?3?8?(0[\s\.-]?\d{2}[\s\.-]?\d{3}[\s\.-]?\d{2}[\s\.-]?\d{2})$',value):
            self._value = value
        else:
            raise Exception ("Phone number must consist only from numbers and have format: +380 XX XXX XX XX, +380-XX-XXX-XX-XX, +380.XX.XXX.XX.XX or without '+38'")

class Birthday(Field):
    def __init__(self, value):
        self.value=value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if re.search(r'\d{2}\.\d{2}\.\d{4}',value):
            self._value = value
        else:
            raise Exception ("Birthday must have format 'DD.MM.YYYY' and consist only from numbers")



class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday=birthday
        

    def add_phones(self, phone):
        if phone not in self.phones:
            self.phones.append(phone)

    def change_phones(self, phone, phone_new):
        for count, ele in enumerate(self.phones):
            if ele == phone:
                self.phones[count] = phone_new
                break

    def remove_phones(self, phone):
        for count, ele in enumerate(self.phones):
            if ele == phone:
                self.phones.remove(ele)
                break

    def list_phones(self):
        return self.phones

    def days_to_birthday(self,birthday):
        self.birthday=datetime.strptime(birthday.value, '%d.%m.%Y')
        now = datetime.now()
        delta1 = datetime(now.year, self.birthday.month, self.birthday.day)
        delta2 = datetime(now.year+1, self.birthday.month, self.birthday.day)
        return ((delta1 if delta1 > now else delta2) - now).days

    


class AddressBook(UserDict):


    def add_record(self, record):
        self.data[record.name.value] = record
        return self.data
        
    def iterator(self, n=2):
        index = 0
        lst_temp = []
        for k, v in self.data.items():
            lst_temp.append(v)
            index = index + 1
            if index >= n: 
                yield lst_temp
                lst_temp.clear()
                index = 0
        if lst_temp:
            yield lst_temp    
    
    def get_page(self, n=2):
        step = self.iterator(n)
        for i in range(len(self.data)):
            try:
                result = next(step)
                print(result)
                input('Press enter for next page: ')
            except StopIteration:
                break



name1=Name('Ivan')
print(name1.value)
name2=Name('Roman')
name3=Name('Nazar')
phone1 = Phone('+380645637685')
print(phone1.value)
phone2 = Phone('0636745676')
phone3 = Phone('0638456778')
birthday1=Birthday('18.06.1968')
print(birthday1.value)
birthday2=Birthday('08.05.1978')
birthday3=Birthday('08.12.1986')
record1=Record(name1, phone1,birthday1)
print(record1.days_to_birthday(birthday1))
print(record1.birthday)
record2=Record(name2, phone2)
record3=Record(name3, phone2,birthday2)
book1=AddressBook()
print(book1)
book1.add_record(record1)
book1.add_record(record2)
book1.add_record(record3)
print(book1)
print(book1.get_page(2))
