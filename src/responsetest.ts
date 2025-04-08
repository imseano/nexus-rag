import { ChatOpenAI } from "@langchain/openai"
import { HumanMessage, SystemMessage } from "@langchain/core/messages"
import dotenv from "dotenv"
dotenv.config()

const model = new ChatOpenAI({ modelName: "gpt-3.5-turbo", temperature: 0, openAIApiKey: process.env.OPENAI_API_KEY })

const messages = [
    new SystemMessage({ content: "You are a helpful assistant." }),
    new HumanMessage({ content: "What is the capital of France?" }),
]

await model.invoke(messages) 
