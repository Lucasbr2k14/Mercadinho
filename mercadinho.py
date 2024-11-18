import os
from pathlib import Path
from random import randint
from table import table


# Bicho market

# Classe banco de dados

class DataBase:
  def __init__(self, file:str) -> None:
    if Path(file).is_file():
      self.file:str = file
    else:
      print("Arquivo Não existe")
      exit(-1)


  def create(self, prod:str, price:float, quanti:int, id:int):
    data_base = open(self.file, 'a', encoding='utf-8')
    data_base.write(f"{prod}|{price}|{quanti}|{id}\n")
    data_base.close() 
  

  def getAll(self):
    data_base = open(self.file, 'r', encoding='utf-8')
    data = data_base.read().split('\n')
    data.pop(-1)
    for i in range(len(data)):
      data[i] = data[i].split("|")
      data[i][1] = float(data[i][1])
      data[i][2] = int(data[i][2])
      data[i][3] = int(data[i][3])
    return data
  

  def getProd(self, collum:int, product:str):
    get_all = self.getAll()
    for i in range(len(get_all)):
      if get_all[i][collum] == product:
        return get_all[i]
    return -1
  

  def edit(self, collum:int, value, collumNewValue:int, newValue):
    get_all = self.getAll()
    for i in range(len(get_all)):
      if get_all[i][collum] ==  value:
        get_all[i][collumNewValue]  = newValue
    self.write(get_all)

  
  def delete(self, collum:int, value):
    get_all = self.getAll()
    i = 0
    while i <= len(get_all)-1:
      if get_all[i][collum] == value:
        get_all.pop(i)
      i += 1
    self.write(get_all)


  def write(self, prodList:list):
    data = prodList.copy()
    for i in range(len(data)):
      data[i][1] = str(data[i][1])
      data[i][2] = str(data[i][2])
      data[i][3] = str(data[i][3])
      data[i] = "|".join(data[i])
    data = '\n'.join(data) + '\n'
    data_base = open(self.file, 'w', encoding='utf-8')
    data_base.write(data)
    data_base.close()



# Classe mercado onde está as régras de negócio

class Market:
  def __init__(self):
    self.data_base = DataBase("db.txt")


  def create(self, userInput:list):
    if len(user_input) == 4:
      command, name, price, quanti = user_input
      self.data_base.create(name, price, quanti, randint(1, 1_000))
    else:
      print("Erro tem alguma coisa de errado na sua entrada. :(")


  def show(self):
    get_all = self.data_base.getAll()

    for i in range(len(get_all)):
      get_all[i][1] = f"R$ {get_all[i][1]:.2f}"

    print(table(["Produto", "preço", "Quantidade", "Id"], get_all))


  def shell(self, userInput:list):    
    if len(userInput) != 3:
      print("Sua entrada está inválida")
      return
    command, product, quant = user_input
    get_prod = self.data_base.getProd(0, product)
    if get_prod == -1:
      print("Produto inválido")
      return
    if get_prod[2] > 0 and int(quant) <= get_prod[2]:
      price = int(quant) * get_prod[1]
      print(f"Vendendo {product} o valor total é R$ {price}.")
      self.data_base.edit(0, product, 2, get_prod[2]-int(quant))
    else:
      print("Erro, não é possível comprar mais que nosso estoque possui.")


  def remove(self, userInput):
    if len(userInput) == 2:
      self.data_base.delete(0, user_input[1])
    else:
      print("Sua entrada está inválida")


  def replace(self, userInput):
    if len(user_input) < 3:
      print("Sua entrada está inválida")
      return

    command, product, quant = userInput
    prod = self.data_base.getProd(0, product)
    self.data_base.edit(0, product, 2, prod[2]+int(quant))
    

def help():
  comands = [
    "[help]   -> Mostrar este menu",
    "[exit]   -> sair",
    "[clear]  -> limpar tela",
    "[create] -> Para adicionar um produto novo.",
    "[sell]   -> Vender um produto",
    "[remove] -> Remover um produto",
    "[replace]-> Reabastecer o produto",
    "[show]   -> Mostrar todos os produtos",
  ]
  for i in range(len(comands)):
    print(comands[i])

runing = True

print("Escreva [help] para mais ajuda")
print("Para sair [exit]\n")

market = Market()

while runing:
  user_input = input(">>> ").split(' ')

  if user_input[0] == "exit":
    runing = False
  
  if user_input[0] == "help":
    help()

  if user_input[0] == "clear":
    if os.name == "nt":
      os.system("cls")
    elif os.name == "posix":
      os.system("clear")
  
  if user_input[0] == "create":
    market.create(user_input)
  
  if user_input[0] == "show":
    market.show()

  if user_input[0] == "remove":
    market.remove(user_input)

  if user_input[0] == "shell":
    market.shell(user_input)

  if user_input[0] == "replace":
    market.replace(user_input)


"""
+--------+--------+----------+-----+
|Produtos|Preço   |Quantidade|Id   |
+--------+--------+----------+-----+
|Maça    |R$ 2.50 |30        |20   |
|abacate |R$ 3.50 |90        |99999|
+--------+--------+----------+-----+
"""