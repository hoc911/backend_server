from crewai import LLM, Agent
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import os

## call the gemini models
llm = LLM(
    model="gemini/gemini-2.0-flash-thinking-exp-1219",
    verbose=True,
    temperature=0.5,
    api_key=os.getenv("GEMINI_API_KEY"),
)

## creating a write agent with custom
programer = Agent(
    role='مبرمج خبير',
    goal='إنشاء صفحة ويب بناءً على وصف.',
    verbose=True,
    memory=True,
    backstory=(
        "مبرمج ماهر يقوم ببرمجة احترافية عند الطلب"
        "دقيق للغاية، يكتب الكود من خلال الوصف بكل احترافية"
    ),
    llm=llm,
    allow_delegation=False
)
