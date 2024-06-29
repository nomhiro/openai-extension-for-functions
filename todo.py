import streamlit as st
import pandas as pd
import numpy as np

tasks = [
  {
    "task": "すきやねんAzure7月の登壇ネタ検証",
    "priority": "high",
    "due_date": "2021-07-20",
    "status": "todo",
    "details": "Azure Functions for OpenAIを使ったデモを作成"
  },
  {
    "task": "AOAI Dev DayのLTネタ検討",
    "priority": "medium",
    "due_date": "2021-07-15",
    "status": "todo",
    "details": ""
  },
  {
    "task": "転職のための履歴書と職務経歴書の作成",
    "priority": "high",
    "due_date": "2021-06-16",
    "status": "progress",
    "details": "Wordで作成"
  }
]

USER_NAME = "user"
ASSISTANT_NAME = "assistant"

def mock_assistant(user_msg: str, chat_history) -> str:
  return "Hello! How can I help you today?"

# ブラウザのタブのタイトルを設定
st.set_page_config(page_title="ToDo App", page_icon=":clipboard:", layout="wide")

# 「チャット」ボタン押下時に、画面を左右にに分割して右側にチャット画面を表示
col1, col2 = st.columns([2, 1])
with col1:
  df = pd.DataFrame(tasks)

  # タスクを新規登録するボタン
  if st.button("タスクを新規登録する"):
      task = st.text_input("タスクを入力してください")
      if task:
          st.write(f"新しいタスク: {task}")
          # タスクを新規登録する処理を実装する

  # タスク一覧(tasks)をGridで表示
  st.write("■タスク一覧")
  st.table(df)
  
with col2:
  st.write("■チャット画面")
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
    res_message = mock_assistant(user_msg=user_msg, chat_history=st.session_state.chat_log)
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



