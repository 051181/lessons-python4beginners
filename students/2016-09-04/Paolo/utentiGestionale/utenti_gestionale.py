# -*- coding: utf-8 -*-

import csv  
import json
import xml.etree.cElementTree as ET
import sys
from collections import defaultdict

PEOPLE = []

def print_on_screen(list_input):
    for i,p in enumerate(list_input):
        print("Utente {}".format(i))
        
        print("     Name: {}".format(p["name"]))
        print("     City: {}".format(p["city"]))
        print("     Salary: {}".format(p["salary"]))
        
        
def write_on_csv(list_input, filename = "people.csv"):
    with open(filename, "wb") as csvfile:
        
        
        fieldnames = ['name', 'city', 'salary', 'annual']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames, delimiter = ";")

        writer.writeheader()
        
        for p in list_input:
            writer.writerow(p)

def write_on_json(list_input, filename = "people.json"):

    if filename.endswith(".json"):
    
        with open("people.json", "wb") as jsonfile:
            json.dump(list_input, jsonfile, indent = 2) #Indent = 2 mi permette di avere il json scritto in colonna per bene e non tutto in riga..!
    else:
        print("Impossible to write on json file")
  
def write_on_xml(list_input):
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")
    utenti_child = ET.SubElement(doc, "Utenti")
    
    for i,p in enumerate(list_input):
        ET.SubElement(utenti_child, "utente " + str(i), name="name").text = p["name"]
        ET.SubElement(utenti_child, "utente " + str(i), name="city").text = p["city"]
        ET.SubElement(utenti_child, "utente " + str(i), name="salary").text = str(p["salary"])
        
    tree = ET.ElementTree(root)
    tree.write("people.xml")

def main():
    
    number_of_people = int(raw_input("Per quanti utenti vuoi inserire le anagrafiche?"))
    
    for count in range(number_of_people):
        anagraphic_people_dict = {}
        name, city, salary = raw_input("Inserisci name, city, salary:").split()
        
        anagraphic_people_dict["name"] = name
        anagraphic_people_dict["city"] = city
        anagraphic_people_dict["salary"] = int(salary)
        PEOPLE.append(anagraphic_people_dict)
        
    print_on_screen(PEOPLE)

def save(list_of_dict, input_args):
    write_on_csv(list_of_dict)
    
    if len(input_args) > 1:
        write_on_json(list_of_dict, input_args[1])
    else:
        write_on_json(list_of_dict)
        
    write_on_xml(list_of_dict)
    

class DictList(dict):
    def get(self, k, default = None):
        if k not in self:
            self[k] = []
        return super(DictList, self).get(k, default)
        
def print_people_by_city_feroda(list_input): #Questa opzione per le persone suddivise in città è più comoda di quella sotto ed utilizza una classe fatta da noi
    
    res = DictList()
    
    for elem in list_input:
        res.get(elem["city"]).append(elem["name"])
    
    print("People by City By Feroda:")
    for elem in res:
        print("City: " + elem)
        for e in res[elem]:
            print("  " + e)
    
def print_people_by_city(list_input):   #Invece di fare il doppio ciclo per assegnare la lista vuota ecc, mi basterebbe farne uno dove per primo 
                                        #faccio res[elem["city"]] = res.get(elem["city"], []) 
                                        #Che auto inizializza il dizionario per una chiave con una lista vuota se quella chiave non è già presente.
    print("People by City..")
    
    res = {}
    
    for elem in list_input:
        res[elem["city"]] = []
    
    for elem in list_input:
        res[elem["city"]].append(elem["name"])
        
        
    for elem in res:
        print("City: " + elem)
        for e in res[elem]:
        
            print("  " + e)
        
    
def compute_annual_salary(person):
    person["annual"] = person["salary"] * 13
    
def print_people_with_annual_salary(list_input):
    for p in list_input:
        compute_annual_salary(p)
    
    for elem in list_input:
        print(elem) 

    write_on_csv(list_input, "peopleWithAnnualSalary.csv")
    
def main_and_save(input_args):
    main()
    save(PEOPLE, input_args)
    print_people_by_city(PEOPLE)
    print_people_by_city_feroda(PEOPLE)
    print_people_with_annual_salary(PEOPLE)
    
    
if __name__ == "__main__":
 
    try:
        main_and_save(sys.argv)
    except KeyboardInterrupt:
        print("Non puoi uscire")
        #response = raw_input("Sei sicuro di voler uscire? (s/n)")
        #if response == s:
         #   sys.exit()
    
    