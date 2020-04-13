import json


def query_by_number(numb):
    return [d for d in documents if d['number'] == numb]


def list_all():
    for doc in documents:
        print(f'{doc["type"]} "{doc["number"]}" "{doc["name"]}";')


def shelf_search(num):
    for k, v in directories.items():
        if num in v:
            return k
    return "Nothing found"


def del_doc(num):
    for i, doc in enumerate(documents):
        if doc['number'] == num:
            del documents[i]
            shelf_num = shelf_search(num)  # fixed
            if shelf_num != "Nothing found":
                directories[shelf_num].remove(num)
            return 0
    return 1


def add_doc():
    type = input("Enter Type: ").strip()
    numb = input("Enter Number: ").strip()
    name = input("Enter Name: ").strip()
    while 1:
        shelf = input("Enter Shelf: ").strip()
        if shelf not in directories.keys():
            print("Select ", directories.keys())
        else:
            break
    documents.append({"type": type, "number": numb, "name": name})
    directories[shelf].append(numb)
    return 0


def move_doc(doc_numb, new_shelf_number):
    for sh_id, doc_numbers in directories.items():
        if doc_numb in doc_numbers:
            if sh_id == new_shelf_number:
                return 1  # the same shelf, action not needed
            else:
                add_shelf(new_shelf_number)  # fixed
                del doc_numbers[doc_numbers.index(doc_numb)]
                directories[new_shelf_number].append(doc_numb)
                return 0  # success
    return 2  # doc not found on the shelves


def add_shelf(sh_numb):
    if sh_numb not in directories.keys():
        directories.update({sh_numb: []})


def show_owners():
    owners = set()
    for doc in documents:
        try:
            owners.add(doc['name'])
        except KeyError:
            print(f"Error. Document \"{doc}\" doesn\'t have \"name\" attribute")

    print("Owners:")
    for owner in owners:
        print(owner)


if __name__ == "__main__":

    info_message = '''p – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит;
    l– list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин";
    s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится;
    a – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться.
    d – delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок;
    m – move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую;
    as – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень;
    o - owners - команда, выводящая имена всех владельцев документов;
    q - for exit
    '''

    cmd_list = ["p", "l", "s", "a", "q", "d", 'm', 'as', 'o']

    with open("fixtures/documents.json", encoding="utf-8") as f:
       documents = json.load(f)

    with open("fixtures/directories.json", encoding="utf-8") as f:
        directories = json.load(f)

    print(info_message)
    while 1:
        cmd = input("SELECT ACTION:\n").lower()
        if cmd in cmd_list:
            if cmd == 'q':
                exit(0)
            elif cmd == 'p':
                result = query_by_number(input("Enter document number:").strip())
                if result:
                    print(f'Name: {result.pop()["name"]}')
                else:
                    print("Nothing found")
            elif cmd == 'l':
                list_all()
            elif cmd == 's':
                print('Shelf number: ', shelf_search(input("Enter document number:").strip()))
            elif cmd == 'a':
                add_doc()
            elif cmd == 'd':
                result = del_doc(input("Enter document number:"))
                p = lambda r: "Deleted" if not r else "Nothing found"
                print(p(result))
            elif cmd == 'm':
                result = move_doc(input("Enter document number: "), input("Enter Shelf number: "))
                if result == 0:
                    print('Moved')
                elif result == 1:
                    print('The same shelf, action not needed')
                else:
                    print('Doc not found on the shelves')
            elif cmd == 'as':
                add_shelf(input("Enter new shelf number: ").strip())
            elif cmd == 'o':
                show_owners()


