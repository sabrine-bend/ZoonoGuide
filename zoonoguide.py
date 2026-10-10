
import os

import streamlit as st

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage



# Load API key from the env file in the project folder

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / "env", override=True)



# -------------------- PAGE CONFIG --------------------



st.set_page_config(

    page_title="ZoonoGuide AI",

    page_icon="🔬",

    layout="wide"

)



# -------------------- BLUE UI --------------------



st.markdown("""

<style>

.stApp {

    background: #F4F8FF;

}

[data-testid="stHeader"] {

    background: rgba(244, 248, 255, 0.95);

}

.main .block-container {

    max-width: 1000px;

    padding-top: 2rem;

    padding-bottom: 3rem;

}

h1, h2, h3 {

    color: #174A8B;

}

p, li, label {

    color: #263B56;

}

.guide-card {

    background: white;

    border: 1px solid #D7E6FA;

    border-radius: 16px;

    padding: 24px;

    margin: 12px 0 22px 0;

}

.definition {

    color: #263B56;

    font-size: 16px;

    line-height: 1.8;

}

.source-link {

    color: #1769AA;

    font-weight: 600;

}

div.stButton > button {

    background: #E7F0FF;

    color: #174A8B;

    border: 1px solid #B9D2F5;

    border-radius: 12px;

    min-height: 48px;

    text-align: left;

    white-space: normal;

}

div.stButton > button:hover {

    background: #D4E6FF;

    border-color: #5593DC;

    color: #103B70;

}

div.stButton > button[kind="primary"] {

    background: #1769AA;

    color: white;

    border: none;

}

[data-testid="stChatMessage"] {

    background: white;

    border: 1px solid #DDE8F7;

    border-radius: 12px;

}

.small-note {

    color: #64748B;

    font-size: 13px;

}

</style>

""", unsafe_allow_html=True)



# -------------------- DISEASE INFORMATION --------------------

# Prepared in advance. No AI API call is needed to display definitions.



DISEASES = {

    "Toxoplasmosis": {

        "name_en": "Toxoplasmosis",

        "name_fr": "Toxoplasmose",

        "definition_en": """

Toxoplasmosis is an infectious disease caused by a microscopic parasite

called *Toxoplasma gondii*. The parasite can infect humans and many

warm-blooded animals, including cats, which play an important role in

its life cycle.



People may become infected by accidentally swallowing the parasite

through contaminated soil, water, food, or undercooked meat. Infection

can also occur during pregnancy when the parasite passes from an

infected pregnant person to the developing baby. Most healthy people

have no symptoms or experience only mild, flu-like illness. However,

infection can be more serious for unborn babies and people with

weakened immune systems.

""",

        "definition_fr": """

La toxoplasmose est une maladie infectieuse causée par un parasite

microscopique appelé *Toxoplasma gondii*. Ce parasite peut infecter

l’être humain et de nombreux animaux à sang chaud. Les chats jouent

un rôle important dans son cycle de vie.



L’être humain peut être infecté en avalant accidentellement le parasite

présent dans la terre, l’eau ou les aliments contaminés, ou dans de la

viande insuffisamment cuite. Une transmission de la mère au bébé est

également possible pendant la grossesse. Chez les personnes en bonne

santé, l’infection ne provoque souvent aucun symptôme ou entraîne

des symptômes légers ressemblant à ceux de la grippe. Elle peut

cependant être grave pour le fœtus et les personnes immunodéprimées.

""",

        "source_name": "CDC",

        "source_url": "https://www.cdc.gov/toxoplasmosis/",

        "questions_en": [

            "How can people get toxoplasmosis from the environment or food?",

            "What role do cats play in the transmission of toxoplasmosis?",

            "Why can toxoplasmosis be dangerous during pregnancy?",

            "How can people reduce their risk of infection?"

        ],

        "questions_fr": [

            "Comment peut-on contracter la toxoplasmose par l’environnement ou les aliments ?",

            "Quel rôle les chats jouent-ils dans la transmission de la toxoplasmose ?",

            "Pourquoi la toxoplasmose peut-elle être dangereuse pendant la grossesse ?",

            "Comment réduire le risque d’infection ?"

        ]

    },



    "Brucellosis": {

        "name_en": "Brucellosis",

        "name_fr": "Brucellose",

        "definition_en": """

Brucellosis is a bacterial infection caused by bacteria of the genus

*Brucella*. It is an important zoonotic disease because it can spread

from infected animals to humans. Cattle, goats, sheep, pigs, and some

other animals may carry different Brucella species.



People are commonly infected by consuming unpasteurized milk or dairy

products from infected animals. Infection can also occur through direct

contact with infected animals, their blood, tissues, or birth products,

especially in farming, veterinary, and slaughterhouse settings.

Symptoms may include fever, sweating, tiredness, headaches, and muscle

or joint pain. The illness can persist or return if not properly managed.

""",

        "definition_fr": """

La brucellose est une infection bactérienne causée par des bactéries

du genre *Brucella*. C’est une zoonose importante, car elle peut se

transmettre des animaux infectés à l’être humain. Les bovins, les

chèvres, les moutons, les porcs et certains autres animaux peuvent

héberger différentes espèces de Brucella.



La contamination humaine survient souvent après la consommation

de lait cru ou de produits laitiers non pasteurisés provenant d’animaux

infectés. Elle peut également se produire par contact direct avec des

animaux infectés, leur sang, leurs tissus ou les produits de mise bas,

notamment dans les milieux agricoles, vétérinaires et les abattoirs.

Les symptômes peuvent comprendre de la fièvre, des sueurs, de la

fatigue, des maux de tête et des douleurs musculaires ou articulaires.

La maladie peut persister ou réapparaître.

""",

        "source_name": "WHO / OMS",

        "source_url": "https://www.who.int/news-room/fact-sheets/detail/brucellosis",

        "questions_en": [

            "How does brucellosis spread from livestock to humans?",

            "Why is unpasteurized milk a risk factor?",

            "What symptoms can brucellosis cause in humans?",

            "How can farmers and animal handlers reduce exposure?"

        ],

        "questions_fr": [

            "Comment la brucellose se transmet-elle du bétail à l’être humain ?",

            "Pourquoi le lait non pasteurisé représente-t-il un risque ?",

            "Quels symptômes la brucellose peut-elle provoquer chez l’être humain ?",

            "Comment les éleveurs et les personnes en contact avec les animaux peuvent-ils réduire les risques ?"

        ]

    },



    "Salmonellosis": {

        "name_en": "Salmonellosis",

        "name_fr": "Salmonellose",

        "definition_en": """

Salmonellosis is an infection caused by bacteria belonging to the

genus *Salmonella*. These bacteria can be found in the intestines of

humans and many animals, including poultry, reptiles, and livestock.

The infection is often associated with contaminated food, especially

undercooked eggs, poultry, meat, and other foods that have been

handled or stored unsafely.



People can also become infected through contact with infected animals

or environments contaminated with their feces. Common symptoms

include diarrhea, abdominal cramps, fever, and nausea. Many people

recover without specific treatment, but dehydration and more serious

illness can occur, particularly in young children, older adults, and

people with weakened immune systems.

""",

        "definition_fr": """

La salmonellose est une infection causée par des bactéries du genre

*Salmonella*. Ces bactéries peuvent être présentes dans l’intestin

des humains et de nombreux animaux, notamment les volailles, les

reptiles et les animaux d’élevage. L’infection est souvent liée à des

aliments contaminés, en particulier les œufs, la volaille et la viande

insuffisamment cuits, ou à des aliments mal manipulés ou conservés.



La contamination peut aussi se produire par contact avec des animaux

infectés ou avec un environnement contaminé par leurs matières

fécales. Les symptômes courants comprennent la diarrhée, les

crampes abdominales, la fièvre et les nausées. De nombreuses

personnes guérissent sans traitement spécifique, mais une

déshydratation ou une maladie plus grave est possible, notamment

chez les jeunes enfants, les personnes âgées et les personnes

immunodéprimées.

""",

        "source_name": "CDC",

        "source_url": "https://www.cdc.gov/salmonella/",

        "questions_en": [

            "Which animals can carry Salmonella?",

            "How can Salmonella spread through food and animal contact?",

            "What symptoms are commonly associated with salmonellosis?",

            "What food-handling and hygiene practices help prevent infection?"

        ],

        "questions_fr": [

            "Quels animaux peuvent porter des bactéries Salmonella ?",

            "Comment Salmonella se transmet-elle par les aliments et le contact animal ?",

            "Quels sont les symptômes fréquents de la salmonellose ?",

            "Quelles pratiques d’hygiène et de manipulation des aliments aident à prévenir l’infection ?"

        ]

    },



    "Ringworm": {

        "name_en": "Ringworm (Dermatophytosis)",

        "name_fr": "Teigne (Dermatophytose)",

        "definition_en": """

Ringworm, also called dermatophytosis, is a contagious fungal infection

that affects the skin and sometimes the scalp or nails. Despite its

name, it is not caused by a worm. The fungi responsible, known as

dermatophytes, use keratin found in the skin, hair, and nails.



Some dermatophytes can spread between animals and humans. Cats and

dogs are possible sources of infection, although other animals and

contaminated objects or surfaces may also play a role. Infection can

spread through direct contact with an infected person or animal, or

through contaminated items such as grooming tools, bedding, and

clothing. It often causes an itchy, scaly rash that may form a ring-like

shape, although its appearance can vary.

""",

        "definition_fr": """

La teigne, également appelée dermatophytose, est une infection

fongique contagieuse qui touche la peau et parfois le cuir chevelu

ou les ongles. Malgré son nom, elle n’est pas causée par un ver.

Les champignons responsables, appelés dermatophytes, utilisent

la kératine présente dans la peau, les cheveux et les ongles.



Certains dermatophytes peuvent se transmettre entre les animaux

et les humains. Les chats et les chiens peuvent être des sources

d’infection, mais d’autres animaux ainsi que des objets ou surfaces

contaminés peuvent également intervenir. La transmission peut se

produire par contact direct avec une personne ou un animal infecté,

ou par des objets contaminés comme les brosses, la literie et les

vêtements. La teigne provoque souvent une éruption cutanée

squameuse et prurigineuse, parfois en forme d’anneau.

""",

        "source_name": "WHO / OMS",

        "source_url": "https://www.who.int/news-room/fact-sheets/detail/ringworm-%28tinea%29",

        "questions_en": [

            "Can cats and dogs transmit ringworm to humans?",

            "What does ringworm usually look like in humans?",

            "Can ringworm spread through grooming tools or bedding?",

            "How can people reduce the risk of spreading ringworm?"

        ],

        "questions_fr": [

            "Les chats et les chiens peuvent-ils transmettre la teigne à l’être humain ?",

            "À quoi ressemble généralement la teigne chez l’être humain ?",

            "La teigne peut-elle se transmettre par les brosses ou la literie ?",

            "Comment réduire le risque de transmission de la teigne ?"

        ]

    }

}



# -------------------- SESSION STATE --------------------



defaults = {

    "explored_disease": None,

    "explored_language": None,

    "chat_history": [],

    "pending_question": None,

    "suggested_questions": [],

    "suggestion_key": None,

    "notice": None

}



for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value



# -------------------- LANGUAGE & DISEASE --------------------



st.title("🔬 ZoonoGuide AI")

st.markdown(

    "Learn about zoonotic diseases and explore reliable information "

    "with an AI-powered educational guide."

)

st.caption("Educational information only • Not a diagnostic tool")



col1, col2 = st.columns(2)



with col1:

    language = st.selectbox(

        "Choose your language / Choisissez votre langue",

        ["English", "Français"]

    )



with col2:

    disease_key = st.selectbox(

        "Choose a zoonotic disease / Choisissez une zoonose",

        list(DISEASES.keys()),

        format_func=lambda key: (

            DISEASES[key]["name_en"]

            if language == "English"

            else DISEASES[key]["name_fr"]

        )

    )



if language == "English":

    explore_label = "Explore disease"

    title_label = "About this disease"

    source_label = "Official source"

    chat_title = "Ask ZoonoGuide AI"

    chat_intro = (

        "Choose a suggested question or type your own question "

        "about the selected disease."

    )

    suggestions_title = "Questions you could ask"

    input_placeholder = "Ask a question about this disease..."

    clear_label = "Clear conversation"

    footer_note = (

        "ZoonoGuide AI provides general educational information. "

        "It does not diagnose diseases or replace a qualified professional."

    )

else:

    explore_label = "Découvrir la maladie"

    title_label = "À propos de cette maladie"

    source_label = "Source officielle"

    chat_title = "Posez vos questions à ZoonoGuide AI"

    chat_intro = (

        "Choisissez une question proposée ou écrivez votre propre "

        "question sur la maladie sélectionnée."

    )

    suggestions_title = "Questions que vous pouvez poser"

    input_placeholder = "Posez une question sur cette maladie..."

    clear_label = "Effacer la conversation"

    footer_note = (

        "ZoonoGuide AI fournit des informations générales à visée "

        "éducative. Il ne pose pas de diagnostic et ne remplace pas "

        "un professionnel qualifié."

    )



# -------------------- GROQ MODEL --------------------



@st.cache_resource

def load_model():

    # Read the API key from the env file, not Streamlit secrets.

    api_key = os.getenv("GROQ_API_KEY")



    if not api_key:

        return None



    return ChatGroq(

        model="openai/gpt-oss-120b",

        api_key=api_key,

        temperature=0.2,

        max_tokens=800

    )



# -------------------- AI HELPERS --------------------



def get_suggested_questions(disease_name, definition, lang):

    """Ask the AI to suggest disease-specific questions."""



    model = load_model()



    if model is None:

        return None



    if lang == "English":

        prompt = f"""

You are the educational question-planning assistant for ZoonoGuide AI.



Selected disease: {disease_name}



Disease overview:

{definition}



Generate exactly 5 short, useful questions that a learner could ask

to understand THIS disease better.



Requirements:

- Questions must be specific to the selected disease.

- Cover a useful mix of transmission, signs in humans, prevention,

  animal carriers, and risk factors where relevant.

- Do not answer the questions.

- Do not give medical advice or ask the user to provide personal

  health information.

- Return only the 5 questions, one per line, without numbering,

  bullets, headings, or extra commentary.

"""

    else:

        prompt = f"""

Tu es l'assistant qui propose des questions éducatives pour

ZoonoGuide AI.



Maladie sélectionnée : {disease_name}



Présentation de la maladie :

{definition}



Propose exactement 5 questions courtes et utiles pour mieux

comprendre CETTE maladie.



Consignes :

- Les questions doivent être spécifiques à la maladie sélectionnée.

- Couvre différents sujets pertinents : transmission, signes chez

  l'humain, prévention, animaux porteurs et facteurs de risque.

- Ne réponds pas aux questions.

- Ne donne pas de conseils médicaux personnalisés.

- Retourne uniquement les 5 questions, une par ligne, sans numéros,

  puces, titres ni commentaires supplémentaires.

"""



    try:

        response = model.invoke([HumanMessage(content=prompt)])

        content = response.content



        if not isinstance(content, str):

            content = str(content)



        questions = [

            line.strip().lstrip("•-0123456789. ").strip()

            for line in content.splitlines()

            if line.strip()

        ]

        questions = [q for q in questions if len(q) > 10]

        return questions[:5] if questions else None



    except Exception as error:

        print(f"Groq suggestion error: {error}")

        return None





def answer_question(disease_name, definition, question, lang, history):

    """Answer the user's question using the selected disease context."""



    model = load_model()



    if model is None:

        return (

            "The Groq API key was not found. Please check your env file."

            if lang == "English"

            else

            "La clé API Groq est introuvable. Vérifiez votre fichier env."

        )



    if lang == "English":

        system_prompt = f"""

You are ZoonoGuide AI, an educational assistant about zoonotic diseases.



Selected disease: {disease_name}



Prepared disease overview:

{definition}



Rules:

1. Answer in English.

2. Answer the user's actual question clearly, with enough detail to

   be useful but without unnecessary length.

3. Keep the answer specific to the selected disease.

4. Use the prepared overview as context, but you may explain relevant

   established scientific information.

5. Do not invent statistics, scientific claims, or references.

6. Do not diagnose a person or animal, prescribe medicines, or

   provide individualized treatment instructions.

7. For urgent or personal health concerns, advise contacting a

   qualified healthcare professional. For animal-health concerns,

   advise contacting a veterinarian.

8. If a question is unrelated to zoonotic diseases, politely guide

   the user back to educational questions about the selected disease.

9. Do not create a separate section titled "When to seek professional

   help".

10. Never claim that the app replaces medical or veterinary care.

11. Be respectful, accessible, and educational.

"""

    else:

        system_prompt = f"""

Tu es ZoonoGuide AI, un assistant éducatif spécialisé dans les zoonoses.



Maladie sélectionnée : {disease_name}



Présentation de la maladie :

{definition}



Règles :

1. Réponds en français.

2. Réponds clairement à la question, avec suffisamment de détails

   utiles sans être inutilement long.

3. Reste centré sur la maladie sélectionnée.

4. Utilise la présentation fournie comme contexte et explique les

   connaissances scientifiques établies lorsque cela est pertinent.

5. N'invente ni statistiques, ni faits scientifiques, ni références.

6. Ne pose pas de diagnostic, ne prescris pas de médicaments et ne

   donne pas de traitement personnalisé.

7. Pour un problème de santé personnel ou urgent, recommande de

   contacter un professionnel de santé qualifié. Pour un animal,

   recommande de contacter un vétérinaire.

8. Si la question n'est pas liée aux zoonoses, invite poliment

   l'utilisateur à poser une question éducative sur la maladie choisie.

9. Ne crée pas de section intitulée « Quand consulter un professionnel ».

10. Ne prétends jamais remplacer un professionnel de santé ou un vétérinaire.

11. Adopte un ton accessible, respectueux et pédagogique.

"""



    messages = [SystemMessage(content=system_prompt)]



    for item in history[-8:]:

        if item["role"] == "user":

            messages.append(HumanMessage(content=item["content"]))

        elif item["role"] == "assistant":

            messages.append(AIMessage(content=item["content"]))



    messages.append(HumanMessage(content=question))



    try:

        response = model.invoke(messages)

        return response.content

    except Exception as error:

        print(f"Groq API error: {error}")

        return (

            "Sorry, I couldn't get an answer right now. Please try again."

            if lang == "English"

            else

            "Désolé, je n'ai pas pu obtenir de réponse. Veuillez réessayer."

        )



# -------------------- EXPLORE BUTTON --------------------



if st.button(explore_label, type="primary", use_container_width=True):

    st.session_state.explored_disease = disease_key

    st.session_state.explored_language = language

    st.session_state.chat_history = []

    st.session_state.pending_question = None

    st.session_state.notice = None



    disease = DISEASES[disease_key]

    definition = (

        disease["definition_en"]

        if language == "English"

        else disease["definition_fr"]

    )



    # Generate disease-specific questions once per selection.

    with st.spinner(

        "Preparing suggested questions..."

        if language == "English"

        else "Préparation des questions..."

    ):

        generated = get_suggested_questions(

            disease["name_en"] if language == "English"

            else disease["name_fr"],

            definition,

            language

        )



    # Use curated, disease-specific questions if the API is unavailable.

    if generated:

        st.session_state.suggested_questions = generated

    else:

        st.session_state.suggested_questions = (

            disease["questions_en"]

            if language == "English"

            else disease["questions_fr"]

        )



    st.session_state.suggestion_key = (disease_key, language)



# -------------------- DISPLAY SELECTED DISEASE --------------------



is_current_selection = (

    st.session_state.explored_disease == disease_key

    and st.session_state.explored_language == language

)



if is_current_selection:

    disease = DISEASES[disease_key]



    disease_name = (

        disease["name_en"]

        if language == "English"

        else disease["name_fr"]

    )



    definition = (

        disease["definition_en"]

        if language == "English"

        else disease["definition_fr"]

    )



    st.divider()



    st.subheader(f"📘 {title_label}: {disease_name}")



    st.markdown(

        f'<div class="guide-card"><div class="definition">'

        f'{definition.strip().replace(chr(10), "<br><br>")}'

        f'</div></div>',

        unsafe_allow_html=True

    )



    st.markdown(

        f'**{source_label}:** '

        f'[{disease["source_name"]}]({disease["source_url"]})'

    )



    st.divider()

    st.subheader(f"💬 {chat_title}")

    st.write(chat_intro)



    # -------------------- SUGGESTED QUESTIONS --------------------



    st.markdown(f"#### 💡 {suggestions_title}")



    questions = st.session_state.suggested_questions



    for i in range(0, len(questions), 2):

        cols = st.columns(2)



        for j, col in enumerate(cols):

            question_index = i + j



            if question_index >= len(questions):

                continue



            question = questions[question_index]



            with col:

                if st.button(

                    question,

                    key=f"suggest_{disease_key}_{language}_{question_index}",

                    use_container_width=True

                ):

                    st.session_state.pending_question = question



    # -------------------- CHAT HISTORY --------------------



    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])



    # -------------------- USER INPUT --------------------



    typed_question = st.chat_input(input_placeholder)



    question_to_answer = typed_question



    if st.session_state.pending_question:

        question_to_answer = st.session_state.pending_question

        st.session_state.pending_question = None



    if question_to_answer:

        st.session_state.chat_history.append({

            "role": "user",

            "content": question_to_answer

        })



        with st.chat_message("user"):

            st.markdown(question_to_answer)



        with st.chat_message("assistant"):

            with st.spinner(

                "Thinking..."

                if language == "English"

                else "Réflexion en cours..."

            ):

                answer = answer_question(

                    disease_name,

                    definition,

                    question_to_answer,

                    language,

                    st.session_state.chat_history[:-1]

                )



            st.markdown(answer)



        st.session_state.chat_history.append({

            "role": "assistant",

            "content": answer

        })



        st.rerun()



    if st.session_state.chat_history:

        if st.button(clear_label):

            st.session_state.chat_history = []

            st.rerun()



    st.caption(footer_note)



else:

    st.info(

        "Choose a disease and click 'Explore disease' to read its "

        "overview and discover suggested questions."

        if language == "English"

        else

        "Choisissez une maladie puis cliquez sur « Découvrir la maladie » "

        "pour lire sa présentation et découvrir des questions suggérées."

    )
