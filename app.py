import cohere
import streamlit as st
import os

# Initialize Cohere client
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

# Function to generate a startup idea
def generate_idea(industry, temperature):
    base_idea_prompt = """This program generates a startup idea given the industry.

--
Industry: Workplace
Startup Idea: A platform that generates slide deck contents automatically based on a given outline

--
Industry: Home Decor
Startup Idea: An app that calculates the best position of your indoor plants for your apartment

--
Industry: Healthcare
Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week

--
Industry: Education
Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals

--
Industry:"""

    response = co.generate(
        model="command",
        prompt=base_idea_prompt + " " + industry + "\nStartup Idea: ",
        max_tokens=30,
        temperature=temperature,
        stop_sequences=["\n\n--"]
    )
    startup_idea = response.generations[0].text.split('--')[0].strip()
    return startup_idea

# Function to generate a startup name
def generate_name(idea, temperature):
    base_name_prompt = """This program generates a startup name given the startup idea.

--
Startup Idea: A platform that generates slide deck contents automatically based on a given outline
Startup Name: Deckerize

--
Startup Idea: An app that calculates the best position of your indoor plants for your apartment
Startup Name: Planteasy

--
Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week
Startup Name: Hearspan

--
Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals
Startup Name: Prime Age

--
Startup Idea:"""

    response = co.generate(
        model="command",
        prompt=base_name_prompt + " " + idea + "\nStartup Name:",
        max_tokens=7,
        temperature=temperature,
        stop_sequences=["\n\n--"]
    )
    startup_name = response.generations[0].text.split('--')[0].strip()
    return startup_name

# Streamlit front-end
st.title("🚀 Startup Idea Generator")

form = st.form(key="user_settings")
with form:
    industry_input = st.text_input("Industry", key="industry_input")
    col1, col2 = st.columns(2)
    with col1:
        num_input = st.slider(
            "Number of ideas",
            value=3,
            key="num_input",
            min_value=1,
            max_value=10,
            help="Choose to generate between 1 to 10 ideas"
        )
    with col2:
        creativity_input = st.slider(
            "Creativity",
            value=0.5,
            key="creativity_input",
            min_value=0.1,
            max_value=0.9,
            help="Lower values generate more 'predictable' output, higher values generate more 'creative' output"
        )
    generate_button = form.form_submit_button("Generate Idea")

if generate_button:
    if industry_input == "":
        st.error("Industry field cannot be blank")
    else:
        my_bar = st.progress(0.05)
        st.subheader("Startup Ideas:")
        for i in range(num_input):
            st.markdown("---")
            startup_idea = generate_idea(industry_input, creativity_input)
            startup_name = generate_name(startup_idea, creativity_input)
            st.markdown("##### " + startup_name)
            st.write(startup_idea)
            my_bar.progress((i + 1) / num_input)

