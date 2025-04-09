//import "cheerio"
import { ChatOpenAI } from "@langchain/openai"
//import { HumanMessage, SystemMessage } from "@langchain/core/messages"
import { Document } from "langchain/document"
import dotenv from "dotenv"
import { vectorStore } from "./vectorstore.js"
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio"
import { ChatPromptTemplate } from "@langchain/core/prompts"
import { pull } from "langchain/hub"
import { Annotation, StateGraph } from "@langchain/langgraph"
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter"
dotenv.config()

const model = new ChatOpenAI({ modelName: "gpt-3.5-turbo", temperature: 0, openAIApiKey: process.env.OPENAI_API_KEY })

//const messages = [
//    new SystemMessage({ content: "You are a helpful assistant." }),
 //   new HumanMessage({ content: "What is the capital of France?" }),
//]

const vec = vectorStore

const pTagSelector = "p"
const cheerioLoader = new CheerioWebBaseLoader("https://en.wikipedia.org/wiki/Paris", {
    selector: pTagSelector,
}
)

const docs = await cheerioLoader.load()

const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 1000,
    chunkOverlap: 200
})

const allSplits = await splitter.splitDocuments(docs)

await vec.addDocuments(allSplits)

const promptTemplate = await pull<ChatPromptTemplate>("rlm/rag-prompt")
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const InputStateAnnotation = Annotation.Root({question: Annotation<string>})


const StateAnnotation = Annotation.Root({
    question: Annotation<string>,
    context: Annotation<Document[]>,
    answer: Annotation<string>,
})

const retrieve = async (state: typeof InputStateAnnotation.State) => {
    const retrievedDocs = await vec.similaritySearch(state.question)
    return { context: retrievedDocs }
}

const generate = async (state: typeof StateAnnotation.State) => {
    const docsContent = state.context.map(doc => doc.pageContent).join("\n")
    const messages = await promptTemplate.invoke({ question: state.question, context: docsContent })
    const response = await model.invoke(messages)
    return { answer: response.content }
}

const graph = new StateGraph(StateAnnotation)
.addNode("retrieve", retrieve)
.addNode("generate", generate)
.addEdge("__start__", "retrieve")
.addEdge("retrieve", "generate")
.addEdge("generate", "__end__")
.compile();
//await model.invoke(messages) 

//const stream = await model.stream(messages);

//const chunks = [];
//for await (const chunk of stream) {
  //chunks.push(chunk);
  //console.log(`${chunk.content}|`);
//}

const inputs = { question: "What is this document about?" };

const result = await graph.invoke(inputs);
console.log(result.answer);