import { Chroma } from '@langchain/community/vectorstores/chroma';
import { embeddings } from './embeddings.js';

export const vectorStore = new Chroma(embeddings, {
    collectionName: 'nexus'
})



