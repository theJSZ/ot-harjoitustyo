class Person:
    def __init__(self, name):
        self._name = name

    def talk(self):
        print(f'{self._name}: "Blabla"')

    def scream(self):
        print(f'{self._name}: "AAIEEE"')


persons = [Person("Jussi"), Person("Alvin")]
functions = [Person.talk, Person.scream]
for person in persons:
    functions[1](person)