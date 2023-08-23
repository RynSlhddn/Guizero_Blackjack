from guizero import App, Box, PushButton, Slider, Text, Window
from random import shuffle
from time import sleep

def getDeck():
    global deck
    deck = []
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    for suit in [HEARTS, DIAMONDS, SPADES, CLUBS]:
        for value in values:
          deck.append((value, suit))
        shuffle(deck)

def getBet():
    global bet
    bet = betSlider.value
    betSlider.hide()
    cashIn.hide()
    feedback.value = f"You have bet {bet}"
    deal()
    
def deal():
    global playerHand, dealerHand, pNewTotal
    dealer.show()
    player.show()
    buttons.show()
    dd.show()
    dealerHand = [deck.pop(), deck.pop()]
    playerHand = [deck.pop(), deck.pop()]
    #playerHand = [('Q', '♣'), ('A', '♣')] #for testing
    pNewTotal = showTotal(playerHand)
    playerHandText.value = showHand(playerHand, True)
    playerTotalText.value = pNewTotal
    dealerHandText.value = showHand(dealerHand, False)
    dealerTotalText.value = back
    if showTotal(playerHand) == 21:
        playerBlackjack()
    

def hitMe():
    global doublingDown, pNewTotal
    dd.hide()
    playerHand.append(deck.pop())
    pNewTotal = showTotal(playerHand)
    playerHandText.value = showHand(playerHand, True)
    playerTotalText.value = pNewTotal
    if pNewTotal < 21:
        if doublingDown:
            app.after(3000, dealerTurn)
    elif pNewTotal == 21:
        playerBlackjack()
    else:
        playerBusted()
            
def doubleDown():
    global bet, doublingDown
    bet = min(money, bet*2)
    buttons.hide()
    feedback.value = f"Your bet is now {bet}"
    doublingDown = True
    app.after(3000, hitMe)

def playerBlackjack():
    feedback.value = "BLACKJACK!"
    buttons.hide()
    app.after(3000, dealerTurn)

def playerBusted():
    global money, broke
    feedback.value = "Busted!"
    dealer.hide()
    money -= bet
    betSlider.end = money
    if money == 0 and not broke:
        broke = True
        app.warn("YOU'RE BROKE!","You may continue playing without any money change if you please.")
    showPlayAgain()

def reveal():
    global dNewTotal
    dealerHandText.value = showHand(dealerHand, True)
    dNewTotal = showTotal(dealerHand)
    dealerTotalText.value = dNewTotal
   
def dealerTurn():
    global dNewTotal, revealed, wait
    if not revealed:
        revealed = True
        buttons.hide()
        feedback.value = "Dealer's turn\nThe Dealer reveals his face down card, along with his total"
    reveal()
    app.update()
    if len(dealerHand) == 2:
        sleep(wait)
    if dNewTotal < 17:
        dealerHit()
    elif dNewTotal > 21:
        dealerBusted()
    elif dNewTotal == 21:
        dealerBlackjack()
    else:
        dealerStands()
        
def dealerHit():
    card = deck.pop()
    dealerHand.append(card)
    dealerHandText.value = showHand(dealerHand, True)
    dNewTotal = showTotal(dealerHand)
    dealerTotalText.value = dNewTotal
    feedback.value = "Dealer hits"
    app.after(3000, dealerTurn)

def dealerBusted():
    feedback.value = "Dealer busted!"
    if pNewTotal > 21:
        app.after(2000, lose)
    else:
        app.after(2000, win)
    
def dealerBlackjack():
    feedback.value = "Dealer has BLACKJACK!"
    if pNewTotal == 21:
        app.after(2000, tie)
    else:
        app.after(2000, lose)
    
def dealerStands():
    feedback.value = "Dealer stands"
    if pNewTotal == 21 or pNewTotal > dNewTotal:
        app.after(2000, win)
    elif pNewTotal < dNewTotal:
        app.after(2000, lose)
    else:
        app.after(2000, tie)
    
def tie():
    feedback.value = "You tied with the dealer and keep your money"
    showPlayAgain()

def win():
    global money
    feedback.value = "You won! Your bet is added to your money"
    money += bet
    betSlider.end = money
    showPlayAgain()
    
def lose():
    global money
    feedback.value = "You lost! Your bet is deducted from your money"
    money -= bet
    betSlider.end = money
    showPlayAgain()
    
def showPlayAgain():
    playAgain.show()
    buttons.hide()

def replay():
    betSlider.show()
    cashIn.show()
    feedback.clear()
    playAgain.hide()
    dealer.hide()
    player.hide()
    buttons.hide()

def showHand(hand, includeFirstCard):
    if includeFirstCard:
        cards = hand
        s = ''
    else:
        cards = hand[1:]
        s = BACK + ' '
    for card in cards:
        s += cardName(card) + ' '
    return s

def showTotal(hand):
    total = 0
    numAces = 0
    for card in hand:
        value = cardValue(card)
        total += value
        if value == 11:
            numAces += 1
        if total > 21 and numAces > 0:
            total -= 10
            numAces -= 1
    return total
    
def cardName(card):
    value, suit = card
    return value + suit

def cardValue(card):
    value, suit = card
    if value in ['J', 'Q', 'K']:
        return 10
    elif value == 'A':
        return 11
    else:
        return int(value)

# - - - - - - - - - - - - - - - - - - M A I N _ C O D E - - - - - - - - - - - - - - - - - - - - -

app = App(title="B L A C K J A C K", bg="#237136", width=640, height=480)

TC = "white"
FONT = "Verdana"

HEARTS = '♥'
DIAMONDS = '♦'
SPADES = '♠'
CLUBS = '♣'
BACK = "[face down card]"
back = "???"

startMoney = 5000
money = startMoney
bet = 0

broke = False
doublingDown = False
revealed = False
wait = 3

Box(app, height=5, width="fill")

dealer = Box(app, width=app.width*0.95, height=100, border=2)
dealerTitle = Text(dealer, text="Dealer: ", size=18, color=TC, font=FONT, align="left")
dealerHandText = Text(dealer, text="", size=18, color=TC, font=FONT, align="left")
dealerTotalText = Text(dealer, text="", size=18, color=TC, font=FONT, align="right")

Box(app, height=10, width="fill")

player = Box(app, width=app.width*0.95, height=100, border=2)
playerTitle = Text(player, text="Player: ", size=18, color=TC, font=FONT, align="left")
playerHandText = Text(player, text="", size=18, color=TC, font=FONT, align="left")
playerTotalText = Text(player, text="", size=18, color=TC, font=FONT, align="right")
dealer.bg = player.bg = "green"

Box(app, height=10, width="fill")

gambling = Box(app, width="fill")
betSlider = Slider(gambling, start=0, end=money, width=300)
betSlider.text_size = 18
betSlider.text_color = TC
betSlider.font = FONT
betSlider.bg = "green"
Box(gambling, height=10, width="fill")
cashIn = PushButton(gambling, text="Place Bet", width=5, command=getBet)
cashIn.bg = "#eeeeee"

Box(app, height=5, width="fill")

buttons = Box(app, width=190, height=50)
hit = PushButton(buttons, align="left", text="Hit", command=hitMe)
stand = PushButton(buttons, align="left", text="Stand", command=dealerTurn)
dd = PushButton(buttons, align="left", text="Double Down", command=doubleDown)
hit.bg = stand.bg = dd.bg = "gold"

feedback = Text(app, text="", size=16, color=TC, font=FONT)

Box(app, height=15, width="fill")

playAgain = PushButton(app, align="top", text="Play Another Hand", command=replay)
playAgain.bg = "green"
playAgain.text_color = TC

playAgain.hide()
dealer.hide()
player.hide()
buttons.hide()

ruleBox = Window(app, width=870, height=490, bg="#111111", title="Blackjack Rules")
rules = Text(ruleBox, font=FONT, color=TC, text='''
Try to get as close to 21 without going over, which is known as busting

Kings, Queens and Jacks are worth 10 points
Aces are worth 11 or 1 points, depends on how many you have
Cards 2 through 10 are worth their face value

Hit to take another card
Stand to stop taking cards
Double down doubles ones bet, and then hits only one more time before standing
Double down may only be used on your first turn

The dealer stops hitting at 17

If both the dealer and the player have blackjack then it is a draw and your money value is indifferent
The player immdiately looses upon busting
If only the dealer busts, the player wins
If there is only one blackjack, whoever has it wins
If both the dealer and the player have normal cards, then the person with the higher value wins

Winning adds your bet to your money count, and losing subtracts so

''')
kill = PushButton(ruleBox, text="Kill this window", command=ruleBox.destroy)
kill.bg = "#222222"
kill.text_color = "red"

getDeck()

app.display()