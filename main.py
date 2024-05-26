import json



class Node:

    next_id = 1

    def __init__(self, data, parent=None, color="red", question=None):
        self.id = Node.next_id
        Node.next_id += 1
        self.data = data
        self.parent = parent
        self.question = []
        self.children = []
        self.concept = []
        self.color = color

    def add_child(self, data, color="red"):
        new_node = Node(data, self, color)
        self.children.append(new_node)
        return new_node

    def change_color(self, color):
        self.color = color

    def rename(self, new_data):
        self.data = new_data

    def move_to(self, new_parent):
        if self.parent:
            self.parent.children.remove(self)
        new_parent.children.append(self)
        self.parent = new_parent
    
    def return_question(self):
        return self.question

    def __repr__(self):
        display_data = self.data if len(self.data) <= 50 else self.data[:50] + "..."
        return f"{self.id}: {display_data} ({self.color})"
    
    def full_repr(self):
        return f"{self.id}: {self.data} "














def save_tree(root):
    tree_data = {
        "next_id": Node.next_id,
        "nodes": []
    }

    def encode_node(node):
        node_data = {
            "id": node.id,
            "data": node.data,
            "color": node.color,
            "parent": None if node.parent is None else node.parent.id,
            "children": [child.id for child in node.children],
            "questions": node.question,
            "concept": node.concept
        }
        return node_data

    def encode_tree(node):
        tree_data["nodes"].append(encode_node(node))
        for child in node.children:
            encode_tree(child)

    encode_tree(root)

    with open("DSA.json", "w") as file:
        json.dump(tree_data, file, indent=2)



def load_tree():
    try:
        with open("DSA.json", "r") as file:
            tree_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return Node("Root Node")

    nodes = {}

    def decode_node(node_data):
        node = Node(node_data["data"], None, node_data["color"])
        node.id = node_data["id"]
        nodes[node.id] = node
        node.question = node_data.get("questions", [])  # Load questions or initialize to empty list
        node.concept = node_data.get("concept", [])  # Load concepts or initialize to empty list
        return node

    root = None
    for node_data in tree_data["nodes"]:
        node = decode_node(node_data)
        if node_data["parent"] is None:
            root = node
        else:
            parent = nodes[node_data["parent"]]
            node.parent = parent
            parent.children.append(node)
            

    Node.next_id = tree_data["next_id"]
    return root


def print_tree(node, indent=0):
    print("\n" + " " * indent + node.full_repr())
    for child in node.children:
        print_tree(child, indent + 2)

def get_node(root, node_id):
    if root.id == node_id:
        return root
    for child in root.children:
        node = get_node(child, node_id)
        if node:
            return node
    return None

def add_node(node):
    data = input(f"Enter data for new node (parent: {node}): ")
    new_node = node.add_child(data, "red")
    print(f"New node added: {new_node}")
    save_tree(root)


def add_question(node, question):
   node.question.append(question)

def add_concept(node, question):
   node.concept.append(question)

def show_questions(node):
    for each in node.question:
        print(each, end=' ')
    print()  # Add a newline character after all questions

def show_questions2(node, indent):
    if node.question == []:
        return "None"
    else:
        questions_str = "\n"
        for index, question in enumerate(node.question, 1):  # Unpack the tuple
            questions_str += f"{' ' * (indent)}{question}\n"  # Format with f-string
        return questions_str.rstrip("\n")  # Remove trailing newline
    
def get_questions_for_node(node):
    return node.return_question()


def show_subtree(node):
    """Prints the subtree rooted at the given node with full text."""
    def print_subtree(node, indent=0):
        print(" " * indent + node.full_repr())
        for child in node.children:
            print_subtree(child, indent + 2)
    
    print_subtree(node)

def show_questions_in_tree(node, indent=0):
    print("\n" + " " * indent + node.full_repr())

    questions = show_questions2(node, indent)
    if questions != "None":  # Check if there are questions
        print(" " * (indent + 2) + questions)

    for child in node.children:
        show_questions_in_tree(child, indent + 2)


def show_questions_in_tree2(node, indent=0):
    questions = show_questions2(node, indent)
    
    if questions != "None":  # If node has questions
        print(" " * (indent + 2) + questions)  # Display questions first

    if node.parent is not None:  # Display node information (except for root node)
        print(" " * indent + node.full_repr())

    for child in node.children:
        show_questions_in_tree2(child, indent + 2)  



















def main():
    global root
    root = load_tree()
    print("Initial tree:")
    print_tree(root)

    while True:
        print("\nOptions:")
        print("1. Add a new node")
        print("2. Change color of a node")
        print("3. Rename a node")
        print("4. Move a node")
        print("5. Show subtree")
        print("6. Add question")
        print("7. Show question")
        print("8. Show questions in the form of tree")
        print("9. Show questions first, in the form of a tree")
        print("10. Exit")
        choice = input("Enter your choice (9): ")

        if choice == "1":
            print("\nAdd a new node")
            parent_id = input("Enter parent node ID (or leave blank for root): ")
            if parent_id:
                try:
                    parent_node = get_node(root, int(parent_id))
                    if parent_node:
                        add_node(parent_node)
                    else:
                        print(f"Node with ID {parent_id} not found.")
                except ValueError:
                    print("Invalid parent node ID. Please enter a valid integer.")
            else:
                add_node(root)
            print("\nUpdated tree:")
            print_tree(root)

        elif choice == "2":
            print("\nChange color of a node")
            node_id = input("Enter node ID: ")
            try:
                node_id = int(node_id)
                node = get_node(root, node_id)
                if node:
                    new_color = input(f"Enter new color for node '{node}': ")
                    node.change_color(new_color)
                    save_tree(root)
                    print("\nUpdated tree:")
                    print_tree(root)
                else:
                    print(f"Node with ID {node_id} not found.")
            except ValueError:
                print("Invalid node ID. Please enter a valid integer.")

        elif choice == "3":
            print("\nRename a node")
            node_id = input("Enter node ID: ")
            try:
                node_id = int(node_id)
                node = get_node(root, node_id)
                if node:
                    new_data = input(f"Enter new data for node '{node}': ")
                    node.rename(new_data)
                    save_tree(root)
                    print("\nUpdated tree:")
                    print_tree(root)
                else:
                    print(f"Node with ID {node_id} not found.")
            except ValueError:
                print("Invalid node ID. Please enter a valid integer.")

        elif choice == "4":
            print("\nMove a node")
            node_id = input("Enter node ID to move: ")
            try:
                node_id = int(node_id)
                node = get_node(root, node_id)
                if node:
                    new_parent_id = input("Enter new parent node ID: ")
                    try:
                        new_parent_id = int(new_parent_id)
                        new_parent = get_node(root, new_parent_id)
                        if new_parent:
                            node.move_to(new_parent)
                            save_tree(root)
                            print("\nUpdated tree:")
                            print_tree(root)
                        else:
                            print(f"Node with ID {new_parent_id} not found.")
                    except ValueError:
                        print("Invalid new parent node ID. Please enter a valid integer.")
                else:
                    print(f"Node with ID {node_id} not found.")
            except ValueError:
                print("Invalid node ID to move. Please enter a valid integer.")

        elif choice == "5":
            print("\nShow subtree")
            node_id = input("Enter node ID to show subtree: ")
            try:
                node_id = int(node_id)
                node = get_node(root, node_id)
                if node:
                    show_subtree(node)
                else:
                    print(f"Node with ID {node_id} not found.")
            except ValueError:
                print("Invalid node ID. Please enter a valid integer.")

        elif choice == "6":
            print("\nAdd question:")
            node_id = int(input("Enter node ID to add question: "))
            node = get_node(root, node_id)
            if node:
                while True:
                    question = input("Enter question (or 'q' to finish): ")
                    if question.lower() == 'q':
                        break
                    add_question(node, question)
                    save_tree(root)
            else:
                print(f"Node with ID {node_id} not found.")
        
        elif choice == "7":
            print("\nView questions: ")
            node_id = input("Enter node ID to view questions: ")
            try:
                node_id = int(node_id)
                node = get_node(root, node_id)
                if node:
                    show_questions_in_tree(node)
                else:
                    print(f"Node with ID {node_id} not found")
            except ValueError:
                print("Invalid node ID. Please enter a valid integer.")

        elif choice == "8":
            print("Show Subtree in the form of questions: ")
            node_id = int(input("Enter node ID to view questions: "))  # Convert input to int directly
            node = get_node(root, node_id)
            if node:
                show_questions_in_tree(node)  # Pass root to show_questions_in_tree
            else:
                print(f"Node with ID {node_id} not found")
        
        elif choice == "9":
            print("Show question first, in the form of a tree: ")
            node_id = int(input("Enter node ID to view questions: "))  # Convert input to int directly
            node = get_node(root, node_id)
            if node:
                show_questions_in_tree2(node)  # Pass root to show_questions_in_tree
            else:
                print(f"Node with ID {node_id} not found")
  
        elif choice == "10":
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
