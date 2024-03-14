# 导入所需的库
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
import pandas as pd
import streamlit as st
from findLoc import findLoc
from modelscope import snapshot_download

# 在侧边栏中创建一个标题和一个链接
with st.sidebar:
    st.markdown("## InternLM LLM")
    "[InternLM](https://github.com/InternLM/InternLM.git)"
    "[SiteMaster](https://www.modelscope.cn/models/ECNUBigDataLab/SiteMaster)"
    system_prompt = st.text_input("System_Prompt", "请你耐心地为我提供选址指导")

# 创建一个标题和一个副标题
st.title("💬 InternLM2-Chat-7B SiteMaster")
st.caption("🚀 A streamlit chatbot powered by InternLM2")

# 定义模型路径
model_id = 'ECNUBigDataLab/SiteMaster'
mode_name_or_path = snapshot_download(model_id, revision='master')

# 定义一个函数，用于获取模型和tokenizer
@st.cache_resource
def get_model():
    # 从预训练的模型中获取tokenizer
    tokenizer = AutoTokenizer.from_pretrained(mode_name_or_path, trust_remote_code=True)
    # 从预训练的模型中获取模型，并设置模型参数
    model = AutoModelForCausalLM.from_pretrained(mode_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()
    model.eval()  
    return tokenizer, model

# 加载Chatglm3的model和tokenizer
tokenizer, model = get_model()

# 如果session_state中没有"messages"，则创建一个包含默认消息的列表
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 遍历session_state中的所有消息，并显示在聊天界面上
for msg in st.session_state.messages:
    st.chat_message("user").write(msg[0])
    st.chat_message("assistant").write(msg[1])

# 如果用户在聊天输入框中输入了内容，则执行以下操作
if prompt := st.chat_input():
    # 在聊天界面上显示用户的输入
    st.chat_message("user").write(prompt)
    start_loc=findLoc(prompt)

    # 构建输入     
    response, history = model.chat(tokenizer, prompt, meta_instruction='请你耐心地为我提供选址指导。', history=st.session_state.messages)
    # 将模型的输出添加到session_state中的messages列表中
    st.session_state.messages.append((prompt, response))
    # 在聊天界面上显示模型的输出
    st.chat_message("assistant").write(response)
    end_loc=findLoc(response)

    # if len(start_loc) == 0 and len(end_loc) == 0:
    #     pass
    # else:
    #     if len(start_loc) == 0:
    #         end_loc['pcolor'] = (999,999,0,50)
    #         result=end_loc
    #     elif len(end_loc) == 0:
    #         start_loc['pcolor'] = (0,999,0,50)
    #         result=start_loc
    #     else:
    #         start_loc['pcolor'] = (0,999,0,50)
    #         end_loc['pcolor'] = (999,999,0,50)
    #         result = pd.concat([start_loc, end_loc])
    #
    #     st.map(result,
    #            latitude='lat',
    #            longitude='lon',
    #            color='pcolor')
    if len(start_loc) == 0 and len(end_loc) == 0:
        pass
    else:
        if len(start_loc) == 0:
            end_loc['size'] = 50
            result=end_loc
        elif len(end_loc) == 0:
            start_loc['size'] = 50
            result=start_loc
        else:
            start_loc['size'] = 50
            end_loc['size'] = 50
            result = pd.concat([start_loc, end_loc])

        st.map(result,
               latitude='lat',
               longitude='lon',
               size=100,
               color=(130,42,220,255))