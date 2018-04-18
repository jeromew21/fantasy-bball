import league, pickle, sys

def save(l):
    with open(league.SAVE_DIR + l.name + '.dat', 'wb') as f:
        pickle.dump(l, f)

def load(filename):
    try:
        savefile = open(league.SAVE_DIR + filename, "rb")
        return pickle.load(savefile)
    except:
        return False

lg = None

if len(sys.argv) == 1:
    lg = league.League()
    save(lg)
else:
    lg = load(sys.argv[1])
    if not lg:
        lg = league.League()
        save(lg)

players = league.allPlayers()
players = list(reversed(sorted(players, key=lambda p: p.getRating())))

def leave():
    save(lg)
    sys.exit()

def save_lg():
    save(lg)
    print("Saved.")

commands = {
    'exit': leave,
    'save': save_lg
}

while True:
    cmd = input('Command:')
    if cmd in commands:
        commands[cmd]()
    else:
        print('Command not found')