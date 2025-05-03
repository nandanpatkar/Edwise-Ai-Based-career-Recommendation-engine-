
import streamlit as st

def iq_test():
    st.subheader("🧠 Aptitude Test")
    score = 0
    
    questions = {
        "What comes next: 2, 4, 8, 16?": ("32", ["20", "24", "32", "64"]),
        "If CAT is to DOG, BLACK is to?": ("WHITE", ["BLUE", "WHITE", "BROWN", "DARK"]),
        "Which word in brackets is most opposite in meaning to the word in capitals? EXPEDITE": ("curb", ["dispatch", "dismiss", "curb", "conclude"]),
        "How many minutes is it before noon if 29 minutes ago it was six times as many minutes past 10 am?": ("13 minutes", ["13 minutes", "15 minutes", "10 minutes", "16 minutes"]),
        "Which is the odd one out?": ("interpret", ["dilate", "elaborate", "expatiate", "interpret"]),
        "What comes next: 7 9 5 11 4 15 12 7 13 8 11 ?" : ("11", ["8", "10", "11", "13"]),
        "What comes next: 2 5 7 4 7 5 3 6 ?": ("6", ["4", "6", "8", "10"]),
        "What comes next: 2, 5, 8, 11, ?": ("14", ["8", "12", "14", "16"]),
        "What comes next: 121, 144, 169, 196, ?": ("225", ["225", "230", "275", "221"]),
        "What comes next: 4, 6, 9, 6, 14, 6, ?": ("19", ["14", "9", "16", "19"]),
        "What comes next: 2, 3, 5, 9, 17, 33, 65, ?": ("129", ["104", "129", "97", "135"]),
        "What comes next: 1, 3, 12, 52, 265, ?": ("1596", ["1188", "1390", "1489", "1596"]),
        "What comes next: 2, 8, 26, 62, 122, 212, ?": ("338", ["338", "339", "340", "341"]),
        "What is the name given to a group of BUTLERS?": ("draught", ["blast", "host", "draught", "staff"]),
        "What is a CURRICLE?": ("a vehicle", ["a vehicle", "a boat", "a curtain", "a vegetable"]),
        "Which word means the same as NEGATORY?": ("trifling", ["fallacious", "prodigious", "trifling", "restraining"]),
        "What is always associated with FAIENCE?": ("pottery", ["pottery", "fairies", "zinc", "ghosts"]),
        "Which of the following is not an anagram of an animal?": ("MOMS HOUR", ["BRISK PONG", "PUNCH KIM", "RED OPAL", "MOMS HOUR"]),
        "Which word in brackets means the same as the word in capitals? PROGENY": ("lineage", ["skill", "lineage", "movement", "vocation"]),
        "PERIGEE : APOGEE PERIHELION: ?": ("aphelion", ["aphelion", "eliptic", "orrery", "nadir"]),
        "What is a FERRULE?": ("a metal band", ["a metal band", "a circus wheel", "a window", "a funeral"]),
    }

    for q, (correct, options) in questions.items():
        answer = st.radio(q, options, key=q)
        if answer == correct:
            score += 1

    if st.button("Submit IQ Test", key="iq_submit"):
        normalized_score = score * 10
        st.session_state["iq_score"] = normalized_score  # ✅ Store it
       # st.success(f"Your IQ score is: {normalized_score}")
        return normalized_score

    # Return from session state if already submitted
    return st.session_state.get("iq_score", None)


















































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































# import streamlit as st

# def iq_test():
#     st.subheader("🧠 IQ Test")
#     score = 0
    
#     questions = {
#         "What comes next: 2, 4, 8, 16?": ("32", ["20", "24", "32", "64"]),
#         "If CAT is to DOG, BLACK is to?": ("WHITE", ["BLUE", "WHITE", "BROWN", "DARK"]),
#         "Which word in brackets is most opposite in meaning to the word in capitals? EXPEDITE": ("curb", ["dispatch", "dismiss", "curb", "conclude"]),
#         "How many minutes is it before noon if 29 minutes ago it was six times as many minutes past 10 am?": ("13 minutes", ["13 minutes", "15 minutes", "10 minutes", "16 minutes"]),
#         "Which is the odd one out?": ("interpret", ["dilate", "elaborate", "expatiate", "interpret"]),
#         "What comes next: 7 9 5 11 4 15 12 7 13 8 11 ?" : ("11", ["8", "10", "11", "13"]),
#         "What comes next: 2 5 7 4 7 5 3 6 ?": ("6", ["4", "6", "8", "10"]),
#         "What comes next: 2, 5, 8, 11, ?": ("14", ["8", "12", "14", "16"]),
#         "What comes next: 121, 144, 169, 196, ?": ("225", ["225", "230", "275", "221"]),
#         "What comes next: 4, 6, 9, 6, 14, 6, ?": ("19", ["14", "9", "16", "19"]),
#         "What comes next: 2, 3, 5, 9, 17, 33, 65, ?": ("129", ["104", "129", "97", "135"]),
#         "What comes next: 1, 3, 12, 52, 265, ?": ("1596", ["1188", "1390", "1489", "1596"]),
#         "What comes next: 2, 8, 26, 62, 122, 212, ?": ("338", ["338", "339", "340", "341"]),
#          "What is the name given to a group of BUTLERS?": ("draught", ["blast", "host", "draught", "staff"]),
#         "What is a CURRICLE?": ("a vehicle", ["a vehicle", "a boat", "a curtain", "a vegetable"]),
#         "Which word means the same as NEGATORY?": ("trifling", ["fallacious", "prodigious", "trifling", "restraining"]),
#         "What is always associated with FAIENCE?": ("pottery", ["pottery", "fairies", "zinc", "ghosts"]),
#         "Which of the following is not an anagram of an animal?": ("MOMS HOUR", ["BRISK PONG", "PUNCH KIM", "RED OPAL", "MOMS HOUR"]),
#         "Which word in brackets means the same as the word in capitals? PROGENY": ("lineage", ["skill", "lineage", "movement", "vocation"]),
#         "PERIGEE : APOGEE PERIHELION: ?": ("aphelion", ["aphelion", "eliptic", "orrery", "nadir"]),
#         "What is a FERRULE?": ("a metal band", ["a metal band", "a circus wheel", "a window", "a funeral"]),
        
#     }

#     for q, (correct, options) in questions.items():
#         answer = st.radio(q, options, key=q)
#         if answer == correct:
#             score += 1

#     if st.button("Submit IQ Test"):
#         normalized_score = score * 10 
#         st.success(f"Your IQ score is: {normalized_score}")
#         return normalized_score
    
#     return st.session_state.get("iq_score", None)  # fallback if resubmitting

#     if st.button("Submit IQ Test"):
#       st.session_state["iq_score"] = score * 10 










# import random

# def iq_test():
#     st.subheader("🧠 IQ Test")

#     score = 0

    # questions = {
    #     "What comes next: 2, 4, 8, 16?": ("32", ["20", "24", "32", "64"]),
    #     "If CAT is to DOG, BLACK is to?": ("WHITE", ["BLUE", "WHITE", "BROWN", "DARK"]),
    #     "What comes next: 7 9 5 11 4 15 12 7 13 8 11 ?": ("11", ["8", "10", "11", "13"]),
    #     "What comes next: 2 5 7 4 7 5 3 6 ?": ("6", ["4", "6", "8", "10"]),
    #     "What comes next: 2, 5, 8, 11, ?": ("14", ["8", "12", "14", "16"]),
    #     "What comes next: 121, 144, 169, 196, ?": ("225", ["225", "230", "275", "221"]),
    #     "What comes next: 4, 6, 9, 6, 14, 6, ?": ("19", ["14", "9", "16", "19"]),
    #     "What comes next: 2, 3, 5, 9, 17, 33, 65, ?": ("129", ["104", "129", "97", "135"]),
    #     "What comes next: 1, 3, 12, 52, 265, ?": ("1596", ["1188", "1390", "1489", "1596"]),
    #     "What comes next: 2, 8, 26, 62, 122, 212, ?": ("338", ["338", "339", "340", "341"]),
    #     "What comes next: 13, 17, 19, 23, 29, ?": ("31", ["30", "31", "33", "34"]),
    #     "What comes next: 2, 3, 6, 11, 18, 27, ?": ("38", ["21", "28", "38", "41"]),
    #     "What comes next: 2, 2, 4, 12, 48, 240, ?": ("1440", ["347", "567", "1009", "1440"]),
    #     "What comes next: 3 2 2 5 5 5 7 8 8 9 11 11 ?": ("11", ["11", "12", "13", "15"]),
#         "What comes next: 1 3 2 6 3 11 4 18 5 ?": ("27", ["20", "25", "27", "29"]),
#         "What comes next: 13 17 23 29 31 37 ?": ("41", ["39", "41", "49", "55"]),
#         "What comes next: 17 16 14 12 11 8 8 ?": ("4", ["None of the above", "11", "3", "4"]),
#         "What comes next: 9 11 13 ?": ("None of the above", ["None of the above", "14", "16", "17"]),
#         "What comes next: 5, 6, 9, 14, 21, ?": ("30", ["None of the above", "30", "31", "36"]),
#         "What comes next: 40, 30, 22, 16, ?": ("12", ["12", "10", "14", "30"]),
#         "What comes next: 1, 3, 6, 11, 18, ?": ("29", ["20", "24", "25", "29"]),
#         "What comes next: 32, 19, 8, ?": ("1", ["1", "3", "5", "10"]),
#         "What comes next: 1, 3, 9, 27, 81, ?": ("243", ["216", "243", "250", "none of the above"]),
#         "What comes next: 1, 2, 6, 15, 31, ?": ("56", ["44", "56", "60", "none of the above"]),
#         "What comes next: 71, 55, 46, 42, ?": ("41", ["41", "40", "39", "60"]),
#         "What comes next: 1, 2, 10, 37, 101, ?": ("226", ["402", "206", "226", "178"]),
#         "What comes next: 225, 100, 36, 9, 1, ?": ("0", ["11", "-5", "6", "0"]),
#         "What comes next: 13, 25, 51, 101, 203, ?": ("405", ["306", "344", "405", "406"]),
#         "What comes next: 5, 11, 23, 47, 95, ?": ("199", ["176", "191", "199", "207"]),
#         "What comes next: 1, 2, 2, 4, 3, 8, 7, 10, ?": ("11", ["9", "8", "13", "11"]),
#         "What comes next: 831, 842, 853, 864, 875, ?": ("886", ["880", "886", "890", "892"]),
#         "What comes next: 74, 83, 92, 101, 110, ?": ("119", ["118", "119", "120", "122"]),
#         "What comes next: 8 10 14 18 ?": ("26", ["20", "26", "28", "30"]),
#         "What comes next: 16 (31) 47 ?": ("27", ["37", "21", "15", "27"]),
#         "What comes next: 7 9 8 6 10 9 5 11 10 ?": ("4", ["4", "5", "11", "29"]),
#         "What comes next: ? 9 27 81 ?": ("3", ["0", "1", "3", "5"]),
#         "What comes next: 144, ?, 206, 240 ?": ("174", ["155", "167", "170", "174"]),
#         "What comes next: 16, 64, ?, 1024, 4096 ?": ("256", ["98", "156", "256", "298"]),
#         "What comes next: 56, 75, 94, ?, 132 ?": ("113", ["113", "128", "130", "131"]),
#         "What comes next: 19, 57, ?, 513 ?": ("171", ["88", "171", "333", "467"]),
#         "What comes next: 2448, 408, 68, ?": ("17", ["9", "11", "17", "29"]),
#         "What comes next: 68, ?, 86, 95, 104 ?": ("77", ["77", "11", "17", "29"]),
#         "What comes next: -9, -6, -3, ?, 3 ?": ("0", ["3", "4", "5", "0"]),
#         "What comes next: 498 668 ? 974 ?": ("896", ["699", "966", "896", "716"]),
#         "What comes next: 64, ?, 1024, 4096 ?": ("256", ["98", "167", "199", "256"]),
#         "What comes next: 169, ?, 225, 256, 289 ?": ("196", ["176", "196", "199", "200"]),
#         "What comes next: 278, 179, ?, -19, -118 ?": ("80", ["0", "80", "-7", "66"]),
#         "What comes next: 2754, ?, 306, 102, 34 ?": ("918", ["918", "1345", "1266", "1456"]),
#         "What comes next: 288 594 ? 738 ?": ("588", ["677", "413", "588", "698"]),
#         "What comes next: 83, ?, 332, 664 ?": ("166", ["166", "178", "266", "567"]),
#         "What comes next: 92, ?, 5888, 47 104 ?": ("736", ["109", "167", "677", "736"]),
#         "What comes next: 78, 184, ?, 396, 502 ?": ("290", ["290", "1345", "1266", "1456"]),
#         "Which fraction is the biggest?": ("5/8", ["3/5", "5/8", "1/2", "4/7"]),
#         "The store reduces the price of one product by 20 percent. How many percent do you need to raise to the percentage to get the original price?": ("25", ["25", "27", "30", "35"]),
#         "There are 5 machines that make 5 parts in 5 minutes. How long does it take to make 100 parts on 100 machines?": ("5", ["5", "10", "15", "30"]),
#         "There is a lake on the surface of which water lilies float. The number of lilies doubles daily. If it takes 48 days to completely occupy the entire area of the lake, how many days will it take to occupy the floor of the lake?": ("47", ["47", "46", "96", "108"]),
#         "A car travels at a speed of 40 mph over a certain distance and then returns over the same distance at a speed of 60 mph. What is the average speed for the total journey?": ("48 mph", ["30 mph", "40 mph", "60 mph", "48 mph"]),
#         "SUNDAY MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY Which day is three days before the day immediately following the day two days before the day three days after the day immediately before Friday?": ("Wednesday", ["Tuesday", "Wednesday", "Thursday", "Sunday"]),
#         "What is always associated with DOLMEN?": ("stone", ["cloths", "statue", "tribe", "stone"]),
#         "What is the name given to a group of HORSES?": ("harras", ["husk", "harras", "mute", "rush"]),
#         "You have accidentally left the plug out of the bath and are attempting to fill the bath with both taps full on. The hot tap takes three minutes to fill the bath and the cold tap two minutes, and the water empties through the plughole in six minutes. In how many minutes will the bath be filled?": ("1.5", ["1", "3", "1.5", "5"]),
#         "Which word in brackets is opposite in meaning to the word in capitals? FREQUENT": ("avoid", ["glow", "restrain", "avoid", "discard"]),
#         "What is the name given to a group of FINCHES?": ("a charm", ["a charm", "a cluster", "a nest", "a place"]),
#         "What is a GOOGOL?": ("a mathematical term", ["a folk dance", "a carrion crow", "an albatross", "a mathematical term"]),
#         "Which is the odd one out? CLAVICHORD, HARPSICHORD, CLARION, ACCORDION": ("clarion", ["clavichord", "harpsichord", "clarion", "accordion"]),
#         "LATTICE : WINDOW Which two words below have the same relationship as the two words above?": ("mansard: roof", ["portal: gable", "mansard: roof", "parapet: door", "fascia: floor"]),
#         "Which word in brackets means the same as the word in capitals? INDISCRETION": ("folly", ["folly", "sloth", "aversion", "vacillation"]),
#         "Which is the odd one out?": ("EVACUATION", ["SALIFEROUS", "EVACUATION", "EXHAUSTION", "INOCULATED"]),
#         "What is an ORRERY?": ("a clockwork model", ["a museum", "a dungeon", "a clockwork model", "a golden ornament"]),
#         "Which one of these is not an animal?": ("dihras", ["macyan", "lawsee", "rougac", "dihras"]),
#         "MUSIC: COMPOSE DEVICE: ?": ("invent", ["use", "create", "construct", "invent"]),
#         "Which one of these is not a vegetable?": ("xestte", ["rocart", "xestte", "romraw", "eyeclr"]),
#         "What is the name given to a group of BUTLERS?": ("draught", ["blast", "host", "draught", "staff"]),
#         "What is a CURRICLE?": ("a vehicle", ["a vehicle", "a boat", "a curtain", "a vegetable"]),
#         "Which word means the same as NEGATORY?": ("trifling", ["fallacious", "prodigious", "trifling", "restraining"]),
#         "What is always associated with FAIENCE?": ("pottery", ["pottery", "fairies", "zinc", "ghosts"]),
#         "Which of the following is not an anagram of an animal?": ("MOMS HOUR", ["BRISK PONG", "PUNCH KIM", "RED OPAL", "MOMS HOUR"]),
#         "Which word in brackets means the same as the word in capitals? PROGENY": ("lineage", ["skill", "lineage", "movement", "vocation"]),
#         "PERIGEE : APOGEE PERIHELION: ?": ("aphelion", ["aphelion", "eliptic", "orrery", "nadir"]),
#         "What is a FERRULE?": ("a metal band", ["a metal band", "a circus wheel", "a window", "a funeral"]),
#         "What is the name given to a group of KITTENS?": ("kindle", ["clutch", "labour", "kindle", "swarm"]),
#         "What is always associated with GENOA?": ("a sail", ["a bustle", "haberdashery", "a sail", "an eyeglass"]),
#         "Which one of these is not a flower?": ("TRYLUS", ["ALEZAA", "SUCROC", "TEVOIL", "TRYLUS"]),
#         "Which of the following is not an anagram of ‘intelligence test'?": ("LET TESTING CLIENT", ["TESTING ELECT LINE", "TESTING CLIENTELE", "TIES GENTLE CLIENT", "LET TESTING CLIENT"]),
#         "Which word in brackets is opposite in meaning to the word in capitals? GRUESOME": ("appealing", ["enjoyable", "appealing", "wholesome", "young"]),
#         "SUNDAY, MONDAY, WEDNESDAY, SATURDAY, WEDNESDAY Which day comes next?": ("MONDAY", ["SUNDAY", "MONDAY", "WEDNESDAY", "SATURDAY"]),
#         "Which word means the same as ESOTERIC?": ("secret", ["pristine", "misshapen", "gibbous", "secret"]),
#         "What is a GIGOT?": ("a leg of mutton", ["a dancer", "a leg of mutton", "a rogue", "a measure"]),
#         "What is the name given to a group of LARKS?": ("exaltation", ["exaltation", "badelynge", "flock", "pitying"]),
#         "Which one of these is not a musical instrument?": ("MATBAN", ["NILOIV", "MATBAN", "THIZRE", "LAMYCB"]),
#         "Only one set of letters below can be arranged into a five-letter word. Can you find the word?": ("EMRUD", ["KIRCE", "ONTDI", "EMRUD", "ENCID"]),
#         "Which word in brackets is opposite in meaning to the word in capitals? SURREPTITIOUS": ("overt", ["servile", "trusty", "scarce", "overt"]),
#         "Which is the odd one out?": ("MOGUL", ["MOGUL", "SHANG", "TANG", "MING"]),
#         "GENEALOGY : ANCESTRY ETYMOLOGY : ?": ("words", ["knowledge", "fossils", "inscriptions", "words"]),
#         "What is STOCCADO?": ("a fencing stroke", ["a stockade", "fast talking", "a fencing stroke", "illness"]),
#         "What is the name given to a group of PEACOCKS?": ("ostentation", ["bevy", "ostentation", "lepe", "richesse"]),
#         "What is always associated with INCARNADINE?": ("flesh coloured", ["imprisonment", "body language", "flesh coloured", "quarries"]),
#         "Which one of these is not a weather term?": ("SUMPOS", ["YLILHC", "YTOSMR", "SUMPOS", "WEROHS"]),
#         "Which word in brackets means the same as the word in capitals. METAPHYSICAL": ("esoteric", ["transient", "esoteric", "symbolic", "fastidious"]),
#         "Only one set of letters below can be arranged into a five-letter word. Can you find the word?": ("EMRUD", ["KIRCE", "ENCID", "ONTDI", "EMRUD"]),
#         "Which word means the same as ESPALIER?": ("wooden trellis", ["wooden trellis", "spectre", "advocate", "ligament"]),
#         "Which word in brackets is most opposite in meaning to the word in capitals? EXPEDITE": ("curb", ["dispatch", "dismiss", "curb", "conclude"]),
#         "How many minutes is it before noon if 29 minutes ago it was six times as many minutes past 10 am?": ("13 minutes", ["13 minutes", "15 minutes", "10 minutes", "16 minutes"]),
#         "Which is the odd one out?": ("interpret", ["dilate", "elaborate", "expatiate", "interpret"])
#     }

#     selected_questions = random.sample(list(questions.items()), 20)

#     for question, (correct_answer, options) in selected_questions:
#         user_answer = st.radio(question, options, key=question)
#         if user_answer == correct_answer:
#             score += 1

#     if st.button("Submit IQ Test"):
#         normalized_score = score * 10 
#         st.session_state["iq_score"] = normalized_score
#         st.success(f"Your estimated IQ score is: {normalized_score}")
        
#     return st.session_state.get("iq_score", None)





# import streamlit as st
# import random

# def iq_test():
#     st.subheader("🧠 IQ Test")

#     # Dictionary of questions
#     questions = {
#         "What comes next: 2, 4, 8, 16?": ("32", ["20", "24", "32", "64"]),
#         "If CAT is to DOG, BLACK is to?": ("WHITE", ["BLUE", "WHITE", "BROWN", "DARK"]),
#         "What comes next: 7 9 5 11 4 15 12 7 13 8 11 ?": ("11", ["8", "10", "11", "13"]),
#         "What comes next: 2 5 7 4 7 5 3 6 ?": ("6", ["4", "6", "8", "10"]),
#         "What comes next: 2, 5, 8, 11, ?": ("14", ["8", "12", "14", "16"]),
#         "What comes next: 121, 144, 169, 196, ?": ("225", ["225", "230", "275", "221"]),
#         "What comes next: 4, 6, 9, 6, 14, 6, ?": ("19", ["14", "9", "16", "19"]),
#         "What comes next: 2, 3, 5, 9, 17, 33, 65, ?": ("129", ["104", "129", "97", "135"]),
#         "What comes next: 1, 3, 12, 52, 265, ?": ("1596", ["1188", "1390", "1489", "1596"]),
#         "What comes next: 2, 8, 26, 62, 122, 212, ?": ("338", ["338", "339", "340", "341"]),
#         "What comes next: 13, 17, 19, 23, 29, ?": ("31", ["30", "31", "33", "34"]),
#         "What comes next: 2, 3, 6, 11, 18, 27, ?": ("38", ["21", "28", "38", "41"]),
#         "What comes next: 2, 2, 4, 12, 48, 240, ?": ("1440", ["347", "567", "1009", "1440"]),
#         "What comes next: 3 2 2 5 5 5 7 8 8 9 11 11 ?": ("11", ["11", "12", "13", "15"]),
#         "What comes next: 1 3 2 6 3 11 4 18 5 ?": ("27", ["20", "25", "27", "29"]),
#         "What comes next: 13 17 23 29 31 37 ?": ("41", ["39", "41", "49", "55"]),
#         "What comes next: 17 16 14 12 11 8 8 ?": ("4", ["None of the above", "11", "3", "4"]),
#         "What comes next: 9 11 13 ?": ("None of the above", ["None of the above", "14", "16", "17"]),
#         "What comes next: 5, 6, 9, 14, 21, ?": ("30", ["None of the above", "30", "31", "36"]),
#         "What comes next: 40, 30, 22, 16, ?": ("12", ["12", "10", "14", "30"])
#     }

#     # Randomly select 20 questions
#     selected_questions = dict(random.sample(list(questions.items()), 20))

#     score = 0
#     for question, (correct_answer, options) in selected_questions.items():
#         user_answer = st.radio(question, options, key=question)
#         if user_answer == correct_answer:
#             score += 1

#     if st.button("Submit IQ Test"):
#         # Normalize score: adding 90 ensures a base IQ of 90 and scaling the additional points
#         normalized_score = score * 10 + 90
#         st.session_state["iq_score"] = normalized_score
#         st.success(f"Your estimated IQ score is: {normalized_score}")

#     return st.session_state.get("iq_score", None)

# def main():
#     st.title("Online IQ Test")
#     iq_test()

# if __name__ == "__main__":
#     main()




# import streamlit as st
# import random

# def iq_test():
#     st.subheader("🧠 IQ Test")

#     # Dictionary of questions
#     questions = {
#         "What comes next: 2, 4, 8, 16?": ("32", ["20", "24", "32", "64"]),
#         "If CAT is to DOG, BLACK is to?": ("WHITE", ["BLUE", "WHITE", "BROWN", "DARK"]),
#         "What comes next: 7 9 5 11 4 15 12 7 13 8 11 ?": ("11", ["8", "10", "11", "13"]),
#         "What comes next: 2 5 7 4 7 5 3 6 ?": ("6", ["4", "6", "8", "10"]),
#         "What comes next: 2, 5, 8, 11, ?": ("14", ["8", "12", "14", "16"]),
#         "What comes next: 121, 144, 169, 196, ?": ("225", ["225", "230", "275", "221"]),
#         "What comes next: 4, 6, 9, 6, 14, 6, ?": ("19", ["14", "9", "16", "19"]),
#         "What comes next: 2, 3, 5, 9, 17, 33, 65, ?": ("129", ["104", "129", "97", "135"]),
#         "What comes next: 1, 3, 12, 52, 265, ?": ("1596", ["1188", "1390", "1489", "1596"]),
#         "What comes next: 2, 8, 26, 62, 122, 212, ?": ("338", ["338", "339", "340", "341"]),
#         "What comes next: 13, 17, 19, 23, 29, ?": ("31", ["30", "31", "33", "34"]),
#         "What comes next: 2, 3, 6, 11, 18, 27, ?": ("38", ["21", "28", "38", "41"]),
#         "What comes next: 2, 2, 4, 12, 48, 240, ?": ("1440", ["347", "567", "1009", "1440"]),
#         "What comes next: 3 2 2 5 5 5 7 8 8 9 11 11 ?": ("11", ["11", "12", "13", "15"]),
#         "What comes next: 1 3 2 6 3 11 4 18 5 ?": ("27", ["20", "25", "27", "29"]),
#         "What comes next: 13 17 23 29 31 37 ?": ("41", ["39", "41", "49", "55"]),
#         "What comes next: 17 16 14 12 11 8 8 ?": ("4", ["None of the above", "11", "3", "4"]),
#         "What comes next: 9 11 13 ?": ("None of the above", ["None of the above", "14", "16", "17"]),
#         "What comes next: 5, 6, 9, 14, 21, ?": ("30", ["None of the above", "30", "31", "36"]),
#         "What comes next: 40, 30, 22, 16, ?": ("12", ["12", "10", "14", "30"])
#     }

#     # Randomly select 20 questions
#     selected_questions = dict(random.sample(list(questions.items()), 20))

#     score = 0
#     for question, (correct_answer, options) in selected_questions.items():
#         user_answer = st.radio(question, options, key=question)
#         if user_answer == correct_answer:
#             score += 1

#     if st.button("Submit IQ Test"):
#         # Normalize score: adding 90 ensures a base IQ of 90 and scaling the additional points
#         normalized_score = score * 10 + 90
#         st.session_state["iq_score"] = normalized_score
#         st.success(f"Your estimated IQ score is: {normalized_score}")

#     return st.session_state.get("iq_score", None)

# def main():
#     st.title("Online IQ Test")
#     iq_test()

# if __name__ == "__main__":
#     main()