import streamlit as st
from datetime import date, datetime

st.title("Your ToDoリスト")
st.caption("タスク管理アプリです。")
st.markdown("---")

# ToDoリストの初期化
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# タスク追加機能
st.subheader("NEW タスク")
new_task = st.text_input("タスクを入力", placeholder="プログラミング課題")
priority = st.selectbox("重要度を選択", ["低", "中", "高"])
due_date = st.date_input("期限日を選択", value=date.today())

if st.button("登録"):
    if new_task:
        st.session_state.todo_list.append({
            "task": new_task,
            "done": False,
            "priority": priority,
            "due_date": due_date
        })
        st.success(f"「{new_task}」登録完了")
        st.rerun()
    else:
        st.error("タスクを入力してください")

st.markdown("---")
# ToDoリスト表示
st.subheader("ToDoリスト")

if not st.session_state.todo_list:
    st.info("タスクはありません")
else:
    # 完了・未完了の統計
    total_tasks = len(st.session_state.todo_list)
    completed_tasks = sum(1 for item in st.session_state.todo_list if item["done"])
    
    st.write(f"**タスク数**: {total_tasks} 件 | **完了**: {completed_tasks} 件 | **残り**: {total_tasks - completed_tasks} 件")
    
    # 各タスクの表示
    for i, item in enumerate(st.session_state.todo_list):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            # 重要度に応じた背景色を設定
            priority_color = {
                "低": "#d4edda",  # 緑
                "中": "#fff3cd",  # 黄色
                "高": "#f8d7da"   # 赤
            }
            remaining_days = (item["due_date"] - date.today()).days
            remaining_text = f"残り日数: {remaining_days} 日" if remaining_days >= 0 else "期限切れ"
            
            st.markdown(
                f'<div style="background-color: {priority_color[item["priority"]]}; padding: 10px; border-radius: 5px;">'
                f'<strong>{item["task"]}</strong><br>'
                f'<small>期限日: {item["due_date"]} | {remaining_text}</small>'
                '</div>',
                unsafe_allow_html=True
            )
            
            # チェックボックスで完了状態を管理
            is_done = st.checkbox(
                item["task"], 
                value=item["done"], 
                key=f"checkbox_{i}"
            )
            
            # 完了状態が変更された場合
            if is_done != item["done"]:
                st.session_state.todo_list[i]["done"] = is_done
                st.rerun()
        
        with col2:
            # 削除ボタン
            if st.button("削除", key=f"delete_{i}"):
                st.session_state.todo_list.pop(i)
                st.success("タスクを削除しました")
                st.rerun()
        
        with col3:
            # 並び替え機能
            new_position = st.selectbox(
                "移動先",
                options=list(range(1, len(st.session_state.todo_list) + 1)),
                index=i,
                key=f"move_{i}"
            )
            
            if st.button("移動", key=f"move_button_{i}"):
                task = st.session_state.todo_list.pop(i)
                st.session_state.todo_list.insert(new_position - 1, task)
                st.success(f"タスク「{task['task']}」を位置 {new_position} に移動しました")
                st.rerun()

# 一括操作
if st.session_state.todo_list:
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("全て完了にする"):
            for item in st.session_state.todo_list:
                item["done"] = True
            st.success("全てのタスクを完了にしました")
            st.rerun()
    
    with col2:
        if st.button("完了済みタスクを削除"):
            st.session_state.todo_list = [item for item in st.session_state.todo_list if not item["done"]]
            st.success("完了済みタスクを削除しました")
            st.rerun()