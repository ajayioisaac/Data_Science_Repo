
# Online Python - IDE, Editor, Compiler, Interpreter
#Task: Build a Simple Contact Book using Dictionaries
#Problem Statement: You're going to write a Python program that allows users to store and retrieve contacts using a dictionary.
class ContactManager:
    
    def __init__(self):
        self.contacts = {}
        
    def add_contact(self):
        name = input("Enter contact name: ")
        phone = input("Enter phone number: ")
        self.contacts[name] = phone
        print(f"Contact for {name} added successfully")

    def search_contact(self):
        name = input("Enter contact name: ")
        if name in self.contacts:
            print(f"{name}'s phone number is {self.contacts[name]}\n")
        else:
            print(f"Contact for {name} not found.\n")
    
    def view_all(self):
        if self.contacts:
            print('\nAll Contacts:')
            for name, phone in self.contacts.items():
                print(f"{name}:{phone}")
            print()
        else:
            print("No contacts found.\n")
    
    def menu(self):
        while True:
            print("Contact Manager")
            print("1. Add Contact")
            print("2. Search Contact")
            print("3. View All Contact")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                self.add_contact()
            elif choice == "2":
                self.search_contact()
            elif choice == "3":
                self.view_all()
            elif choice == "4":
                print("Goodbye")
                break
            else:
                print("Invalid choice. Please try again.\n")
manager = ContactManager()
manager.menu()
