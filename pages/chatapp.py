import streamlit as st
import logging
from typing import List
from func_aoai import call_func_aoai

logging.basicConfig(level=logging.INFO)

USER_NAME = "user"
ASSISTANT_NAME = "assistant"

CHAT_MODE = [
    {
        "display": "関西弁アシスタント",
        "instructions": "あなたはアシスタントです。生粋の関西弁で応答してください。"
    },
    {
        "display": "東北弁アシスタント",
        "instructions": "あなたはアシスタントです。生粋の東北弁で応答してください。"
    },
    {
        "display": "関東弁アシスタント",
        "instructions": "あなたはアシスタントです。生粋の関東弁で応答してください。"
    }
]

def mock_assistant(chat_id: str, user_msg: str, chat_history: List[str]) -> str:
    
    return call_func_aoai.postUserResponse(chat_id=chat_id, user_msg=user_msg)


# ChatModeを選択するプルダウン。
chat_mode = st.selectbox("ChatModeを選択してください", [chat["display"] for chat in CHAT_MODE])
# チャットModeが選択されたら、CreateChatBotを呼び出す。選択されたモードがすでに選択済みの場合は何もしない
if chat_mode and st.session_state.get("chat_mode") != chat_mode:
    logging.info(f"🚀 st.session_state.get(chat_mode): {st.session_state.get('chat_mode')}")
    logging.info(f"🚀 chat_mode: {chat_mode}")
    instruction = [chat["instructions"] for chat in CHAT_MODE if chat["display"] == chat_mode][0]
    chat_id = call_func_aoai.createChatBot(instruction=instruction)
    # st.stateにchat_modeとchat_idを保存
    st.session_state.chat_mode = chat_mode
    st.session_state.chat_id = chat_id
    
    # チャットログを初期化
    st.session_state.chat_log = []

# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

user_msg = st.chat_input("メッセージを入力")
if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # 最新のユーザメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントのメッセージを表示
    res_message = mock_assistant(chat_id=st.session_state.get("chat_id"), user_msg=user_msg, chat_history=st.session_state.chat_log)
    with st.chat_message(ASSISTANT_NAME):
        assistant_msg = res_message
        assistant_response_area = st.empty()
        assistant_response_area.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
    # チャットログを出力
    print(" ■チャットログ:")
    for chat in st.session_state.chat_log:
        print("  " + chat["name"] + ": " + chat["msg"])