import tkinter as tk
import tkinter.ttk as ttk

verbs = {
    'have': ('had', 'have', 'will have'),
    'do': ('did', 'do', 'will do'),
    'say': ('said', 'say', 'will say'),
    'go': ('went', 'go', 'will go'),
    'get': ('got', 'get', 'will get'),
    'make': ('made', 'make', 'will make'),
    'know': ('knew', 'know', 'will know'),
    'think': ('thought', 'think', 'will think'),
    'take': ('took', 'take', 'will take'),
    'see': ('saw', 'sees', 'will see'),
    'come': ('came', 'come', 'will come'),
    'want': ('wanted', 'want', 'will want'),
    'look': ('looked', 'look', 'will look'),
    'use': ('used', 'use', 'will use'),
    'find': ('found', 'find', 'will find'),
    'give': ('gave', 'give', 'will give'),
    'tell': ('told', 'tell', 'will tell'),
    'work': ('worked', 'work', 'will work'),
    'call': ('called', 'call', 'will call'),
    'try': ('tried', 'try', 'will try'),
    'ask': ('asked', 'ask', 'will ask'),
    'need': ('needed', 'need', 'will need'),
    'feel': ('felt', 'feel', 'will feel'),
    'become': ('became', 'become', 'will become'),
    'leave': ('left', 'leave', 'will leave'),
    'put': ('put', 'put', 'will put'),
    'mean': ('meant', 'mean', 'will mean'),
    'keep': ('kept', 'keep', 'will keep'),
    'let': ('let', 'let', 'will let'),
    'begin': ('began', 'begin', 'will begin'),
    'seem': ('seemed', 'seem', 'will seem'),
    'help': ('helped', 'help', 'will help'),
    'talk': ('talked', 'talk', 'will talk'),
    'turn': ('turned', 'turn', 'will turn'),
    'start': ('started', 'start', 'will start'),
    'show': ('showed', 'show', 'will show'),
    'hear': ('heard', 'hear', 'will hear'),
    'play': ('played', 'play', 'will play'),
    'run': ('ran', 'run', 'will run'),
    'move': ('moved', 'move', 'will move'),
    'like': ('liked', 'like', 'will like'),
    'live': ('lived', 'live', 'will live'),
    'believe': ('believed', 'believe', 'will believe'),
    'hold': ('held', 'hold', 'will hold'),
    'bring': ('brought', 'bring', 'will bring'),
    'happen': ('happened', 'happen', 'will happen'),
    'write': ('wrote', 'write', 'will write'),
    'provide': ('provided', 'provide', 'will provide'),
    'sit': ('sat', 'sit', 'will sit'),
    'stand': ('stood', 'stand', 'will stand'),
    'lose': ('lost', 'lose', 'will lose'),
    'pay': ('paid', 'pay', 'will pay'),
    'meet': ('met', 'meet', 'will meet'),
    'include': ('included', 'include', 'will include'),
    'continue': ('continued', 'continue', 'will continue'),
    'set': ('set', 'set', 'will set'),
    'learn': ('learned', 'learn', 'will learn'),
    'change': ('changed', 'change', 'will change'),
    'lead': ('led', 'lead', 'will lead'),
    'understand': ('understood', 'understand', 'will understand'),
    'watch': ('watched', 'watch', 'will watch'),
    'follow': ('followed', 'follow', 'will follow'),
    'stop': ('stopped', 'stop', 'will stop'),
    'create': ('created', 'create', 'will create'),
    'speak': ('spoke', 'speak', 'will speak'),
    'read': ('read', 'read', 'will read'),
    'allow': ('allowed', 'allow', 'will allow'),
    'add': ('added', 'add', 'will add'),
    'spend': ('spent', 'spend', 'will spend'),
    'grow': ('grew', 'grow', 'will grow'),
    'open': ('opened', 'open', 'will open'),
    'walk': ('walked', 'walk', 'will walk'),
    'win': ('won', 'win', 'will win'),
    'offer': ('offered', 'offer', 'will offer'),
    'remember': ('remembered', 'remember', 'will remember'),
    'love': ('loved', 'love', 'will love'),
    'consider': ('considered', 'consider', 'will consider'),
    'appear': ('appeared', 'appear', 'will appear'),
    'buy': ('bought', 'buy', 'will buy'),
    'wait': ('waited', 'wait', 'will wait'),
    'serve': ('served', 'serve', 'will serve'),
    'die': ('died', 'die', 'will die'),
    'send': ('sent', 'send', 'will send'),
    'build': ('built', 'build', 'will build'),
    'stay': ('stayed', 'stay', 'will stay'),
    'fall': ('fell', 'fall', 'will fall'),
    'cut': ('cut', 'cut', 'will cut'),
    'reach': ('reached', 'reach', 'will reach'),
    'kill': ('killed', 'kill', 'will kill'),
    'remain': ('remained', 'remain', 'will remain'),
    'suggest': ('suggested', 'suggest', 'will suggest'),
    'raise': ('raised', 'raise', 'will raise'),
    'pass': ('passed', 'pass', 'will pass'),
    'sell': ('sold', 'sell', 'will sell'),
    'require': ('required', 'require', 'will require'),
    'report': ('reported', 'report', 'will report'),
    'decide': ('decided', 'decide', 'will decide'),
    'pull': ('pulled', 'pull', 'will pull'),
    'visit': ('visited', 'visit', 'will visit'),
    'break': ('broke', 'break', 'will break'),
    'choose': ('chose', 'choose', 'will choose'),
    'draw': ('drew', 'draw', 'will draw'),
    'drive': ('drove', 'drive', 'will drive'),
    'eat': ('ate', 'eat', 'will eat'),
    'feed': ('fed', 'feed', 'will feed'),
    'fight': ('fought', 'fight', 'will fight'),
    'fly': ('flew', 'fly', 'will fly'),
    'forget': ('forgot', 'forget', 'will forget'),
    'forgive': ('forgave', 'forgive', 'will forgive'),
    'freeze': ('froze', 'freeze', 'will freeze'),
    'hang': ('hung', 'hang', 'will hang'),
    'hide': ('hid', 'hide', 'will hide'),
    'hit': ('hit', 'hit', 'will hit'),
    'hurt': ('hurt', 'hurt', 'will hurt'),
    'lay': ('laid', 'lay', 'will lay'),
    'lend': ('lent', 'lend', 'will lend'),
    'lie': ('lay', 'lie', 'will lie'),
    'light': ('lit', 'light', 'will light'),
    'quit': ('quit', 'quit', 'will quit'),
    'ride': ('rode', 'ride', 'will ride'),
    'ring': ('rang', 'ring', 'will ring'),
    'rise': ('rose', 'rise', 'will rise'),
    'shake': ('shook', 'shake', 'will shake'),
    'shoot': ('shot', 'shoot', 'will shoot'),
    'shut': ('shut', 'shut', 'will shut'),
    'sing': ('sang', 'sing', 'will sing'),
    'sink': ('sank', 'sink', 'will sink'),
    'sleep': ('slept', 'sleep', 'will sleep'),
    'slide': ('slid', 'slide', 'will slide'),
    'steal': ('stole', 'steal', 'will steal'),
    'stick': ('stuck', 'stick', 'will stick'),
    'strike': ('struck', 'strike', 'will strike'),
    'swear': ('swore', 'swear', 'will swear'),
    'sweep': ('swept', 'sweep', 'will sweep'),
    'swim': ('swam', 'swim', 'will swim'),
    'swing': ('swung', 'swing', 'will swing'),
    'teach': ('taught', 'teach', 'will teach'),
    'tear': ('tore', 'tear', 'will tear'),
    'throw': ('threw', 'throw', 'will throw'),
    'wake': ('woke', 'wake', 'will wake'),
    'wear': ('wore', 'wear', 'will wear'),
}

# List of 150 common adjectives in English
adjectives = [
    "big", "small", "tall", "short", "fat", "thin", "fast", "slow", "old", "young",
    "new", "old", "beautiful", "ugly", "clean", "dirty", "hot", "cold", "warm", "cool",
    "hard", "soft", "bright", "dark", "heavy", "light", "sweet", "bitter", "sour", "salty",
    "good", "bad", "smart", "stupid", "rich", "poor", "strong", "weak", "fresh", "rotten",
    "loud", "quiet", "long", "short", "full", "empty", "dry", "wet", "happy", "sad",
    "healthy", "sick", "important", "unimportant", "difficult", "easy", "true", "false", "pleasant", "unpleasant",
    "deep", "shallow", "sharp", "dull", "wide", "narrow", "open", "closed", "soft", "hard",
    "famous", "unknown", "simple", "complex", "expensive", "cheap", "useful", "useless", "rare", "common",
    "safe", "dangerous", "strong", "weak", "friendly", "unfriendly", "polite", "rude", "honest", "dishonest",
    "brave", "cowardly", "beautiful", "ugly", "interesting", "boring", "exciting", "dull", "happy", "miserable",
    "generous", "selfish", "kind", "cruel", "optimistic", "pessimistic", "reliable", "unreliable", "calm", "nervous",
    "patient", "impatient", "energetic", "lazy", "organized", "disorganized", "curious", "indifferent", "creative", "unimaginative",
    "sensitive", "insensitive", "warm-hearted", "cold-hearted", "ambitious", "unambitious", "helpful", "unhelpful", "thoughtful", "thoughtless",
    "determined", "indecisive", "loyal", "disloyal", "confident", "insecure", "hardworking", "lazy", "serious", "funny"
]

# List of 150 common nouns in English
nouns = [
    "time", "year", "people", "way", "day", "man", "thing", "woman", "life", "child",
    "world", "school", "state", "family", "student", "group", "country", "problem", "hand", "part",
    "place", "case", "week", "company", "system", "program", "question", "work", "government", "number",
    "night", "point", "home", "water", "room", "mother", "area", "money", "story", "fact",
    "month", "lot", "right", "study", "book", "eye", "job", "word", "business", "issue",
    "side", "kind", "head", "house", "service", "friend", "father", "power", "hour", "game",
    "line", "end", "member", "law", "car", "city", "community", "name", "president", "team",
    "minute", "idea", "kid", "body", "information", "back", "parent", "face", "others", "level",
    "office", "door", "health", "person", "art", "war", "history", "party", "result", "change",
    "morning", "reason", "research", "girl", "guy", "moment", "air", "teacher", "force", "education",
    "foot", "boy", "age", "policy", "process", "music", "market", "sense", "nation", "plan",
    "college", "interest", "death", "course", "someone", "experience", "effect", "control", "society", "view",
    "road", "police", "mind", "value", "office", "decision", "love", "quality", "action", "arm",
    "opportunity", "difference", "respect", "answer", "movement", "department", "manager", "event", "record", "paper"
]

tenses = ['past','present','future']


class SubjectFrame(tk.Frame):
    
    def __init__(self,master,label,adjectives,adjective_var:tk.StringVar,nouns,noun_var:tk.StringVar):
        super().__init__(master)
        self.toplabel = tk.Label(self,text=label)
        self.adjlabel = tk.Label(self,text="Adjective:")
        self.adj_cbox = ttk.Combobox(self,textvariable=adjective_var,values=adjectives,state='readonly')
        self.adj_cbox.current(0)
        self.nounlabel = tk.Label(self,text="Noun:")
        self.noun_cbox = ttk.Combobox(self,textvariable=noun_var,values=nouns,state='readonly')
        self.noun_cbox.current(0)
        
        self.toplabel.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky='ew')
        self.adjlabel.grid(row=1,column=0,padx=5,pady=5,sticky='ew')
        self.adj_cbox.grid(row=1,column=1,padx=5,pady=5,sticky='ew')
        self.nounlabel.grid(row=2,column=0,padx=5,pady=5,sticky='ew')
        self.noun_cbox.grid(row=2,column=1,padx=5,pady=5,sticky='ew')


class VerbFrame(tk.Frame):
    
    def __init__(self,master,verbs,verb_var:tk.StringVar,tenses,tense_var:tk.StringVar):
        super().__init__(master)
        self.toplabel = tk.Label(self,text="Verb")
        self.verblabel = tk.Label(self,text="Verb:")
        self.verb_cbox = ttk.Combobox(self,textvariable=verb_var,values=verbs,state='readonly')
        self.verb_cbox.current(0)
        self.tenselabel = tk.Label(self,text="Tense:")
        self.tense_cbox = ttk.Combobox(self,textvariable=tense_var,values=tenses,state='readonly')
        self.tense_cbox.current(0)
        
        self.toplabel.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky='ew')
        self.verblabel.grid(row=1,column=0,padx=5,pady=5,sticky='ew')
        self.verb_cbox.grid(row=1,column=1,padx=5,pady=5,sticky='ew')
        self.tenselabel.grid(row=2,column=0,padx=5,pady=5,sticky='ew')
        self.tense_cbox.grid(row=2,column=1,padx=5,pady=5,sticky='ew')
        
class SentenceFrame(tk.Frame):
    
    def __init__(self,master,sentence_var:tk.StringVar,button_command):
        super().__init__(master)
        self.button = tk.Button(self,text="Generate sentence",command=button_command)
        self.sentence_label = tk.Label(self,textvariable=sentence_var)
        
        self.button.grid(row=0,column=0,padx=5,pady=5,sticky='ew')
        self.sentence_label.grid(row=1,column=0,padx=5,pady=5,sticky='ew')

def generate_sentence(subject_adj,subject_noun,verb,tense,object_adj,object_noun):
    subject = f"The {subject_adj} {subject_noun}"
    if tense == 'past':
        verb = verbs[verb][0]
    elif tense == 'present':
        verb = verbs[verb][1]
    elif tense == 'future':
        verb = verbs[verb][2]
    object = f"the {object_adj} {object_noun}"
    
    return f"{subject} {verb} {object}"

window = tk.Tk()
window.title("Sentence generator")

adj_var1 = tk.StringVar(window)
noun_var1 = tk.StringVar(window)
subjectF = SubjectFrame(window,"Subject",adjectives,adj_var1,nouns,noun_var1)
subjectF.grid(row=0,column=0,padx=2,pady=2)

verb_var = tk.StringVar(window)
tense_var = tk.StringVar(window)
verbF = VerbFrame(window,list(verbs.keys()),verb_var,tenses,tense_var)
verbF.grid(row=0,column=1,padx=2,pady=2)

adj_var2 = tk.StringVar(window)
noun_var2 = tk.StringVar(window)
objectF = SubjectFrame(window,"Object",adjectives,adj_var2,nouns,noun_var2)
objectF.grid(row=0,column=2,padx=2,pady=2)

sentence_var = tk.StringVar(window,'---')
sentenceF = SentenceFrame(window,sentence_var,lambda: sentence_var.set(generate_sentence(
    adj_var1.get(),
    noun_var1.get(),
    verb_var.get(),
    tense_var.get(),
    adj_var2.get(),
    noun_var2.get()
)))
sentenceF.grid(row=1,column=0,columnspan=3,padx=2,pady=2)

window.mainloop()