# crew.py
from crewai import Crew, Process
from tasks import programer_task
from agents import programer

## Forming the tech focused crew with some enhanced configuration
crew = Crew(
    agents=[programer],
    tasks=[programer_task],
    process=Process.sequential,
    verbose=True  # or verbose=False
)

## starting the task execution process wiht enhanced feedback

# نتيجة التشغيل ستكون في ملف index.html
