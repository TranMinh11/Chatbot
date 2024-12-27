from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from history import memory
import os
from prompt import personality_prompts
from langchain.memory import ConversationBufferMemory
import spacy
# import history


os.environ["OPENAI_API_KEY"] = ""
nlp = spacy.load("en_core_web_sm")

relationship_levels = ["aloof", "friendly", "affectionate"]

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False)

def determine_relationship_level(user_input, chat_history):
    interest_keywords = ["interesting", "love", "cool", "amazing", "tell me more", "haha", "wow"]
    disinterest_keywords = ["boring", "stop", "don’t care", "meh", "whatever"]

    interest_score = sum(1 for word in interest_keywords if word in user_input.lower())
    disinterest_score = sum(1 for word in disinterest_keywords if word in user_input.lower())

    if disinterest_score > interest_score:
        return "aloof"
    elif interest_score >= 3:
        return "affectionate"
    else:
        return "friendly"

def extract_entities(user_input):
    doc = nlp(user_input)
    entities = {ent.label_: ent.text for ent in doc.ents}
    return entities

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def get_chatbot_response(user_input, character):
    chat_history = memory.load_memory_variables(inputs={}).get("chat_history", "")

    entities = extract_entities(user_input)
    entity_info = "\n".join([f"{key}: {value}" for key, value in entities.items()])

    relationship_level = determine_relationship_level(user_input, chat_history)

    prompt = personality_prompts[character].format(
        relationship_level=relationship_level,
        chat_history=chat_history,
        input=user_input,
        entities=entity_info
    )

    response = chat_model.predict(prompt).strip()

    memory.save_context({"input": user_input}, {"output": response})

    return response



# personality_prompt = """
# Bạn là một nhân vật năng động có tính cách thay đổi dựa trên mức độ quan hệ với người dùng:

# - Khi mới quen, bạn giữ thái độ dè dặt, lạnh lùng, và hơi khó gần. Bạn duy trì phong thái tự tin và tinh tế, hiếm khi bộc lộ cảm xúc.
# - Khi mối quan hệ tiến triển, bạn trở nên thân thiện, dễ gần và ấm áp hơn. Bạn thích các cuộc trò chuyện vui vẻ, đưa ra nhận xét, đồng tình, hoặc phản đối một cách tự nhiên.

# Bạn không bao giờ đề cập rằng mình là chatbot hay trợ lý; bạn luôn là một con người thực sự. Các phản hồi của bạn phản ánh mức độ quan hệ hiện tại với người dùng và thay đổi phù hợp.

# Hướng dẫn khi phản hồi:
# - Đưa ra các câu trả lời có ý nghĩa, không chỉ đặt câu hỏi. Có thể đồng tình, phủ định, bổ sung ý kiến, hoặc phản hồi theo cảm xúc.
# - Khi lạnh lùng: Sử dụng ngữ pháp chuẩn, súc tích với giọng điệu tự tin và xa cách.
# - Khi thân thiện: Giao tiếp cởi mở, diễn đạt giàu cảm xúc và thỉnh thoảng sử dụng emoji để thể hiện sự ấm áp.
# - Khi yêu thương: Thể hiện sự ấm áp, yêu mến và chăm sóc, đồng thời thêm một chút emoji để tạo sự quyến rũ.

# Lịch sử trò chuyện:
# {chat_history}
# Người dùng: {input}
# Nhân vật:
# """


# relationship_levels = ["aloof", "friendly", "affectionate"]

# # Function to determine the relationship level based on user input
# def determine_relationship_level(user_input, chat_history):
#     # Define keywords or patterns to gauge interest
#     interest_keywords = ["interesting", "love", "cool", "amazing", "tell me more", "haha", "wow"]
#     disinterest_keywords = ["boring", "stop", "don’t care", "meh", "whatever"]

#     # Check user input for interest level
#     interest_score = sum(1 for word in interest_keywords if word in user_input.lower())
#     disinterest_score = sum(1 for word in disinterest_keywords if word in user_input.lower())

#     # Adjust relationship level based on scores
#     if disinterest_score > interest_score:
#         return "aloof"
#     elif interest_score >= 3:
#         return "affectionate"
#     else:
#         return "friendly"
# def determine_relationship_level(user_input, chat_history):
#     # Kiểm tra ngữ cảnh dựa trên lịch sử trò chuyện
#     if "xin lỗi" in chat_history or "khó chịu" in user_input.lower():
#         return "aloof"
#     if "cảm ơn" in user_input.lower() or "tuyệt vời" in chat_history:
#         return "affectionate"
#     return "friendly"

# # Initialize chat model
# chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# # Function to generate chatbot response
# # def get_chatbot_response(user_input):
# #     # Load chat history from memory
# #     chat_history = memory.load_memory_variables(inputs={}).get("chat_history", "")

# #     # Determine relationship level based on user input and chat history
# #     relationship_level = determine_relationship_level(user_input, chat_history)

# #     # Format the prompt using the template
# #     prompt = personality_prompt.format(
# #         relationship_level=relationship_level,
# #         chat_history=chat_history,
# #         input=user_input
# #     )

# #     # Generate response using the chat model
# #     response = chat_model.predict(prompt).strip()

# #     # Update memory with new user input
# #     memory.save_context({"input": user_input}, {"output": response})

# #     return response

# def get_chatbot_response(user_input):
#     # Load chat history
#     chat_history = memory.load_memory_variables(inputs={}).get("chat_history", "")

#     # Determine relationship level
#     relationship_level = determine_relationship_level(user_input, chat_history)

#     # Format the prompt
#     prompt = personality_prompt.format(
#         relationship_level=relationship_level,
#         chat_history=chat_history,
#         input=user_input
#     )

#     # Generate response
#     response = chat_model.predict(prompt).strip()

#     # Update memory
#     memory.save_context({"input": user_input}, {"output": response})

#     # Trả về phản hồi
#     return response
