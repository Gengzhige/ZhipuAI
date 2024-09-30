import os
from zhipuai import ZhipuAI

# 初始化
client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])

# 创建知识库
knowledge = client.knowledge.create(
    embedding_id=3,
    name="论文知识库",
    description=""
)
print("创建知识库成功：", knowledge.id, "\n\n")

# 上传文件
for filename in os.listdir("papers"):
    result = client.files.create(
        file=open(os.path.join("./papers", filename), "rb"),
        purpose="retrieval", # 知识库检索
        knowledge_id=knowledge.id
    )
    print("文件上传成功：", result.successInfos)

# 提问
response = client.chat.completions.create(
    model="glm-4-plus",
    messages=[
        {"role": "user", "content": "生成Habitat和RoboGen的论文综述"},
    ],
    tools=[
        {
            "type": "retrieval",
            "retrieval": {
                "knowledge_id": os.environ["KNOWLEDGE_ID"],
                "prompt_template": """从文档
                \"\"\"\n{{knowledge}}\n\"\"\"
                中找问题
                \"\"\"\n{{question}}\n\"\"\"
                的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。
                不要复述问题，直接开始回答。"""
            }
        }
    ]
)
print("\n\n", response.choices[0].message.content)

# 删除知识库
result = client.knowledge.delete(
    knowledge_id=knowledge.id
)
print("\n\n删除知识库成功：", result.status_code)

