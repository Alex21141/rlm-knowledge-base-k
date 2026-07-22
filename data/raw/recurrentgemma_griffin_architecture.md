# RecurrentGemma: Moving Past Transformers for Efficient Open Language Models

**Authors:** Griffin, RLHF, and Gemma Teams (Google DeepMind)  
**Paper:** arXiv:2404.07839 (Apr 11, 2024)  
**Code:** https://github.com/google-deepmind/recurrentgemma  
**Models:** RecurrentGemma-2B, RecurrentGemma-9B

## Abstract

We introduce RecurrentGemma, a family of open language models which uses Google's novel Griffin architecture. Griffin combines linear recurrences with local attention to achieve excellent performance on language. It has a fixed-sized state, which reduces memory use and enables efficient inference on long sequences.

We provide two sizes of models, containing 2B and 9B parameters, and provide pre-trained and instruction tuned variants for both. Our models achieve comparable performance to similarly-sized Gemma baselines despite being trained on fewer tokens.

## The Griffin Architecture

RecurrentGemma is based on Griffin, a hybrid model that mixes gated linear recurrences with local sliding window attention. This change improves computation and memory and is better suited for long context prompts.

The architecture eschews global attention, instead modelling the sequence through a mixture of linear recurrences (Gu et al., 2021; Orvieto et al., 2022) and local attention (Beltagy et al., 2020).

### Key Differences from Transformers

To perform inference, transformers must retrieve the KV cache and load it into device memory. This KV cache grows linearly with sequence length. Although one can reduce the cache size by using local attention, this comes at the cost of reduced performance.

In contrast, RecurrentGemma compresses input sequences into a fixed size state without sacrificing performance. This reduces memory use and enables efficient inference on long sequences.

### Model Hyper-parameters

| Parameter | RecurrentGemma-2B | RecurrentGemma-9B |
|-----------|-----------------|-------------------|
| Total params | 2.68B | 8.58B |
| Non-Embedding params | 2.03B | 7.53B |
| Embedding params | 0.65B | 1.05B |
| Vocabulary size | 256k | 256k |
| Model width | 2560 | 4096 |
| RNN width | 2560 | 4096 |
| MLP expansion factor | 3 | 3 |
| Depth | 26 | 38 |
| Attention heads | 10 | 16 |
| Local attention window size | 2048 | 2048 |

### Architecture Modifications

We make only a single modification to the Griffin architecture: multiplying the input embeddings by a constant equal to the square root of model width. The input and output embeddings are tied, but this factor is not applied to the output. A similar multiplicative factor appears in Gemma.

We do not apply weight decay to the parameters of the recurrent (RG-LRU) layers during training. Additionally, when backpropagating through the square root operation in the recurrent layers, we always clip the derivative to a maximum value of 1000 for stability.

## Layer Structure

There are 26 decoder layers in total (for the 2B model), grouped into repeating patterns.

The model begins with two residual blocks with a recurrent block (layers 0-1). This sequence is then followed by a residual block with local MQA (layer 2), and a series of continuous blocks that alternate until the end.

### Residual Block with Recurrent Block

In the recurrent block (Temporal mixing block), the model takes the input of dimension 2560 and applies two linear layers with output dimension 2560 in parallel, creating two branches.

On the first branch (right side), it applies a small separable Conv1D layer with a temporal filter dimension of 4, followed by the RG-LRU (Real-Gated Linear Recurrent Unit) layer.

On the second branch (left side), it applies a GeLU nonlinearity.

The branches are merged by element-wise multiplication, followed by a final linear layer with output dimension 2560. After applying RMSNorm, the MLP block follows.

### Residual Block with Local MQA

After two recurrent blocks, a residual block with local MQA follows. One key disadvantage of global attention is that its computational complexity grows quadratically in sequence length. To address this, RecurrentGemma uses local sliding window attention, allowing each position to attend only to a fixed number of tokens in the past (2048 tokens).

In the local MQA block, the model uses linear projections (q_proj, k_proj, v_proj, o_proj) to create query, key, value, and output representations. k_proj and v_proj share the same head with size 256, while q_proj and o_proj have 10 heads (256 x 10 = 2560).

It incorporates rotary positional embeddings (RoPE) just like the base Gemma models.

## Training Details

### Pre-training

RecurrentGemma is trained on sequences of 8192 tokens of the same pre-training data as Gemma-2B, which comprises primarily English data from web documents, mathematics, and code.

RecurrentGemma-2B is trained on 2T tokens compared to 3T tokens for Gemma-2B. A subset of the SentencePiece tokenizer with a vocabulary size of 256k tokens is used.

### Instruction Tuning and RLHF

A similar instruction tuning approach to Gemma is followed, including a novel RLHF algorithm to fine-tune the model to output responses with high reward.

## Inference Performance

RecurrentGemma achieves higher throughput at all sequence lengths considered. The throughput achieved by RecurrentGemma does not reduce as the sequence length increases, while the throughput achieved by Gemma falls as the cache grows.

RecurrentGemma-9B achieves particularly large (up to two orders of magnitude) improvements over Gemma-7B. This is primarily due to Gemma-7B using Multi-Head Attention, whereas Gemma-2B uses Multi-Query Attention.

When processing the prompt, both Gemma and RecurrentGemma achieve throughput of roughly 40K tokens per second for the 2B models and roughly 12K tokens per second for the 9B model. When sampling, RecurrentGemma achieves throughput of 6K tokens per second, with Gemma substantially slower.

## Limitations and Trade-offs

RecurrentGemma has reduced needle-in-a-haystack performance due to the fixed-sized state of the Griffin architecture. While it is possible to provide the entire text from a book as input, this approach may not be optimal.

Recurrent Neural Networks can encounter difficulties in learning long-range dependencies in exceedingly long sequences, and the model has a limited context window. This means it can only effectively consider a certain number of preceding tokens when making predictions.

Moreover, recurrent models have not yet received as much attention in terms of inference time optimizations compared to their transformer counterparts. There is less research and community support available compared to the well-established transformer architecture.

This model will be highly valuable in scenarios when you are concerned about exhausting your LLM's context window. By prioritizing the most recent information and strategically discarding older data, RecurrentGemma ensures that the LLM's performance remains strong as the context expands.

## Safety and Ethics

RecurrentGemma was evaluated on standard academic safety benchmarks including RealToxicity, Toxigen, BBQ, Winogender, Winobias, and TruthfulQA. The results are within acceptable thresholds for meeting internal policies for categories such as child safety, content safety, representational harms, memorization, and large-scale harms.

The models were trained on data filtered for removal of PII (Personally Identifiable Information). Developers are encouraged to adhere to privacy regulations with privacy-preserving techniques.
