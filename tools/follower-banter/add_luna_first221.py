"""Append Luna's lines to chosen talks in the first six Desktop scripts. Idempotent (skips talks already holding LUNA)."""
import os, re

DESK = r"C:\Users\User\Desktop"
ADD = {
 "FOLLOWER BANTER - SCRIPT BATCH 1.txt": {
  "A2": ["Wonderful. You'll balance each other out. One talks, one doesn't."],
  "A4": ["I can hear you, you know. And it was not a stylish beard."],
  "A5": ["Children. I'm travelling with children."],
  "A6": ["I'll have a tea. Thank you all. Very touching."],
  "A7": ["Or you could let the mage handle it from a sensible distance. Just a thought."],
  "A9": ["Both of you, quiet. Some of us are trying to be invisible."],
  "A10": ["Kaidan, are you alright? You walked into that tree like it owed you money."],
  "A13": ["I'm standing right here, you know."],
  "A16": ["I'd like to thank the frost spell that actually killed it."],
  "A21": ["What are you three whispering about?"],
  "A23": ["Or 'Luna'. It's right there. Two syllables."],
  "B2": ["Scrap likes you, Kaidan. That's more than he says about me."],
  "B3": ["I'm writing down both of your symptoms. For science."],
  "B8": ["Give him back the two septims, Remi."],
  "B10": ["Oh good. There are two of you now."],
  "B12": ["For the record, I asked Calcelmo nicely too. He told me to read a book. I'd read his."],
  "C1": ["Three hundred and sixty-five. That's... very precise, Lucien."],
  "C3": ["He's right about the comberry."],
 },
 "FOLLOWER BANTER - SCRIPT KAIDAN AND LUNA.txt": {
  "K5": ["Who's swooning? Lucien, are you writing limericks about me again?"],
  "K8": ["Kaidan, you've walked into that post twice. Do you need a potion?"],
  "K10": ["Did I overdo it? I think I knocked a goat off the mountain."],
  "K13": ["Morning, both of you. Please don't set anyone on fire before breakfast."],
  "K16": ["Whatever you two are making, I want horker in it."],
  "K18": ["It was a very good joke, Kaidan."],
  "K21": ["I do not snore."],
  "K29": ["Be nice, both of you. I have a fire spell and no patience."],
  "K30": ["Scrap would be an excellent uncle."],
  "K32": ["It was a very good sandwich."],
 },
 "FOLLOWER BANTER - SCRIPT BATCH 2.txt": {
  "R1": ["He's with me, Kaidan. He's... very with me."],
  "R8": ["Val, just get another bedroll."],
  "R9": ["Congratulations, Val. You have a crew again."],
  "R11": ["What am I, Redcap?", "REDCAP: Friend. Not. Fa-ka. Friend."],
  "R17": ["All hail Chief Redcap."],
  "R20": ["I do love a sweet roll."],
  "X1": ["Xelzaz, be nice. He carried your satchel for an hour."],
  "X5": ["If anyone gets that recipe, I want a copy."],
  "I1": ["You'll get along. You both steal my sweetrolls."],
  "L1": ["He means it kindly, Lucien. Mostly."],
  "L2": ["Lucien. Why do you have that?"],
  "G1": ["It's Gore. I could hear it from the next valley."],
  "G2": ["I agree with 'the' as well, for what it's worth."],
  "G3": ["I'm not paying for a lockbox."],
 },
 "FOLLOWER BANTER - SCRIPT QUESTS.txt": {
  "Q2": ["Nobody is putting me in anything Scrap-sized."],
  "Q4": ["Seven thousand two hundred, actually. I counted."],
  "Q5": ["She does have an agenda. It's mostly me."],
  "Q7": ["Keep practising, Redcap. It took me a dragon."],
  "Q11": ["Nobody is doing a heist without a plan. A written one."],
  "Q16": ["Please don't scratch my ears, Redcap."],
  "Q17": ["It was two spells, Lucien. And I'd read the whole syllabus."],
  "Q18": ["You may have a room, Xelzaz. Not the tower."],
  "Q22": ["I'm back. I'm fine. Never let me read anything again."],
 },
 "FOLLOWER BANTER - SCRIPT BATCH 3.txt": {
  "P1": ["It's named for the river, Redcap. Probably."],
  "P6": ["He was VERY red."],
  "P7": ["Kaidan, are you getting up to dance or to fight the bard?"],
  "W9": ["Mm. Just a few more minutes of quiet."],
  "W10": ["That's the Ritual, Val, not the Lover. You'd still hit Solstheim, though."],
  "W11": ["Kaidan, I don't think that's what your name means."],
  "D2": ["No exploding souvenirs, Redcap."],
  "D5": ["Very good, Gore. 'Falmer' even means 'elves of snow'."],
  "D9": ["Snobs. Both of you. Pass the salt."],
 },
 "FOLLOWER BANTER - SCRIPT SEASONS HOLIDAYS LOST.txt": {
  "S4": ["Autumn is also excellent reading weather."],
  "S6": ["It's a very good likeness, Redcap."],
  "H1": ["Mine is to finish my book. The one I've been finishing for three years."],
  "N1": ["I'm taking the scenic route."],
  "N2": ["The map is fine. North is wherever I say it is."],
  "N4": ["I heard that. It's a loop. Loops are efficient."],
  "N10": ["I can hear all of you. We are not lost. We're exploring."],
 },
}
head = re.compile(r"^([A-Z]{1,3}\d+)\. ")
for fn, adds in ADD.items():
    p = os.path.join(DESK, fn)
    raw = open(p, "rb").read(); nl = "\r\n" if b"\r\n" in raw else "\n"
    L = raw.decode("utf-8").split(nl)
    out, cur, done, i = [], None, 0, 0
    # find each talk's last speaker line and insert after it
    talks = {}
    for idx, s in enumerate(L):
        m = head.match(s)
        if m: cur = m.group(1); talks[cur] = {"lines": [], "luna": False}
        elif cur and re.match(r"^[A-Z]+:\s", s):
            talks[cur]["lines"].append(idx)
            if s.startswith("LUNA:"): talks[cur]["luna"] = True
    inserts = {}
    for tid, lines in adds.items():
        t = talks.get(tid)
        if not t: print("missing", fn, tid); continue
        if t["luna"]: continue
        new = [x if re.match(r"^[A-Z]+:", x) else "LUNA:   " + x for x in lines]
        new = [re.sub(r"^REDCAP:\s*", "REDCAP: ", x) for x in new]
        inserts[t["lines"][-1]] = new; done += 1
    for idx, s in enumerate(L):
        out.append(s)
        if idx in inserts: out.extend(inserts[idx])
    open(p, "wb").write(nl.join(out).encode("utf-8"))
    print(fn, "added Luna to", done)
