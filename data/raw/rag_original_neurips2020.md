# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., NeurIPS 2020)

**Source:** arXiv:2005.11401 (https://arxiv.org/html/2005.11401v1)

---

Title:

Content selection saved. Describe the issue below:

Description:

![](https://arxiv.org/static/base/1.0.1/images/icons/smileybones-small.svg)arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2005.11401v1 \[cs.CL\] 22 May 2020

# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

Patrick Lewis‡†{}^{\\dagger}{}^{\\ddagger}, Ethan Perez⋆,&Aleksandra Piktus†, Fabio Petroni†, Vladimir Karpukhin†, Naman Goyal†, Heinrich Küttler†,&Mike Lewis†, Wen-tau Yih†, Tim Rocktäschel‡†{}^{\\dagger}{}^{\\ddagger}, Sebastian Riedel‡†{}^{\\dagger}{}^{\\ddagger}, Douwe Kiela†

†Facebook AI Research; ‡University College London; ⋆New York University;

plewis@fb.com

###### Abstract

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks.
However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures.
Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems.
Pre-trained models with a differentiable access mechanism to explicit non-parametric memory
can overcome this issue, but
have so far been only investigated for extractive downstream tasks.
We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) — models which combine pre-trained parametric and non-parametric memory for language generation.
We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever.
We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token.
We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures.
For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

## 1 Introduction

Pre-trained neural language models have been shown to learn a substantial amount of in-depth knowledge from data \[ [41](https://arxiv.org/html/2005.11401v1#bib.bib41 "")\].
They can do so without any access to an external memory, as a parameterized implicit knowledge base \[ [45](https://arxiv.org/html/2005.11401v1#bib.bib45 ""), [46](https://arxiv.org/html/2005.11401v1#bib.bib46 "")\].
While this development is exciting, such models do have downsides:
They cannot easily expand or revise their memory, can’t straightforwardly provide insight into their predictions, and may produce “hallucinations” \[ [34](https://arxiv.org/html/2005.11401v1#bib.bib34 "")\].
Hybrid models that combine parametric memory with non-parametric (i.e., retrieval-based) memories \[ [18](https://arxiv.org/html/2005.11401v1#bib.bib18 ""), [22](https://arxiv.org/html/2005.11401v1#bib.bib22 ""), [42](https://arxiv.org/html/2005.11401v1#bib.bib42 "")\] can address some of these issues because knowledge
can be directly revised and expanded, and its access can be inspected and interpreted.
REALM \[ [18](https://arxiv.org/html/2005.11401v1#bib.bib18 "")\] and ORQA \[ [27](https://arxiv.org/html/2005.11401v1#bib.bib27 "")\], two recently introduced models that combine masked language models \[ [8](https://arxiv.org/html/2005.11401v1#bib.bib8 "")\] with a differentiable retriever, have shown promising results, but have only explored open-domain extractive question answering.
Here, we bring hybrid parametric and non-parametric memory to the “workhorse of NLP,” i.e. sequence-to-sequence (seq2seq) models.

We endow pre-trained, parametric-memory generation models with a non-parametric memory through a general-purpose fine-tuning approach which we refer to as retrieval-augmented generation (RAG).
We build RAG models where the parametric memory is a pre-trained generative seq2seq transformer, and the non-parametric memory is a dense vector index of Wikipedia, accessed using a pre-trained neural retriever. We combine these components in an end-to-end probabilistic model; the document retriever (Dense Passage Retriever \[ [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\], henceforth DPR) provides latent documents conditioned on the input, and the seq2seq model (BART \[ [28](https://arxiv.org/html/2005.11401v1#bib.bib28 "")\]) then conditions on both these latent documents and the input to generate the output.
We marginalize the latent variables through a top-K approximation, either on a per answer basis (assuming the same document is responsible for all tokens) or a per answer token basis (assuming different documents can be responsible for different tokens).
Just like T5 \[ [45](https://arxiv.org/html/2005.11401v1#bib.bib45 "")\] or BART, RAG can be fine-tuned on any seq2seq task, whereby both the sequence generator and retriever are jointly learned.

There has been extensive previous work proposing architectures to enrich systems with non-parametric memory which are trained from scratch for specific tasks—e.g. in memory networks \[ [58](https://arxiv.org/html/2005.11401v1#bib.bib58 ""), [49](https://arxiv.org/html/2005.11401v1#bib.bib49 "")\], stack-augmented networks \[ [21](https://arxiv.org/html/2005.11401v1#bib.bib21 "")\] and memory layers for transformers \[ [26](https://arxiv.org/html/2005.11401v1#bib.bib26 "")\]. In contrast, we explore a setting where both parametric and non-parametric memory components are pre-trained and pre-loaded with extensive knowledge. Crucially, by using pre-trained knowledge-access mechanisms, the ability to access knowledge is present without additional training.

Our results highlight the benefits of combining parametric and non-parametric memory with generation for knowledge-intensive tasks.
Our RAG models achieve state-of-the-art results on open Natural Questions \[ [25](https://arxiv.org/html/2005.11401v1#bib.bib25 "")\], WebQuestions \[ [3](https://arxiv.org/html/2005.11401v1#bib.bib3 "")\] and CuratedTrec \[ [2](https://arxiv.org/html/2005.11401v1#bib.bib2 "")\] and strongly outperform recent approaches that use specialised pre-training objectives on TriviaQA \[ [20](https://arxiv.org/html/2005.11401v1#bib.bib20 "")\]. Despite these being extractive tasks, we find that unconstrained generation outperforms previous extractive approaches. For knowledge-intensive generation, we experiment with MS-MARCO \[ [1](https://arxiv.org/html/2005.11401v1#bib.bib1 "")\] and Jeopardy question generation, and we find that our models generate responses that are more factual, specific, and diverse than a BART baseline. For the FEVER \[ [50](https://arxiv.org/html/2005.11401v1#bib.bib50 "")\] fact verification task, we achieve results within 4% of sophisticated, state-of-the-art pipeline models which use strong supervision. Finally, we show that the non-parametric memory can be replaced in order to control generation, demonstrating a simple mechanism to update the knowledge that the model uses as facts about the world change.

![Refer to caption](https://arxiv.org/html/2005.11401v1/x1.png)Figure 1: An overview of retrieval-augmented generation (RAG). We combine a pre-trained retriever (Query Encoder \+ Document Index) with a pre-trained encoder-decoder (Generator) and fine-tune end-to-end. For some query xx, we use Maximum Inner Product Search (MIPS) to find the top-K most relevant documents of all documents ziz\_{i}. To make the final prediction yy, we treat zz as a latent variable and marginalize over the encoder-decoder predictions given different documents.

## 2 Methods

We explore RAG models which use the input sequence xx to retrieve text passages zz and use these passages as additional context when generating the target sequence yy. As shown in Figure [1](https://arxiv.org/html/2005.11401v1#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"), our models leverage two components: (i) a retriever pη​(z\|x)p\_{\\eta}(z\|x) with parameters η\\eta that returns (top-K truncated) distributions over text passages given a query xx and (ii) a generator pθ​(yi\|x,z,y1:i−1)p\_{\\theta}(y\_{i}\|x,z,y\_{1:i-1}) parametrized by θ\\theta that generates a current token based on a context of the previous i−1i-1 tokens y1:i−1y\_{1:i-1}, the original input xx and a retrieved passage zz.

To train the retriever and generator end-to-end, we treat the retrieved document as a latent variable.
We propose two models that marginalize over the latent documents in different ways to produce a distribution over generated text. In one approach, _RAG-Sequence_, the model uses the same document to predict each target token. In the other approach, _RAG-Token_, the model can predict each target token based on a different document. In what follows, we formally introduce both models and then describe the pηp\_{\\eta} and pθp\_{\\theta} components, as well as the training and decoding procedure in more detail.

### 2.1 Models

#### RAG-Sequence Model

The RAG-Sequence model uses the same retrieved document to generate the complete _sequence_. Technically, it treats the retrieved passage as a single latent variable that is marginalized to get the seq2seq probability p​(y\|x)p(y\|x) via a top-K approximation,

|     |     |     |
| --- | --- | --- |
|  | pRAG-Sequence​(y\|x)=∑z∈top-k(p(⋅\|x))pη​(z\|x)​∏iNpθ​(yi\|x,z,y1:i−1).p\_{\\text{\\tiny{RAG-Sequence}}}(y\|x)=\\sum\_{z\\in\\text{top-}k(p(\\cdot\|x))}p\_{\\eta}(z\|x)\\prod\_{i}^{N}p\_{\\theta}(y\_{i}\|x,z,y\_{1:i-1}). |  |

#### RAG-Token Model

In the RAG-Token model we can draw a different latent passage for each target _token_ and marginalize accordingly. This allows the generator to choose content from several documents when producing an answer. Formally, we define:

|     |     |     |
| --- | --- | --- |
|  | pRAG-Token​(y\|x)=∏iN∑z∈top-k(p(⋅\|x))pη​(zi\|x)​pθ​(yi\|x,zi,y1:i−1).p\_{\\text{\\tiny{RAG-Token}}}(y\|x)=\\prod\_{i}^{N}\\sum\_{z\\in\\text{top-}k(p(\\cdot\|x))}p\_{\\eta}(z\_{i}\|x)p\_{\\theta}(y\_{i}\|x,z\_{i},y\_{1:i-1}). |  |

Finally, we note that RAG can be used for sequence classification tasks by considering the target class as a target sequence of length one, in which case RAG-Sequence and RAG-Token are equivalent.

### 2.2 Retriever: DPR

The retrieval component pη​(z\|x)p\_{\\eta}(z\|x) is based on DPR \[ [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\]. DPR follows a bi-encoder architecture:

|     |     |     |
| --- | --- | --- |
|  | pη​(z\|x)∝exp⁡⟨𝐝​(z),𝐪​(x)⟩p\_{\\eta}(z\|x)\\propto\\exp\\left<\\mathbf{d}(z),\\mathbf{q}(x)\\right> |  |

where 𝐝​(z)\\mathbf{d}(z) is a dense representation of the document produced by a BERTBASE transformer \[ [8](https://arxiv.org/html/2005.11401v1#bib.bib8 "")\], and 𝐪​(x)\\mathbf{q}(x) a representation of the query by another BERTBASE transformer with a different set of parameters.

To efficiently calculate top-k(pη(⋅\|x))\\text{top-k}(p\_{\\eta}(\\cdot\|x)), the list of kk elements zz with highest prior probability pη​(z\|x)p\_{\\eta}(z\|x), DPR employs a Maximum Inner Product Search (MIPS) index provided by the FAISS library \[ [19](https://arxiv.org/html/2005.11401v1#bib.bib19 "")\].

For non-parametric pre-trained memory, we use a pre-trained bi-encoder from \[ [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\] to both initialize our retriever and to build the document index. This retriever was trained to retrieve documents which contain answers to TriviaQA \[ [20](https://arxiv.org/html/2005.11401v1#bib.bib20 "")\] questions and Natural Questions \[ [25](https://arxiv.org/html/2005.11401v1#bib.bib25 "")\].

### 2.3 Generator: BART

The generator component pθ​(yi\|x,z,y1:i−1)p\_{\\theta}(y\_{i}\|x,z,y\_{1:i-1}) could be modelled using any encoder-decoder. We use BART-large \[ [28](https://arxiv.org/html/2005.11401v1#bib.bib28 "")\], a pre-trained seq2seq transformer \[ [52](https://arxiv.org/html/2005.11401v1#bib.bib52 "")\] with 400M parameters. To combine the input xx with the retrieved content zz when generating from BART, we simply concatenate them.

BART was pre-trained using a denoising objective and a variety of different noising functions. It has obtained state-of-the-art results on a diverse set of generation tasks and outperforms comparably-sized T5 models \[ [28](https://arxiv.org/html/2005.11401v1#bib.bib28 "")\].
We refer to the BART generator parameters θ\\theta as the _parametric memory_ henceforth.

### 2.4 Training

We jointly train the retriever and generator components without any direct supervision on what document should be retrieved.
Given a fine-tuning training corpus of input/output pairs (xj,yj)(x\_{j},y\_{j}), we minimize the negative marginal log-likelihood of each target, ∑j−log⁡p​(yj\|xj)\\sum\_{j}-\\log p(y\_{j}\|x\_{j}) using stochastic gradient descent with Adam \[ [24](https://arxiv.org/html/2005.11401v1#bib.bib24 "")\].
Updating the document encoder during training is costly as it requires the document index to be periodically updated as REALM does during pre-training \[ [18](https://arxiv.org/html/2005.11401v1#bib.bib18 "")\]. We do not find this step necessary for strong performance, and we keep the document encoder (and index) fixed, only fine-tuning the query encoder and the generator.

### 2.5 Decoding

At test/decoding time, RAG-Sequence and RAG-Token require different ways to approximate arg​maxy⁡p​(y\|x)\\operatorname\*{arg\\,max}\_{y}p(y\|x).

#### RAG-Token

The RAG-Token model can be seen as a standard, autoregressive, seq2seq generator with transition probability:

|     |     |     |
| --- | --- | --- |
|  | pθ′​(yi\|x,y1:i−1)=∑z∈top-k(p(⋅\|x))pη​(zi\|x)​pθ​(yi\|x,zi,y1:i−1)p^{\\prime}\_{\\theta}(y\_{i}\|x,y\_{1:i-1})=\\sum\_{z\\in\\text{top-}k(p(\\cdot\|x))}p\_{\\eta}(z\_{i}\|x)p\_{\\theta}(y\_{i}\|x,z\_{i},y\_{1:i-1}) |  |

To decode, we can plug pθ′​(yi\|x,y1:i−1)p^{\\prime}\_{\\theta}(y\_{i}\|x,y\_{1:i-1}) into a standard beam decoder.

#### RAG-Sequence

The likelihood p​(y\|x)p(y\|x) does not break into a conventional per-token likelihood for the RAG-Sequence, and hence we cannot solve it with a single beam search pass. Instead, we run beam search for each candidate document zz, scoring each hypothesis using pθ​(yi\|x,z,y1:i−1)p\_{\\theta}(y\_{i}\|x,z,y\_{1:i-1}). This yields a set of hypotheses YY of which some might not have appeared in the beams of all documents. To estimate the probability of an hypothesis yy across all beams, we run an additional forward pass for each document zz for which yy does not appear in the beam, multiply the generator score with pη​(z\|x)p\_{\\eta}(z\|x) and then sum up the probabilities across beams for the marginals. We refer to this decoding procedure as “Thorough Decoding.”

For longer output sequences, \|Y\|\|Y\| can become large, requiring many forward passes. For more efficient decoding, we can make a further approximation that pθ​(y\|x,zi)≈0p\_{\\theta}(y\|x,z\_{i})\\approx 0 where yy was not generated during beam search from x,zix,z\_{i}. This avoids the need to run additional forward passes once the candidate set YY has been generated. We refer to this decoding procedure as “Fast Decoding”.

## 3 Experiments

We experiment with RAG in a wide range of knowledge-intensive tasks. For all experiments, we use a single Wikipedia dump for our non-parametric knowledge source. Following Lee et al. \[ [27](https://arxiv.org/html/2005.11401v1#bib.bib27 "")\] and Karpukhin et al. \[ [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\], we use the December 2018 dump. Each Wikipedia article is split into disjoint 100-word chunks, to make a total of 21,015,324 documents.111The reader is referred to Karpukhin et al. \[ [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\] for further details on how Wikipedia is pre-processed.
We use the DPR document encoder to compute document embeddings for each document, and we build a single MIPS index using FAISS \[ [19](https://arxiv.org/html/2005.11401v1#bib.bib19 "")\] using Hierarchical Navigable Small World approximation for efficient retrieval \[ [33](https://arxiv.org/html/2005.11401v1#bib.bib33 "")\], which is then used for all experiments. During training, we retrieve the top kk documents for each query, where we consider k∈{5,10}k\\in\\{5,10\\}. We determine kk for test time using validation data.
In the remainder of this section, we will discuss the experimental details for each of these task settings.

### 3.1 Open-domain Question Answering

Open-domain QA is an important real-world NLP application and is often used as test-bed for knowledge-intensive tasks \[ [18](https://arxiv.org/html/2005.11401v1#bib.bib18 "")\].
We tackle open-domain QA by treating questions and answers as simple input-output text pairs (x,y)(x,y), and we train RAG by directly minimizing the negative log-likelihood of answers.
We compare our results to the popular extractive QA paradigm \[ [5](https://arxiv.org/html/2005.11401v1#bib.bib5 ""), [7](https://arxiv.org/html/2005.11401v1#bib.bib7 ""), [27](https://arxiv.org/html/2005.11401v1#bib.bib27 ""), [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\], where answers are extracted as spans from retrieved documents, relying primarily on non-parametric knowledge.
In addition, we also compare to "Closed-Book QA" approaches \[ [46](https://arxiv.org/html/2005.11401v1#bib.bib46 "")\], which, like RAG, generate answers, but do not exploit latent retrieval, instead relying purely on parametric knowledge.

We consider four popular open-domain QA datasets: Natural Questions (NQ) \[ [25](https://arxiv.org/html/2005.11401v1#bib.bib25 "")\], TriviaQA (TQA) \[ [20](https://arxiv.org/html/2005.11401v1#bib.bib20 "")\]. WebQuestions (WQ) \[ [3](https://arxiv.org/html/2005.11401v1#bib.bib3 "")\] and CuratedTrec (CT) \[ [2](https://arxiv.org/html/2005.11401v1#bib.bib2 "")\]. The answers for CuratedTrec are given in the form of regular expressions, which has been cited as a reason why it is unsuitable for answer-generation models \[ [18](https://arxiv.org/html/2005.11401v1#bib.bib18 "")\]. To overcome this, we use a pre-processing step where we first retrieve the top 1000 documents for each query, and use the answer that most frequently matches the regex pattern as the supervision target. If no matches are found, we resort to a simple heuristic: generate all possible permutations for each regex, replacing non-deterministic symbols in the regex nested tree structure with a whitespace. As CuratedTrec and WebQuestions are small datasets, we follow DPR \[ [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\] by initializing CuratedTrec and WebQuestions models with our Natural Questions RAG model.

We use the same training/dev/testing splitting method as in previous work \[ [27](https://arxiv.org/html/2005.11401v1#bib.bib27 ""), [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\]
and report the standard Exact Match (EM) metric. For TriviaQA, in order to compare to T5 \[ [46](https://arxiv.org/html/2005.11401v1#bib.bib46 "")\], we do an additional test evaluation on the TriviaQA Wiki test set.

### 3.2 Abstractive Question Answering

Because RAG leverages an encoder-decoder model, it can go beyond extractive question-answering and answer questions with free-form, abstractive text generation. To test RAG’s ability to generate natural language responses in a knowledge-intensive setting, we use the MS-MARCO Natural Language Generation task v2.1 \[ [38](https://arxiv.org/html/2005.11401v1#bib.bib38 "")\]. This task consists of natural language questions submitted to a search engine, ten snippets retrieved from a search engine for each question, and a full sentence natural language answer annotated from these retrieved passages.

As we are interested in models that can perform their own latent retrieval, we do not use the supplied passages, only the questions and answers, thus treating MS-MARCO as an open-domain abstractive question answering task. MS-MARCO does contain some questions that cannot be answered in a way that matches the reference answer without access to the context passages, such as “What is the weather in volcano, CA?” so we note that performance on Open-MSMARCO will be lower than models that do use these gold context passages.

We further note that there are questions in MS-MARCO that cannot be answered using a Wikipedia knowledge source alone. In these cases, RAG can rely on the parametric implicit knowledge in its BART parameters in order to generate commonsense responses.

### 3.3 Jeopardy Question Generation

In order to further evaluate RAG’s generation abilities in a non-question answering setting, we propose to study Open-domain question generation.
Rather than repurpose questions from standard open-domain QA tasks, which typically consist of short and simple questions, we instead propose to study the more demanding task of generating of Jeopardy questions. Jeopardy is an unusual format that consists of trying to guess an entity from a fact about that entity. For example, “The World Cup” is the answer to the jeopardy question “In 1986 Mexico scored as the first country to host this international sports competition twice.” As Jeopardy “questions" are precise, factual statements, generating Jeopardy-style questions conditioned on the answer entity they refer to constitutes a challenging knowledge-intensive generation task.

We use the raw Jeopardy data and splits from SearchQA
\[ [10](https://arxiv.org/html/2005.11401v1#bib.bib10 "")\], consisting of 97,391 training, 13,713 development, and 26,848 test datapoints. As this is a new task, we also train a BART system to compare RAG to.

[... middle omitted — see footer ...]


- Zhang and Bansal \[2019\]
Shiyue Zhang and Mohit Bansal.

Addressing semantic drift in question generation for semi-supervised
question answering.

In _Proceedings of the 2019 Conference on Empirical Methods in_
_Natural Language Processing and the 9th International Joint Conference on_
_Natural Language Processing (EMNLP-IJCNLP)_, pages 2495–2509, Hong Kong,
China, November 2019. Association for Computational Linguistics.

doi: 10.18653/v1/D19-1253.

URL [https://www.aclweb.org/anthology/D19-1253](https://www.aclweb.org/anthology/D19-1253 "").

- Zhong et al. \[2019\]
Wanjun Zhong, Jingjing Xu, Duyu Tang, Zenan Xu, Nan Duan, Ming Zhou, Jiahai
Wang, and Jian Yin.

Reasoning over semantic-level graph for fact checking.

_ArXiv_, abs/1909.03745, 2019.

URL [https://arxiv.org/abs/1909.03745](https://arxiv.org/abs/1909.03745 "").


## Appendix A Human evaluation

![Refer to caption](https://arxiv.org/html/2005.11401v1/images/annotation_interface.png)Figure 4: Annotation interface for human evaluation of factuality. A pop-out for detailed instructions and a worked example appear when clicking "view tool guide".

Figure [4](https://arxiv.org/html/2005.11401v1#A1.F4 "Figure 4 ‣ Appendix A Human evaluation ‣ Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks") shows the user interface for human evaluation. To avoid any biases for screen position, which model corresponded to sentence A and sentence B was randomly selected for each example. Annotators were encouraged to research the topic using the internet, and were given detailed instructions and worked examples in a full instructions tab. We included some gold sentences in order to assess the accuracy of the annotators. Two annotators did not perform well on these examples and their annotations were removed from the results.

## Appendix B Further details on Open-Domain QA

For open-domain QA, multiple answer annotations are often available for a given question. These answer annotations are exploited by extractive models during training as typically all the answer annotations are used to find matches within documents when preparing training data. For RAG, we also make use of multiple annotation examples for Natural Questions and WebQuestions by training the model with each (q,a)(q,a) pair separately, leading to a small increase in accuracy. For TriviaQA, there are often many valid answers to a given question, some of which are not suitable training targets, such as emoji or spelling variants. For TriviaQA, we filter out answer candidates if they do not occur in top 1000 documents for the query.

#### TriviaQA Evaluation setups

The open-domain QA community customarily uses public development datasets as test datasets, as test data for QA datasets is often restricted and dedicated to reading compehension purposes. We report our results using the datasets splits used in DPR \[ [22](https://arxiv.org/html/2005.11401v1#bib.bib22 "")\], which are consistent with common practice in Open-domain QA. For TriviaQA, this test dataset is the public TriviaQA Web Development split.
Roberts et al. \[ [46](https://arxiv.org/html/2005.11401v1#bib.bib46 "")\] used the TriviaQA official Wikipedia test set instead. Févry et al. \[ [14](https://arxiv.org/html/2005.11401v1#bib.bib14 "")\] follow this convention in order to compare with Roberts et al. \[ [46](https://arxiv.org/html/2005.11401v1#bib.bib46 "")\] (See appendix of \[ [14](https://arxiv.org/html/2005.11401v1#bib.bib14 "")\]). We report results on both test sets to enable fair comparison to both approaches. We find that our performance is much higher using the official Wiki test set, rather than the more conventional open-domain test set, which we attribute to the official Wiki test set questions being simpler to answer from Wikipedia.

## Appendix C Further details on FEVER

For FEVER classification, we follow the practice from \[ [28](https://arxiv.org/html/2005.11401v1#bib.bib28 "")\], and first re-generate the claim, and then classify using the representation of the final hidden state, before finally marginalizing across documents to obtain the class probabilities.
The FEVER task traditionally has two sub-tasks. The first is to classify the claim as either "Supported", "Refuted" or "Not Enough Info", which is the task we explore in the main paper. FEVER’s other sub-task involves extracting sentences from Wikipedia as evidence supporting the classification prediction. As FEVER uses a different Wikipedia dump to us, directly tackling this task is not straightforward. We hope to address this in future work.

## Appendix D "Null document" Probabilities

We experimented with adding "Null document" mechanism to RAG, similar to REALM \[ [18](https://arxiv.org/html/2005.11401v1#bib.bib18 "")\] in order to model cases where no useful information could be retrieved for a given input. Here, if kk documents were retrieved, we would additionally "retrieve" an empty document and predict a logit for the null document, before marginalizing over k+1k+1 predictions. We explored modelling this null document logit by learning (i) a document embedding for the null document, (ii) a static learnt bias term, or (iii) a neural network to predict the logit. We did not find that these improved performance, so in the interests of simplicity, we omit them. For Open MS-MARCO, where useful retrieved documents cannot always be retrieved, we observe that the model learns to always retrieve a particular set of documents for questions that are less likely to benefit from retrieval, suggesting that null document mechanisms may not be necessary for RAG.

## Appendix E Parameters

Our RAG models contain the trainable parameters for the BERT-base query and document encoder of DPR, with 110M parameters each (although we do not train the document encoder ourselves) and 406M trainable parameters from BART-large, 406M parameters, making a total of 626M trainable parameters. The best performing "closed-book" (parametric only) open-domain QA model is T5-11B with 11 Billion trainable parameters. The T5 model with the closest number of parameters to our models is T5-large (770M parameters), which achieves a score of 28.9 EM on Natural Questions \[ [46](https://arxiv.org/html/2005.11401v1#bib.bib46 "")\], substantially below the 44.5 that RAG-Sequence achieves, indicating that hybrid parametric/non-parametric models require far fewer trainable parameters for strong open-domain QA performance. The non-parametric memory index does not consist of trainable parameters, but does consists of 21M 728 dimensional vectors, consisting of 15.3B values.

## Appendix F Retrieval Collapse

In preliminary experiments, we observed that for some tasks such as story generation \[ [11](https://arxiv.org/html/2005.11401v1#bib.bib11 "")\], the retrieval component would “collapse” and learn to retrieve the same documents regardless of the input. In these cases, once retrieval had collapsed, the generator would learn to ignore the documents, and the RAG model would perform equivalently to BART.
The collapse could be due to a less-explicit requirement for factual knowledge in some tasks, or the longer target sequences, which could result in less informative gradients for the retriever. Perez et al. \[ [40](https://arxiv.org/html/2005.11401v1#bib.bib40 "")\] also found spurious retrieval results when optimizing a retrieval component in order to improve performance on downstream tasks.

──────── [TRUNCATED] ────────
Showing 22,162 chars (head) + 7,456 chars (tail) of 81,714 total clean characters.
Full text saved to: /home/hermes/.hermes/cache/web/arxiv.org-38c65e3450.md
To read the omitted middle: read_file path="/home/hermes/.hermes/cache/web/arxiv.org-38c65e3450.md" offset=165 limit=200  (the file is the complete page; raise/lower offset to page through it).
─────────────────────────────