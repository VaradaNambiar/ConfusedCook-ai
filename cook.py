# This is a notebook exported as python file
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


# In[ ]:


def llm_chef(ingredients):
    
    llm = ChatGroq(model="gemma2-9b-it")

    message= "You are a chef. Suggest a recepie made out of {contents} and explain how to make it. Search the internet to find images of this dish "

    prompt_template = ChatPromptTemplate.from_messages({message})

    print("AI Chef is ready! What do you have today in your pantry?")
    #ingredients = input("Contents: ")
    prompt = prompt_template.format(contents=ingredients)

    result = llm.invoke(prompt)

    #print("you can make ->", result.content)
    return result.content

if __name__ == "__main__":
    res = llm_chef()
    print(res)