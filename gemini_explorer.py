import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Initialize and set up the project. 初始化项目：使用特定的项目ID通过vertexai.init()初始化项目。
project = "sample-gemini-jamie-424201"
vertexai.init(project=project)

# Configure the model. 配置生成模型：使用指定的temperature值配置生成模型。
config = generative_models.GenerationConfig(
    temperature=0.4
)

# Create a generative model instance and start a chat session. 创建生成模型的实例，并启动聊天会话。
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat = model.start_chat()

# Define the llm_function. 定义llm_function：该函数负责将用户查询发送到聊天模型，并在Streamlit应用中显示响应。
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)  # Send the user's query to the chat session
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    # Initialize chat history. 初始化聊天历史：确保在用户交互之间维护聊天历史记录。
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Append the user query and model response to the session state.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

    # Display and load chat history. 显示并加载聊天历史记录。
    for index, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Initialize Streamlit App
st.title("Gemini Explorer")
if "messages" not in st.session_state:
    st.session_state.messages = []


# Step 1: Add Initial Message Logic to Streamlit App. 添加初始消息逻辑。
if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive."
    llm_function(chat, initial_prompt)    

# Capture User Query. 捕获用户查询。在捕获用户查询的同时，还捕获用户的名字，并将名字加入到查询中。这是一个不错的想法
query = st.text_input("Enter your query")
if query:
    # Capture user's name
    user_name = st.text_input("Enter your name")
    personalized_query = f"Hey {user_name}, {query}"  # Incorporate user's name into the query
    llm_function(chat, personalized_query, user_name)  # Pass the personalized query to the llm_function



