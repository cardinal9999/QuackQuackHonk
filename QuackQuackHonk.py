import json
import os
import time
import getpass
import urllib
global JSONDecodeError
global variables
global functions
global imported
global if_statement
global if_code
global inputs
global current_answer
global oper_type
JSONDecodeError = json.decoder.JSONDecodeError
variables = {}
functions = {}
imported = []
return_ = 0
loop_code = [0, []]
module = ["_main_", 0]
python_codes = []
inputs = []
if_statement = True
if_code = []
oper_type = ""
current_answer = ""
if not os.path.isdir(f"C:/Users/{getpass.getuser()}/QQH_Data"):
    print("Welcome to QuackQuackHonk!")
    os.mkdir(f"C:/Users/{getpass.getuser()}/QQH_Data")
    os.mkdir(f"C:/Users/{getpass.getuser()}/QQH_Data/modules")
def parse_integers(string):
    lists = []
    lists1 = []
    a = ""
    for i in string:
        if i == ";":
            lists.append(a)
            a = ""
        else:
            a = a + i
    for i in lists:
        lists1.append(int(i))
    return lists1
def parse(string):
    a = list(variables.keys())
    b = list(variables.values())
    for i in range(len(a)):
        string = string.replace(f"$[{a[i]}]", str(b[i]))
        try:
            for j in range(len(a[i])):
                string = string.replace(f"{{${a[i]}:{j}$}}", a[i][j])
        except:
            pass
        
    for i in range(len(inputs)):
         string = string.replace(f"_in_.{i}", str(inputs[i]))
         string = string.replace(f"_/in_.{i}", f"_in_.{i}")
         string = string.replace(f"_//in_.{i}", f"_/in_.{i}")
    string = string.replace("$input_answer", current_answer)
    string = string.replace("$_return_", str(globals()["return_"]))
    return json.loads(string)
def process_code(code):
    Z = globals()["module"]
    if Z[1] == 1:
        file = open(f"C:/Users/{getpass.getuser()}/QQH_Data/modules/{Z[0]}.qqh", "r")
        contents = file.read()
        file.close()
        file1 = open(f"C:/Users/{getpass.getuser()}/QQH_Data/modules/{Z[0]}.qqh", "w")
        file1.write(contents + "\n" + code)
        file1.close()
    
    if code == "exit":
        exit()
    elif code == "" or code == " " or frozenset(code) == frozenset([" "]):
        return 0
    elif code[0] == "@":
        a = ""
        b = 0
        for i in range(999):
            b += 1
            if code[i+1] == ":":
                break
            a = a + code[i+1]
        c = ""
        for i1 in range((len(code) - b) - 1):
            c = c + code[b+(i1 + 1)]
        variables[a] = parse(c)
    elif code[:6] == "print:":
        d = code[-(len(code) - 6):]
        try:
            print(parse(d))
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
    elif code[:6] == "input:":
        d = code[-(len(code) - 6):]
        try:
            e = parse(d)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
            pass
        f = input(e)
        global current_answer
        current_answer = f
    elif code[:8] == "equals?:":
        e = code[-(len(code) - 8):]
        try:
            f = parse(e)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
        g = f[0] == f[1]
        variables[f[2]] = g
    elif code[0] == "+":
        e = code[-(len(code) - 1):]
        E = parse_integers(e)
        globals()["return_"] = E[0] + E[1]
    elif code[0] == "-":
        e = code[-(len(code) - 1):]
        E = parse_integers(e)
        globals()["return_"] = E[0] - E[1]
    elif code[:4] == "mul_":
        e = code[-(len(code) - 4):]
        E = parse_integers(e)
        globals()["return_"] = E[0] * E[1]
    elif code[:4] == "div_":
        e = code[-(len(code) - 4):]
        E = parse_integers(e)
        globals()["return_"] = E[0] / E[1]
    elif code[:5] == "%mod_":
        e = code[-(len(code) -5 ):]
        E = parse_integers(e)
        globals()["return_"] = E[0] % E[1]
    elif code[0] == "#":
        a = ""
        b = 0
        for i in range(999):
            b += 1
            if code[i+1] == ":":
                break
            a = a + code[i+1]
        c = ""
        for i1 in range((len(code) - b) - 1):
            c = c + code[b+(i1 + 1)]
        try:
            c = parse(c)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
            c = []
        functions[a] = {"inputs": [], "code":[]}
    elif code[:5] == "OPER:":
        g = code[-(len(code) - 5):]
        globals()["oper_type"] = json.loads(g)
    elif code[:2] == "->":
        g = code[-(len(code) - 2):]
        functions[globals()["oper_type"]]["code"].append(g)
    elif code[:4] == "run:":
        g = code[-(len(code) - 4):]
        h = parse(g)
        globals()["inputs"] = []
        try:
            H = h["inputs"]
            I = h["name"]
        except KeyError:
            print("KeyError: Wrong map keys")
            return
        for i in H:
            globals()["inputs"].append(i)
        codes = functions[I]["code"]
        for _ in codes:
            process_code(_)
    elif code[:3] == "//:":
        pass
    elif code[:10] == "list.push:":
        h = code[-(len(code) - 10):]
        try:
            H = parse(h)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
        H1 = H[0]
        H2 = H[1]
        globals()["variables"][H1].append(H2)
    elif code[:10] == "list.pull:":
        h = code[-(len(code) - 10):]
        try:
            H = parse(h)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
        H1 = H[0]
        H2 = H[1]
        try:
            globals()["variables"][H1].remove(H2)
        except ValueError:
            print("FindingError: Cannot find item in list")
    elif code[:10] == "file.read:":
        H = code[-(len(code) - 10):]
        try:
            i = parse(H)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
            return
        H1 = H[0]
        H2 = H[1]
        try:
            H3 = open(str(H1), "r")
        except FileNotFoundError:
            print("FindingError: Cannot find file")
            return
        globals()["variables"][H2] = H3.read()
    elif code[:11] == "map.define:":
        I = code[-(len(code) - 11):]
        try:
            I = parse(I)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
            return
        globals()["variables"][I[0]][I[1]]=I[2]
    elif code[:7] == "repeat:":
        I = code[-(len(code) - 7):]
        loop_code[0] = int(I)
        loop_code[1] = []
    elif code[:2] == "=>":
        a = ""
        for i in range(len(code) -2):
            a = a + code[i+2]
        try:
            globals()["loop_code"][1].append(a)
        except:
            print("FindingError: Repeat command after => command")
            return
    elif code == "loop.clear":
        globals()["loop_code"] = [0, []]
    elif code == "loop.run":
        I = globals()["loop_code"]
        I1 = I[0]
        I2 = I[1]
        for _ in range(I1):
            for i in I2:
                process_code(i)
    elif code[:12] == "bitwise.xor:":
        i = code[-(len(code) - 12):]
        try:
            I = parse(i)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
            return
        I2 = I[0] ^ I[1]
        globals()["variables"][I[2]] = I2
    elif code[:11] == "map.remove:":
        i = code[-(len(code) - 11):]
        try:
            i = parse(i)
        except JSONDecodeError:
            print("SyntaxError: Cannot parse token")
            return
        i = dict(i)
        try:
            del globals()["variables"][i["map"]][i["key"]]
        except KeyError:
            print("FindingError: Missing keys 'map' and 'key' for input")
    elif code[0] == "!":
        j = code[-(len(code) - 1):]
        globals()["module"] = [j, 1]
        file = open(f"C:/Users/{getpass.getuser()}/QQH_Data/modules/{j}.qqh", "w")
        file.close()
    elif code == "/x":
        j = globals()["module"][0]
        globals()["module"] = [j, 0]
    elif code[:7] == "return:":
        J = code[-(len(code) - 7):]
        globals()["return_"] = parse(J)
    elif code[0] == "{" and code[-1] == "}":
        a = ""
        b = 0
        for i in range(999):
            b += 1
            if code[i+1] == "}":
                break
            a = a + code[i+1]
        try:
            file = open(f"C:/Users/{getpass.getuser()}/QQH_Data/modules/{a}.qqh", "r")
            J = file.read()
            for j1 in J.splitlines():
                process_code(j1)
        except FileNotFoundError:
            print(f"ModuleNotFoundError: No module named {a}")
    elif code == "py.clear":
        globals()["python_codes"] = []
    elif code == "py.run":
        k = ""
        for K in globals()["python_codes"]:
            k = k + "\n" + K
        exec(k)
    elif code[:3] == "==>":
        l = code[-(len(code) - 3):]
        globals()["python_codes"].append(l)
    elif code[0] == "[" and code[-1] == "]":
        a = ""
        b = 0
        for i in range(999):
            b += 1
            if code[i+1] == "]":
                break
            a = a + code[i+1]
        try:
            file = open(a, "r")
            J = file.read()
            for j1 in J.splitlines():
                process_code(j1)

        except FileNotFoundError:
            print(f"FindingError: No script named {a}")
            
    elif code[:11] == "time.sleep:":
        L = code[-(len(code) - 11):]
        L = parse(L)
        time.sleep(L)
    elif code == "if.run":
        for m in globals()["if_code"]:
            if globals()["if_statement"]:
                process_code(m)
    elif code == "if.clear":
        globals()["if_code"] = []
        globals()["if_statement"] = True
    elif code[:7] == "if.set:":
        M = code[-(len(code) - 7):]
        M = parse(M)
        globals()["if_statement"] = M
    elif code[:3] == "-->":
        n = code[-(len(code) - 3):]
        globals()["if_code"].append(n)
    else:
        print(f"CommandError: Invalid command {code}")
    
while 1:
    a = input("> ")
    process_code(a)
