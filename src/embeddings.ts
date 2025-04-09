import { OpenAIEmbeddings } from "@langchain/openai";

import dotenv from 'dotenv'

dotenv.config()

export const embeddings = new OpenAIEmbeddings({
    openAIApiKey: process.env.OPENAI_API_KEY,
    modelName: 'text-embedding-ada-002',
    maxRetries: 3
});