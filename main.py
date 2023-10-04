import random, copy

EULER_NUM = 2.7182818284590452353602874713527
networks = []
orderedDeck = []
deck = []
deckPointer = 0
playerHand = []
dealerHand = []
gameScore = 0
gameOver = False
gameTextDisplayed = False

#Activation function
def Sigmoid(value):
  return(1 / (1 + EULER_NUM ** (-value)))


class Neuron:
  def __init__(self, layer, pos, value):
    self.layer = layer
    self.pos = pos
    self.value = value

class Network:
  def __init__(self, neuronsInLayers, weights, biases):
    self.neuronsInLayers = neuronsInLayers
    self.weights = weights
    self.biases = biases
    self.neurons = []
    self.fitness = 0
    
    for i in range(len(neuronsInLayers)):
      self.neurons.append([])
      for j in range(neuronsInLayers[i]):
        self.neurons[i].append(Neuron(i, j, 0))
  
  #Calculating each neuron
  def FeedForward(self, layer, pos):
    sum = 0
    
    for i in range(self.neuronsInLayers[layer-1]):
      sum += self.neurons[layer-1][i].value * self.weights[layer-1][i][pos]
    
    sum += self.biases[layer][pos]
    return Sigmoid(sum)

  def UpdateForward(self):
    for layer in range(1, len(self.neurons)):
      for pos in range(len(self.neurons[layer])):
        self.neurons[layer][pos].value = self.FeedForward(layer, pos)
  
  #Calculates the fitness
  def CalculateFitness(): 
    inputNum = 0;
    lossNum = 0;
   
    return(lossNum);

  def SetInputs(self, inputs):
    for i in range(5):
      self.neurons[0][i].value = inputs[i]

  def GetOutputs(self):
    outputs = []
    for i in range(self.neuronsInLayers[len(self.neuronsInLayers)-1]):
      outputs.append(self.neurons[len(self.neurons)-1][i].value)
    return outputs
  
  def Print(self):
    for i in range(len(self.neuronsInLayers)):
      text = ""
      for j in range(len(self.neurons[i])):
        val = str(round(self.neurons[i][j].value * 10) / 10)
        text += " "*(8-len(val)) + val
      print(text)
      
      if i > 0:
        btext = ""
        for j in range(len(self.biases[i])):
          bval = str(round(self.biases[i][j] * 10) / 10)
          btext += " "*(8-len(bval)) + bval
        print(btext)

      print()


  def createChildNetwork(self):

    BIAS_VARIANCE = 2
    WEIGHT_VARIANCE = 2
    childWeights = copy.deepcopy(self.weights)
    childBiases = copy.deepcopy(self.biases)

    for layer in childBiases:
      for i in range(len(layer)):
        layer[i] += random.uniform(-1, 1) * BIAS_VARIANCE
    
    for i in childWeights:
      for j in i:
        for k in range(len(j)):
          j[k] += random.uniform(-1, 1) * WEIGHT_VARIANCE

    return Network(self.neuronsInLayers, childWeights, childBiases)
  
  def becomeChildNetwork(self, parentNetwork):

    BIAS_VARIANCE = 2
    WEIGHT_VARIANCE = 2
        
    for i in range(len(self.biases)):
      for j in range(len(self.biases[i])):
        self.biases[i][j] = parentNetwork.biases[i][j] + random.uniform(-1, 1) * BIAS_VARIANCE
    
    for i in range(len(self.weights)):
      for j in range(len(self.weights[i])):
        for k in range(len(self.weights[i][j])):
          self.weights[i][j][k] = parentNetwork.weights[i][j][k] + random.uniform(-1, 1) * WEIGHT_VARIANCE


#For sorting networks
def getFitness(self):
  return self.fitness

class Card:
  def __init__(self, suit, value):
    self.suit = suit
    self.value = value
  def __str__(self):
    return CardToText(self)

NEW_DECK = []
for suit in range(4):
  for value in range(1, 14):
    NEW_DECK.append(Card(suit, value))


#BlackJack functions
def CardToText(card):
  match card.value:
    case -1:
      return ""
    case 1:
      return "A"
    case 11:
      return "J"
    case 12:
      return "Q"
    case 13:
      return "K"
    case _:
      return str(card.value)
  
def ShuffleDeck():
  global deck, deckPointer
  random.shuffle(deck)

def DealCard():
  global deck, deckPointer
  randCard = deck[deckPointer]
  deckPointer += 1
  return(randCard)

def CardsInHand(hand):
  count = 0
  for card in hand:
    if card.value != -1:
      count += 1
  return count

def Hit(person):
  global playerHand
  global dealerHand
  
  if person == "player":
    pos = CardsInHand(playerHand)
    playerHand[pos] = DealCard()
  elif person == "dealer":
    pos = CardsInHand(dealerHand)
    dealerHand[pos] = DealCard()

def EvaluateHand(hand):
  sum = 0
  hasAce = False
  
  for card in hand:
    if card.value != -1:
      sum += min(card.value, 10)
      if card.value == 1:
        hasAce = True

  if hasAce and sum <= 11:
    sum += 10
  
  return sum

def DealStartingCards():
  global playerHand
  global dealerHand
  playerHand = [Card(-1, -1) for i in range(5)]
  dealerHand = [Card(-1, -1) for i in range(10)]
  
  for i in range(2):
    Hit("player")
    Hit("dealer")

def EvaluateRound():
  while EvaluateHand(dealerHand) < 17:
    Hit("dealer")
  playerScore = EvaluateHand(playerHand)
  dealerScore = EvaluateHand(dealerHand)
  if dealerScore >= 22:
    return 1
  
  if playerScore < dealerScore:
    return -1
  elif playerScore > dealerScore:
    return 1
  else:
    return 0

def MakeMove(move):
  global gameOver, gameScore
  if move == "hit":
    Hit("player")
    playerScore = EvaluateHand(playerHand)
    if playerScore > 21:
      gameScore = -1
      if gameTextDisplayed:
        print(f"Dealer's Hand: {dealerHand[0]}")
        print("Player's Hand: " + " ".join(map(CardToText, playerHand)))
        print("Bust!")
        outCome = "win"
      gameOver = True
    elif playerScore == 21:
      gameScore = 1
      if gameTextDisplayed:
        print(f"Dealer's Hand: {dealerHand[0]}")
        print("Player's Hand: " + " ".join(map(CardToText, playerHand)))
        print("You win!")
      gameOver = True
    if CardsInHand(playerHand) == 5 and playerScore <= 21:
      gameScore = 1
      if gameTextDisplayed:
        print(f"Dealer's Hand: {dealerHand[0]}")
        print("Player's Hand: " + " ".join(map(CardToText, playerHand)))
        print("You win!")
      gameOver = True
  elif move == "stand":
    gameScore = EvaluateRound()
    if gameTextDisplayed:
      print("Dealer's Hand: " + " ".join(map(CardToText, dealerHand)))
      print("Player's Hand: " + " ".join(map(CardToText, playerHand)))
      if gameScore > 0:
        print("You win!")
      elif gameScore < 0:
        print("You lose!")
      else:
        print("Tie!")
    gameOver = True

def CreateRandomNetworks(amount):
  global networks
  
  for num in range(amount):
    networkLayers = [5, 10, 10, 10, 2]
    networkWeights = [[[] for j in range(networkLayers[i])] for i in range(len(networkLayers)-1)]
    networkBiases = [[] for i in range(len(networkLayers))]
    
    for i in range(1, len(networkLayers)):
      for j in range(networkLayers[i]):
        networkBiases[i].append(random.uniform(-1, 1))
    
    for i in range(0, len(networkLayers)-1):
      for j in range(networkLayers[i]):
        for k in range(networkLayers[i+1]):
          networkWeights[i][j].append(random.uniform(-1, 1))
     
    networks.append(Network(networkLayers, networkWeights, networkBiases))

def RunNetwork(network):
  networkInput = []
  for i in range(4):
    val = max(0, playerHand[i].value)
    networkInput.append(val/13)
  networkInput.append(max(0, dealerHand[0].value))
  network.SetInputs(networkInput)
  network.UpdateForward()
  outputs = network.GetOutputs()
  return outputs


def PlayGame(network, orderedDeck):
  global gameOver, gameScore, deck, playerHand, dealerHand, deckPointer
  
  #Game Init
  deckPointer = 0

  DealStartingCards()
  # print(f"Dealer's Hand: {dealerHand[0]}")
  # print("Player's Hand: " + " ".join(map(CardToText, playerHand)))
  gameOver = False
  
  while gameOver == False:
    #Player moves
    # move = input()
    # MakeMove(move)

    if CardsInHand(playerHand) == 2 and EvaluateHand(playerHand) == 21:
      gameScore = 1
      if gameTextDisplayed:
        print(f"Dealer's Hand: {dealerHand[0]}")
        print("Player's Hand: " + " ".join(map(CardToText, playerHand)))
        print("You win!")
      gameOver = True
      break
    
    #AI moves
    output = RunNetwork(network)
    if output[0] > output[1]:
      move = "hit"
    else:
      move = "stand"
    MakeMove(move)

  network.fitness += gameScore



CreateRandomNetworks(24)
print("The number of networks is:", len(networks))
#print("The fitness of the networks:")

def tempIterateGeneration(numIterations):
  global networks, gameOver, gameScore, deck, orderedDeck, playerHand, dealerHand, gameTextDisplayed, NEW_DECK
  
  deck = copy.deepcopy(NEW_DECK)
  for i in range(300):
    ShuffleDeck()
    for network in networks:
      PlayGame(network, deck)
 
  totalFitness = 0
  numGenerations = 0
  totalNumGenerations = 0
  for iteration in range(numIterations):
    
    networks.sort(reverse=True, key=getFitness)
    
    tempGameTextDisplayed = gameTextDisplayed
    gameTextDisplayed = True
    print("A random game from the most fit network:")
    PlayGame(networks[0], orderedDeck)
    gameTextDisplayed = tempGameTextDisplayed
    
    # for network in networks
    #   print(network.fitness, end=" ")
    # print()
    
    
    # networks = networks[0:len(networks)//3]
    
    # networksChildren = []
    # for network in networks:
    #   networksChildren.append(network.createChildNetwork())
    # networks += networksChildren

    # while(len(networks) < 24):
    #   networks.append(networks[0].createChildNetwork())

    childCounter = 0
    for network in networks[8:15]:
      network.becomeChildNetwork(networks[childCounter])
      childCounter += 1

    for network in networks[16:]:
      network.becomeChildNetwork(networks[0])

    
    
    # print("result: ")
    for network in networks:
      network.fitness = 0 
      
    for i in range(1000):
      ShuffleDeck()
      
      for network in networks:
        PlayGame(network, deck)

    totalGenFitness = 0
    counter = 0
    if(numGenerations >= 100):
      numGenerations = 0
      totalFitness = 0
    print("The fitness of the networks:")
    for network in networks:
      print(network.fitness, end=" ")
      if counter < 1:#len(networks)/2:
        totalGenFitness += network.fitness
      counter += 1
    totalFitness += totalGenFitness
    numGenerations += 1
    totalNumGenerations += 1
    print("\nTotal Generations: ", totalNumGenerations, " Generations % 100: ", numGenerations, " Generation's Fitness : ", totalGenFitness, " Average Fitness since last 100th generation: ", totalFitness/numGenerations)
    
if __name__ == "__main__": 
  tempIterateGeneration(20000) 
