# Large Language Models Can Be Easily Distracted by Irrelevant Context (Shi et al., ICML 2023)

**Source:** arXiv:2302.00093
**Authors:** Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed Chi, Nathanael Scharl, Denny Zhou
**Published:** ICML 2023

---

arXiv:2302.00093v3 \[cs.CL\] 6 Jun 2023

Large Language Models Can Be Easily Distracted by Irrelevant Context

1 2 \* 1 \* 1 3
Freda Shi Xinyun Chen Kanishka Misra Nathan Scales1 David Dohan1 Ed Chi1
1
Nathanael Scharli ¨ Denny Zhou1

Abstract

Large language models have achieved impressive
performance on various natural language processing tasks. However, so far they have been evaluated primarily on benchmarks where all information in the input context is relevant for solving
the task. In this work, we investigate the distractibility of large language models, i.e., how
the model problem-solving accuracy can be influenced by irrelevant context. In particular, we introduce Grade-School Math with Irrelevant Context
(GSM-IC), an arithmetic reasoning dataset with
irrelevant information in the problem description.
We use this benchmark to measure the distractibility of cutting-edge prompting techniques for large
language models, and find that the model performance is dramatically decreased when irrelevant
information is included. We also identify several
approaches for mitigating this deficiency, such
as decoding with self-consistency and adding to
the prompt an instruction that tells the language
1
model to ignore the irrelevant information.

th
Proceedings of the 40 International Conference on Machine
Learning, Honolulu, Hawaii, USA. PMLR 202, 2023. Copyright
2023 by the author(s).
1
Dataset is available at [https://github.com/](https://github.com/)

4\\mathcal^{t h}

Original Problem
Jessica is six years older than Claire. In two years,
Claire will be 20 years old. How old is Jessica now?
Modified Problem
Jessica is six years older than Claire. In two years, Claire
will be 20 years old. Twenty years ago, the age of
Claire’s father is 3 times of Jessica’s age. How old is
Jessica now?
Standard Answer 24

1
Dataset is available at [https://github.com/](https://github.com/)
google-research-datasets/GSM-IC.

Table 1. An example problem from GSM-IC. An irrelevant sentence (italic and underlined) that does not affect the standard answer is added immediately before the question.

related information, which may or may not be relevant to
the problems that we want to solve. We have to identify
what information is actually necessary during solving those
problems. Studies in psychology have shown that irrelevant
information may significantly decrease some children and
even adults problem-solving accuracy (Hoyer et al., 1979;
Pasolunghi et al., 1999; Marzocchi et al., 2002, inter alia).

In this work, we study the distractibility of large language
models for various prompting techniques; i.e., how is large
language model prompting affected by irrelevant context,
and what strategies can be used to improve performance? To
measure distractibility, we construct the GSM-IC dataset, a
grade-school math problem dataset derived from GSM8K
(Cobbe et al., 2021) and introduce two different metrics. In
contrast to prior work that derives benchmark variations by
arXiv:2302.00093v3 \[cs.CL\] 6 Jun 2023
substituting sentences of the base problems with variations
(Patel et al., 2021; Kumar et al., 2021, inter alia), we keep
the base problem description and add to it one irrelevant sentence, while making sure that it does not affect the solution
of the problem (Table 1).

2
[http://openai.com/api/](http://openai.com/api/)

* * *

Chowdhery et al., 2022).We find that their performance
on GSM-IC greatly decreases compared to the original
GSM8K (without irrelevant context). We then investigate
several approaches to mitigate this weakness, including
self-consistency (Wang et al., 2022c) and adding irrelevant
information to the exemplars in the prompt. In addition
to demonstrating how to handle irrelevant information via
exemplars, we also investigate the usage of task-specific
instructions (Wei et al., 2021; Sanh et al., 2021; Ouyang
et al., 2022; Suzgun et al., 2022; Chung et al., 2022), where
we prepend an instruction sentence “feel free to ignore irrelevant information in the problem description” to the
exemplars. We summarize our key findings below:

1. All investigated prompting techniques are sensitive to

2. All investigated prompting techniques are sensitive to
   irrelevant information in the problem description. In particular, among the original problems that can be solved
   by baseline prompts with greedy decoding, no more than
   18% of them can be consistently solved for all types of
   irrelevant information, showing that the large language
   model is easily distracted and produces inconsistent predictions when adding a small amount of irrelevant information to the problem description.

3. Self-consistency improves the performance of all prompt-

4. Self-consistency improves the performance of all prompting techniques on GSM-IC. In particular, the recall rate
   of the correct answer for GSM-IC is as high as 99.7%
   with 20 samples per problem, i.e., at least one of the 20
   solutions result in the correct final answer, which means
   that using multiple samples allows the model to almost
   always retrieve the correct answer.

5. Adding irrelevant information to the exemplars shown

6. Adding irrelevant information to the exemplars shown
   in the prompt consistently boosts the performance, and
   the same holds for adding an instruction to ignore irrelevant context. This suggests that language models
   are—to some extent—able to learn to ignore irrelevant
   information by following examples or instructions.

7. We identify different factors of the irrelevant information

8. We identify different factors of the irrelevant information
   that affect the model’s sensitivity to irrelevant context.
   Our breakdown analysis shows that varying the numbers
   in the irrelevant information does not notably change the
   model performance, while the degree of lexical overlap
   with the original problem description matters.
   Filtering out irrelevant information is essential for han-

9. Related Work


Few-shot prompting. Few-shot prompting (Brown et al.,
2020; Chowdhery et al., 2022, inter alia) has been significantly boosted with various techniques, including generating
intermediate steps (Ling et al., 2017; Cobbe et al., 2021;
Nye et al., 2021; Wei et al., 2022; Suzgun et al., 2022; Shi
et al., 2022b, inter alia), problem decomposition (Zhou
et al., 2022; Drozdov et al., 2022; Dohan et al., 2022; Khot
et al., 2022; Press et al., 2022, inter alia), generating programs (Austin et al., 2021; Chowdhery et al., 2022; Gao
et al., 2022; Chen et al., 2022, inter alia), marginalizing
intermediate steps that share the same result (Wang et al.,
2022c; Shi et al., 2022a), and ensemble (Wang et al., 2022b;
Drozdov et al., 2022). In addition, Kojima et al. (2022)
demonstrate that appropriate hint in prompts also leads to
decent performance, even without any exemplar. In this
work, we examine these cutting-edge prompting techniques
(Wei et al., 2022; Zhou et al., 2022; Kojima et al., 2022;
Wang et al., 2022c) on our benchmark, and demonstrate that
they are sensitive to irrelevant input context.
Natural language benchmarks with input perturbations.

Natural language benchmarks with input perturbations.
There has been a long line of work on adding input perturbations for natural language tasks, including model-agnostic
input transformations (Liang et al., 2022; Ravichander et al.,
2022, inter alia) and adversarial example generation against
individual models (Jia & Liang, 2017; Shi et al., 2018; Morris et al., 2020; Wang et al., 2021). In particular, prior work
has constructed arithmetic reasoning benchmarks through
paraphrasing or rewriting sentences in the base problems
from clean datasets (Patel et al., 2021; Kumar et al., 2021).
Meanwhile, Liang et al. (2022) evaluate various large language models under several metrics, including accuracy,
robustness, fairness, etc. Specifically, the input transformations in their robustness evaluation include semanticspreserving and semantics-altering perturbations, such as injecting typos and modifying sentences to change the groundtruth classification labels. In contrast the above work where
the meaning of problem descriptions may be changed with
perturbations, we keep all sentences in the original problem description, and introduce an irrelevant sentence that is
ensured not to affect the standard answer.
Natural language benchmarks with irrelevant input con-

Natural language benchmarks with irrelevant input context. Jia & Liang (2017) have shown that neural question answering systems are largely affected by adversarial
distracting sentences, whereas follow up work (Khashabi
et al., 2017; Ni et al., 2019) proposes learning strategies that
mitigate the problem. Similar issues have been found for
general-purpose pretrained language models, on the tasks
of factual reasoning (Kassner & Schutze, 2020; Pandia & ¨
Ettinger, 2021; Misra et al., 2023; Li et al., 2022), code
generation (Jones & Steinhardt, 2022), and syntactic generalization (Chaves & Richter, 2021). In particular, Li et al.

* * *

(2022) evaluated T5 (Raffel et al., 2020) and PaLM (Chowdhery et al., 2022) with few-shot prompts, and proposed
knowledge-aware finetuning that finetunes the model on
problems with counterfactual and irrelevant context, which
strengthens the model robustness to noisy context. In our
evaluation, we show that without training or finetuning,
adding irrelevant context into demonstrations in the prompt
also mitigates the distractibility of the underlying language
model and significantly improves the model performance
on our GSM-IC benchmark.

There exist some logical reasoning benchmarks that contain irrelevant content in task descriptions (Weston et al.,
2015; Sinha et al., 2019; Clark et al., 2021; Han et al., 2022;
Tafjord et al., 2020, inter alia). However, previous work
largely focuses on designing models that require extra training, and prompting alone still hardly achieves the same level
of performance as finetuned models for these tasks (Han
et al., 2022; Creswell et al., 2022). In our work, we focus
on arithmetic reasoning, where prompting techniques have
achieved the state-of-the-art results, e.g., on GSM8K, while
we show that adding a single irrelevant sentence into the
problem description significantly degrades the performance.

Prompting with noisy ground truth. A line of work studies the model performance with incorrect prompting exemplars, i.e., the example problems are paired with wrong
answers (Min et al., 2022; Kim et al., 2022). In addition,
prior work has investigated the model sensitivity to other
parts of the prompt, such as instruction tuning with misleading and irrelevant instructions (Webson & Pavlick, 2021)
and wrong reasoning steps in the examples (Madaan & Yazdanbakhsh, 2022; Wang et al., 2022a). In particular, Madaan
& Yazdanbakhsh (2022) conclude that the correctness of
numbers and equations in chain-of-thought prompts does
not play a key role in model performance, but using wrong
entities and removing either equations or text explanation
in the reasoning steps drastically hamper the performance.
Different from this line of work, we always include correct
answers to example problems in the prompt, and ensure
that the irrelevant context added to the problem description
does not change the ground truth answer. We show that the
model performance significantly drops when presented with
irrelevant context in problem descriptions, and different distributions of numbers and entities in the irrelevant context
also lead to different levels of performance degradation.

3. The GSM-IC Dataset

In this section, we introduce the creation process of the
GSM-IC dataset (§3.1) and the evaluation metrics (§3.2).

|  | COT | LTM | PROGRAM | 0-COT |
| --- | --- | --- | --- | --- |
|  | 95.0 | 94.0 | 83.0 | 44.0 |
| +SC | 96.0 | 99.0 | 91.0 | 76.0 |

Table 2. Accuracy (×100) on the base 100-example dataset
using code-davinci-002. See Table 3 for results with
text-davinci-003.

Original Problem Jeanne wants to ride the Ferris wheel, the roller coaster, and the bumper cars. The Ferris wheel costs 5 tickets,the roller coaster costs 4 tickets and the bumper cars cost 4 tickets. Jeanne has 5 tickets. \[Irrelevant Sentence\] How many more tickets should Jeanne buy?

Options for \[NUMBER\]
In-Range 5,6,7,8...
Out-of-Range 100,1000,5000...

Figure 1. Illustration of the considered factors when creating the
GSM-IC dataset. Best viewed in color.

we then choose 100 problems from this development set
that can be correctly solved by at least one of the prompting
3
techniques mentioned in this paper; that is, our base dataset
is an “easy” subset of GSM8K (Table 2). Each base prob-
4
lem requires two to seven reasoning steps to solve. Among
the 100 base problems, 60 of them can be solved with two
reasoning steps. The full dataset statistics can be found in
Appendix A.
We then generate the examples of our new dataset by adding

We then generate the examples of our new dataset by adding
to each base problem one sentence containing irrelevant
information. We use a template-based method (Figure 1) to
generate these sentences, which can be characterized by the
following three factors:
• Topic of the inserted sentence. We write templates for

• Topic of the inserted sentence. We write templates for
both in-topic and off-topic sentences. In-topic sentences
are closely related to the topic of the original problem,
whereas off-topic sentences are about a different topic.

3
We do not generate new examples or perform analysis on the
test set to avoid potential tuning-on-test-set issues.
4
The number of reasoning steps of a problem is given by the

test set to avoid potential tuning-on-test-set issues.
4
The number of reasoning steps of a problem is given by the
number of sentences in its standard answer (Cobbe et al., 2021).

* * *

• Range of numbers. Since we focus on arithmetic reasoning, most sentence templates also contain a number blank.
We can choose to fill in the number blank with a number
of similar or different magnitude to those in the original
problem description. Concretely, for a number a, if there
exists a number b in the original problem description or
1 a
solution such that ≤ ≤ 10, we consider a as an
10 b
in-range number, and otherwise an out-of-range number.
Since the standard answer to GSM8K problems are all
positive integers, we only consider positive integers as the
number blank fillers.

\\textstyle{{frac{1}{10}};\\leq;{\\frac{a}{b}};\\leq;10}

We manually verify that (1) all the generated sentences are
acceptable in English and that (2) adding them does not
affect the standard solution of the base problem. Because
the above factors are orthogonal, we generate for each base
example a set of derived examples with different factor
combinations. The full GSM-IC benchmark consists of
58,052 examples. More details about the dataset creation
process can be found in Appendix A.

3.2. Evaluation Metrics

s(p)

For a problem p, we denote its standard solution by s(p),
and the solution of method M by M(p). To evaluate the
distractibility of M, we consider the following two metrics:

• Micro accuracy Accmicro(M; P) is the average accuracy
of method M over all the test problems P.
P

Amathit c\_{{m i c r o}}(\\mathcal{M};\\mathcal{P})

\\mathcal{P}

\ c c\_{\\mathit{m i c r o}}(\\mathcal{M};\\mathcal{P})=\\frac{\\sum\_{p\\in\\mathcal{P}}\\mathbb{1}\\left\[\\mathcal{M}(p)=s(p)\\right\]}{\|\\mathcal{P}\|}

This means that the micro accuracy weighs all the individual test problems equally.
Macro accuracy Acc (M; B) is the average accuracy

• Macro accuracy Accmacro(M; B) is the average accuracy
of method M over classes of test problems, where each
class P (b) consists of the set of test examples derived
from the base example b ∈B. We define M’s prediction
for a class P (b) to be correct if and only if M’s prediction
for all problems in this class are correct.
hV i

Amathit c\_{{\\mathit{m a c r o}}}(\\mathcal{M};\\mathcal{B})

\\mathcal{P}(b)

• Normalized accuracy measures how a method is affected
by the distractors, considering its accuracy on base problems. For a micro or macro accuracy aMachieved by
method M, we calculate its corresponding normalized
accuracy by
a

\\mathit c c c\_{\\mathit a m c r r o}(\\mathcal{M};\\mathcal{B})=\\frac{\\sum\_{b\\in\\mathcal{B}}\\mathbb{1}\\left\[\\bigwedge\_{p\\in\\mathcal{P}(b)}\\left\[\\mathcal{M}(p)=s(p)\\right\]\\right\]}{\|\\mathcal{B}\|}

where nMdenotes the base problem accuracy of method
M (Table 2).

:b\\in\\mathcal{B}

n\_{\\mathcal{M}}

\\mathcal{P}(b)

4. Investigated Solutions

In the following section, we review the investigated prompting techniques (§4.1), present the formats of our prompts
(§4.2), and introduce instructed prompting (§4.3).

4.1. Base Techniques

Chain-of-thought prompting (COT; Wei et al., 2022) is
a prompting technique that guides the language models to
solve a problem in a step-by-step manner. By presenting
exemplars that solve the corresponding problems with intermediate reasoning steps in the prompts, COT significantly
improves the reasoning performance over direct answer prediction without such intermediate reasoning steps.

Zero-shot chain-of-thought prompting (0-COT; Kojima
et al., 2022) is a variation of COT where the prompt does
not contain any exemplar. Instead, the model is prompted
directly with the problem of interest followed by the instruction “Let’s think step by step:”.

Least-to-most prompting (LTM; Zhou et al., 2022)
teaches language models to (1) break down a problem into
subproblems, and (2) solve those subproblems sequentially
using COT. The final answer is that to the last subproblem.

Program prompts (PROGRAM; Chowdhery et al., 2022)
represent the arithmetic reasoning process as a program.
Following prior work on solving GSM8K problems with
code (Chowdhery et al., 2022; Gao et al., 2022; Chen et al.,
2022), we include a Python program as the problem solution
in the prompt, and execute the generated Python code using
an external Python interpreter to obtain the final answer.

Self-consistency (SC; Wang et al., 2022c; Shi et al., 2022a)
may further boost the reasoning performance by marginalizing over intermediate reasoning steps that share the same
final result. In practice, SC can be implemented by (1) sampling several solutions from the large language model and
(2) taking the majority vote. Note that SC is orthogonal to
above techniques, and can be combined with any of them.

We present some example prompts used in our experiments
(Figure 2). For few-shot prompting techniques (i.e., COT,
LTM and PROGRAM), the input prompt includes exemplar
problems and their solutions before the problem of interest.
In order to keep simplicity and avoid over-fitting in prompt
engineering, we follow Zhou et al. (2022) on exemplar creation; that is, we only use one simple exemplar for our main
experiments. This exemplar is either based on the \[Original\
Problem\] or the \[Problem with Irrelevant Context\], which

4.2. Prompt Design

* * *

\[PROGRAM Solution\] =
A: Let’s solve the problem by a Python program:
Elsa\_apples = 5
Anna\_apples = 2 + Elsa\_apples
Elsa\_Anna\_apples = Elsa\_apples + $QQDBDSSOHV
print(Elsa\_Anna\_apples)

Q: Jeanne wants to ride the Ferris wheel, the roller FRDVWHU,
and the bumper cars. The Ferris wheel costs 5 tickets, the
roller FRDVWHU costs 4 WLFNHWV and the bumper cars cost 4
tickets. Jeanne has 5 tickets. Jeanne’s QHLJKERU rides 8
NLORPHWHUVto the bus VWDWLRQevery day. How many PRUe
tickets should Jeanne buy?

COT Prompt

0-CoT Prompt (No Exemplar Problem)

LTM Prompt

Q: \[Problem of Interest\]
A: Let's think step by step:

\[Original Problem\]
\[LTM Solution\]
Q: \[Problem of Interest\]
A: Let's break down this problem:

PROGRAM Prompt

\[Original Problem\]
\[PROGRAM Solution\]
Q: \[Problem of Interest\]
A: Let's solve the problem by a Python program:

Instructed COT Prompt

Solve grade school math problems. Feel free to ignore irrelevant information given in the questions.
\[Original Problem\]
\[CoT Solution\]
Q: \[Problem of Interest\]
A:

Figure 2. Prompt formats for the investigated techniques on the right, which are constructed from building blocks on the left (best viewed
in color). The \[Problem with Irrelevant Context\] is obtained by adding an irrelevant sentence (italic and underlined) to the original
problem description and it can be used as an alternative to the \[Original Problem\] in the prompts on the right. In these prompts, identifiers
highlighted and wrapped by brackets (e.g., \[Problem of Interest\]) are replaced by the contents of the corresponding building blocks. The
prompts for all settings can be found in Appendix C.

In addition to presenting irrelevant information in the exemplars, we also investigate whether natural language instructions help language models ignore irrelevant context and
become less distracted. Extending the line of work (Suzgun
et al., 2022; Sanh et al., 2021; Ouyang et al., 2022) that
includes a general task description before exemplars, we
add the sentence “Solve grade school math problems. Feel
free to ignore irrelevant information given in the questions.”
before our exemplars in the prompt (Figure 2), which explicitly instructs the language model to ignore irrelevant
information in the problem description.

4.3. Instructed Prompting

allows us to investigate the effect of irrelevant information
in the prompt exemplar. For 0-COT, we adhere to Kojima
et al. (2022) and directly present the problem of interest
followed by “A: Let’s think step by step:”.

5. Experiments

We compare the performance of different prompting techniques on GSM-IC-4K (Table 3), in terms of both micro

Being mindful of the experiment costs, we uniformly sample 4,000 examples from the GSM-IC dataset (denoted
5
by GSM-IC-4K) for evaluation and analysis purposes
throughout this paper. Unless otherwise specified, we
mainly use code-davinci-002 in our experiments, and
we also evaluate text-davinci-003 which is a model
trained with RLHF to better follow instructions (Ouyang
et al., 2022). For experiments without self-consistency decoding, we use greedy decoding (i.e., temperature τ = 0);
for self-consistency experiments that require multiple samples for a problem, we sample 20 responses with temperature τ = 0.7 following Wang et al. (2022c).

5
Our sampled GSM-IC-4K covers all 100 base problems.

* * *

Large Language Models Can Be Easily Distracted by Irrelevant Context

|  | Micro Accuracy |  |  |  | Macro Accuracy |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Method | 2 Steps | >2 Steps | Overall | Norm | 2 Steps | >2 Steps | Overall | Norm |
| Prompting Exemplar w/o Irrelevant Context, code-davinci-002 |  |  |  |  |  |  |  |  |
| CoT | 73.5 | 70.8 | 72.4 | 76.2 | 8.3 | 2.5 | 6.0 | 6.3 |
| CoT+Inst. | 79.0 | 76.0 | 77.8 | 81.8 | 20.0 | 7.0 | 15.0 | 15.8 |
| 0-CoT | 29.0 | 29.1 | 29.0 | 65.9 | 1.7 | 0.0 | 1.0 | 2.3 |
| 0-CoT+Inst. | 31.6 | 28.8 | 30.5 | 69.3 | 1.7 | 0.0 | 1.0 | 2.3 |
| LTM | 74.9 | 81.5 | 77.5 | 82.4 | 16.7 | 20.0 | 18.0 | 19.1 |
| LTM+Inst. | 80.1 | 81.3 | 80.6 | 85.7 | 18.3 | 35.0 | 25.0 | 26.6 |
| PROGRAM | 59.1 | 47.4 | 54.4 | 65.5 | 6.7 | 2.5 | 5.0 | 6.0 |
| PROGRAM+Inst. | 60.6 | 50.9 | 56.7 | 68.3 | 6.7 | 5.0 | 6.0 | 7.2 |
| CoT+SC | 87.6 | 90.1 | 88.1 | 91.8 | 29.0 | 28.3 | 30.0 | 31.3 |
| 0-CoT+SC | 61.6 | 68.4 | 64.3 | 84.6 | 0.0 | 2.5 | 1.0 | 1.3 |
| LTM+SC | 92.4 | 94.8 | 93.4 | 94.3 | 51.6 | 35.0 | 45.0 | 45.5 |
| PROGRAM+SC | 73.5 | 76.1 | 74.6 | 82.0 | 16.7 | 7.5 | 13.0 | 14.3 |
| Prompting Exemplar w/o Irrelevant Context, text-davinci-003 |  |  |  |  |  |  |  |  |
| CoT | 69.3 | 66.9 | 68.4 | 85.4 | 10.0 | 7.5 | 9.0 | 11.3 |
| CoT+Inst. | 72.0 | 70.3 | 71.3 | 89.1 | 11.7 | 12.5 | 12.0 | 15.0 |
| LTM | 78.0 | 73.6 | 76.3 | 94.2 | 5.0 | 0.0 | 5.0 | 6.2 |
| LTM+Inst. | 80.5 | 70.9 | 76.7 | 94.7 | 5.0 | 0.0 | 5.0 | 6.2 |
| Prompting Exemplar w/ Irrelevant Context, code-davinci-002 |  |  |  |  |  |  |  |  |
| CoT | 79.8 | 72.4 | 76.8 | 80.8 | 16.7 | 10.0 | 14.0 | 14.7 |
| CoT+Inst. | 80.5 | 74.4 | 78.1 | 82.2 | 20.0 | 12.0 | 17.0 | 17.9 |
| LTM | 78.1 | 84.6 | 80.7 | 85.9 | 23.3 | 35.0 | 28.0 | 29.8 |
| LTM+Inst. | 81.0 | 85.4 | 82.8 | 88.1 | 23.3 | 35.0 | 28.0 | 29.8 |
| PROGRAM | 67.0 | 55.0 | 62.2 | 74.9 | 11.7 | 5.0 | 9.0 | 10.8 |
| PROGRAM+Inst. | 68.8 | 54.8 | 63.2 | 76.1 | 15.0 | 7.5 | 12.0 | 14.5 |

Table 3. Micro and macro accuracies (×100) on the GSM-IC-4K dataset. SC denotes self-consistency. Norm is the overall accuracy
normalized by the fraction of solved base problems (Table 2), which is a measure for robustness w.r.t. irrelevant information. For
text-davinci-003, the base problem accuracy with COT is 80.0, and the base problem accuracy with LTM is 81.0. The best
numbers in each column for each section (i.e., whether using code-davinci-002 or text-davinci-003, whether using exemplar
with irrelevant context or not, and whether using self-consistency or not) are in boldface.

and macro accuracies, as well as their corresponding normalized accuracies. Overall, we observe significant performance drop for both models with all prompting techniques.
The drop on macro accuracy is especially large, showing
that fewer than 30% of the base problems are consistently
solved after adding distractors. Comparing the results of two
models, text-davinci-003 achieves better normalized
micro accuracy than code-davinci-002, though its
macro accuracy is mostly worse. In Figure 3, we present
a GSM-IC-4K example where a single irrelevant sentence
causes different types of errors in investigated prompting
techniques. One common error type is wrongly using the
number in the irrelevant sentence, as shown in the LTM
prediction and other examples in Appendix B. Even if the
model does not directly use the irrelevant number for numerical calculation, the presence of the irrelevant sentence in
the reasoning steps alone can still cause a wrong prediction,
as shown in the COT prediction.

els. Using code-davinci-002, LTM achieves about
double macro accuracy of COT. Interestingly, with
text-davinci-003, despite that LTM outperforms
COT on the micro accuracy, its macro accuracy is lower.
Specifically, text-davinci-003 is highly susceptible
to irrelevant context with role overlap; e.g., such irrelevant
sentences decrease the macro accuracy to 0 on problems
with more than 2 reasoning steps. See Table 4 for the breakdown performance on different types of irrelevant context.
Selecting exemplars with distractors mitigates the dis-

Selecting exemplars with distractors mitigates the distractibility. For few-shot prompts, we find that using exemplars with distractors (i.e., including problems with irrelevant context) consistently outperforms using the original
exemplars without distractors across prompting techniques.
While prior work has shown that training and fine-tuning
with different types of problems improves model robustness
(Li et al., 2022), our results show that prompting with exemplars that demonstrate how to ignore irrelevant context also
results in significant robustness improvement. In Table 5, we
further show that using exemplars with distractors does not
cause a performance drop on the original GSM8K dataset,

* * *

0RGLıHG3UREOHP
Maria buys a ODUge bar of French soap that lasts her for 2 months. She

0RGLıHG3UREOHP
Maria buys a ODUge bar of French soap that lasts her for 2 months. She
spends $8.00 per bar of soap. Every 10 months, Maria's QHLJKERUbuys a QHZ
VKDPSRRand PRLVWXUL\]HUfor Maria's QHLJKERU. If Maria wants to stock up for
WKHHQWLUe year, how much will she spend on soap?

Correct COT Output to the Original Problem
Maria spends $8.00 per bar of soap. She buys a bar of soap every 2
months. 7KHUe DUe 12 months in a \\HDU. Maria will spend $8.00 x 12 / 2 =
$48.00 on soap for the year. The answer is $48.00.

Output to the ModiıHG3UREOHP
COT
Maria buys a ODUge bar of French soap that lasts her for 2 months. She

Maria buys a ODUge bar of French soap that lasts her for 2 months. She
spends $8.00 per bar of soap. Every 10 months, Maria's QHLJKERUbuys a
new VKDPSRRand PRLVWXUL\]HUfor Maria's QHLJKERU. If Maria wants to
stock up for the HQWLUe \\HDU, she will spend $8.00 x 12 = $96.00 on soap.
The answer is $96.00.

LTM
Let's EUeak down this SUoblem: 1. How much does Maria spend on soap
every 10 months? 2. How much does Maria spend on soap every year?

1. Maria spends $8.00 per bar of soap. She buys a new bar of soap every
   10 months. So Maria spends $8.00 \* 10 = $80.00 every 10 months.
2. Maria spends $80.00 every 10 months. So Maria spends $80.00 \* 12 =
   $960.00 every year.
   The answer is $960.00.

PROGRAM
Soap\_price = 8.00
Soap\_per\_year = 2 \* 12
Soap\_total = Soap\_price \* Soap\_per\_year
print(Soap\_total)

Output: 192.0

Figure 3. Example problem and corresponding outputs by different
prompting techniques (best viewed in color). The COT answer to
the original problem is highlighted in green. The added irrelevant
sentence is in italic and highlighted in red, which causes different
errors (highlighted in yellow) for all prompting techniques. More
examples of model predictions can be found in Appendix B.

indicating that such a prompt design can be beneficial in
achieving better accuracy and robustness simultaneously.

Self-consistency significantly reduces the distractibility.
Taking the majority vote from 20 samples,

Self-consistency significantly reduces the distractibility.
6
Taking the majority vote from 20 samples, SC improves

Self-consistency significantly reduces the distractibility.
6
Taking the majority vote from 20 samples, SC improves
the overall micro accuracy by more than 11 percentage

Taking the majority vote from 20 samples,
the overall micro accuracy by more than 11 percentage
points. This means that in addition to improving model performance on clean arithmetic reasoning tasks (Wang et al.,
2022c), SC also substantially reduces the distractibility of

Taking the majority vote from 20 samples, SC improves
the overall micro accuracy by more than 11 percentage
points. This means that in addition to improving model performance on clean arithmetic reasoning tasks (Wang et al.,
2022c), SC also substantially reduces the distractibility of

2022c), SC also substantially reduces the distractibility of
large language models to irrelevant context. The gain on
micro accuracy is notably large on 0-COT (35.5 percentage

micro accuracy is notably large on 0-COT (35.5 percentage
points). Furthermore, the correct answer for 99.7% of the
problems is in the 20 sampled answers for both COT and
LTM. Even for 0-COT, the recall of correct solutions within

micro accuracy is notably large on 0-COT (35.5 percentage
points). Furthermore, the correct answer for 99.7% of the
problems is in the 20 sampled answers for both COT and
LTM. Even for 0-COT, the recall of correct solutions within

LTM. Even for 0-COT, the recall of correct solutions within
20 samples is 96.5%. Despite these improvements, the best
macro accuracy among all prompting techniques is only

macro accuracy among all prompting techniques is only
45%, suggesting that for more than half of the base problems, SC fails to prevent the model from being distracted
by different variants of irrelevant information. These results
imply that a better algorithm may be developed to further
reduce the distractibility based on a few sampled solutions.

macro accuracy among all prompting techniques is only
45%, suggesting that for more than half of the base problems, SC fails to prevent the model from being distracted
by different variants of irrelevant information. These results
imply that a better algorithm may be developed to further
reduce the distractibility based on a few sampled solutions.

reduce the distractibility based on a few sampled solutions.

Figure 4. Micro accuracies on GSM-IC-4K with respect to the
number of required reasoning steps.

5.2. Break-Down Analysis

5.2.1. FACTORS OF THE IRRELEVANT CONTEXT

We analyze the performance of COT, LTM and PROGRAM
with respect to the considered factors (§3.1) of the irrelevant sentences (Table 4). For both models, we find that
(1) in-topic sentences with (2) role name overlap and (3)
in-range numbers are generally more challenging, which
is examplified by Figure 3. For LTM, the latter two factors do not have a large effect on the micro accuracy. The
difference is more significant for the macro accuracy and,
as an anomaly, using distractors with in-range numbers
turns out to be less challenging than out-of-range numbers
when using irrelevant context in the exemplar. Again, with
code-davinci-002, LTM outperforms COT and PRO-
GRAM on all investigated sub-categories. On the other hand,
using text-davinci-003, LTM outperforms COT in
terms of the micro accuracy, but the macro accuracy is much
lower on all sub-categories.

5.2.2. BREAK-DOWN ACCURACIES W.R.T. # STEPS

6
If there is a tie, we take a random top-tier result for evaluation,
following Wang et al. (2022c) and Shi et al. (2022a).

We analyze the break-down accuracies for problems with
respect to the reasoning steps (Figure 4). While we see a
significant drop for COT and PROGRAM on problems that
require four or more steps in the reasoning process, the
performance of LTM is fairly consistent across difficulty.
In addition to the advantage of LTM on clean problems
for complicated reasoning (Zhou et al., 2022), our results
show that LTM is also less sensitive to irrelevant context for
complicated problems that require more steps to solve.

We analyze the break-down accuracies for problems with
respect to the reasoning steps (Figure 4). While we see a
significant drop for COT and PROGRAM on problems that
require four or more steps in the reasoning process, the
performance of LTM is fairly consistent across difficulty.
In addition to the advantage of LTM on clean problems
for complicated reasoning (Zhou et al., 2022), our results
show that LTM is also less sensitive to irrelevant context for
complicated problems that require more steps to solve.

* * *

Large Language Models Can Be Easily Distracted by Irrelevant Context

| Method | Micro Accuracy |  |  |  |  |  | Macro Accuracy |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Topic |  | Role Overlap |  | Num. Range |  | Topic |  | Role Overlap |  | Num. Range |  |  |  |
| In | Off | Yes | No | In | Out | In | Off | Yes | No | In | Out |  |  |
| Prompting Exemplar w/o Irrelevant Context (code-davinci-002) |  |  |  |  |  |  |  |  |  |  |  |  |  |
| COT | 63.1 | 80.7 | 68.3 | 76.6 | 70.2 | 74.6 | 10.2 | 33.0 | 10.3 | 22.2 | 11.0 | 19.0 |  |
| LTM | 70.8 | 83.4 | 77.0 | 78.2 | 77.2 | 77.8 | 23.5 | 45.0 | 25.8 | 35.4 | 27.0 | 29.0 |  |
| PROGRAM | 44.1 | 63.5 | 50.7 | 58.4 | 54.3 | 54.5 | 4.1 | 24.0 | 9.3 | 16.2 | 7.0 | 11.0 |  |
| Prompting Exemplar w/o Irrelevant Context (text-davinci-003) |  |  |  |  |  |  |  |  |  |  |  |  |  |
| COT | 63.3 | 72.9 | 68.7 | 68.1 | 67.2 | 69.6 | 16.3 | 36.0 | 17.5 | 20.2 | 19.0 | 22.0 |  |
| LTM | 75.4 | 76.9 | 75.6 | 76.8 | 75.3 | 77.2 | 6.1 | 7.0 | 6.2 | 9.1 | 6.0 | 6.0 |  |
| Prompting Exemplar w/ Irrelevant Context (code-davinci-002) |  |  |  |  |  |  |  |  |  |  |  |  |  |
| COT | 70.2 | 82.7 | 73.6 | 80.2 | 76.1 | 77.7 | 18.4 | 43.0 | 21.6 | 32.3 | 22.0 | 26.0 |  |
| LTM | 73.0 | 87.5 | 81.4 | 80.2 | 80.0 | 81.4 | 28.6 | 58.0 | 37.1 | 42.4 | 41.0 | 35.0 |  |
| PROGRAM | 52.9 | 70.5 | 60.2 | 64.5 | 61.5 | 62.8 | 10.2 | 37.0 | 14.4 | 23.2 | 15.0 | 17.0 |  |

Table 4. Breakdown accuracies (×100) w.r.t. the factors of the added irrelevant sentence. Lower accuracy indicates the model is more
fragile to the corresponding type of irrelevant contexts. Note that the macro average accuracies are higher than the corresponding ones
reported in Table 3, as we only include a subset of created problems (i.e., those corresponding to the appropriate factor) here to compute
the metric. The best result in each column is in boldface.

original exemplars reaches comparable or even better performance than uninstructed prompting that uses exemplars
with distractors for both COT and LTM. Note that adding
the instruction “Solve grade school math problems.” alone
does not significantly improve the performance, and it is the
instruction “Feel free to ignore irrelevant information given
in the questions.” that makes the difference. Similar to the
instruction “Let’s think step by step.” employed by 0-CoT,
this shows that language models are—to some extent—able
to follow natural language instructions in a way that dramatically changes their problem solving behavior, suggesting
that such instructions may be useful for guiding the behavior
of language models on more tasks.
On the original GSM8K development set (Cobbe et al.,

On the original GSM8K development set (Cobbe et al.,
2021; Zhou et al., 2022), we do not observe a drop in accuracy when using exemplars with irrelevant information,
adding natural language instructions, or both (Table 5). The
same holds for SVAMP (Patel et al., 2021), an arithmetic reasoning benchmark constructed by applying different types
of variations to math problems from existing clean datasets,
e.g., changing sentence structures, asking different questions with the same information, etc. This is impressive
because the results on GSM-IC show that prompt exemplars with irrelevant information and instructed prompting

[... middle omitted — see footer ...]


2. Blank fillers: role names.

(b) We choose from the name set {Ada, David, Emma, Jack, John, Mary, Max, Tom} for nonoverlapped role names.
(c) We write five names that have overlap with the original character, and five names that do not have overlap for each

(c) We write five names that have overlap with the original character, and five names that do not have overlap for each
problem.

X^{\\prime}

ℓ
(a) For in-range numbers, we randomly sample positive integers in the range of \[, 10r\], where ℓ and r denote the
10
smallest and the largest number that appear in the problem description and standard solution, respectively.

r

\\left lbrack\\frac{\\ell}{10},10r\\right\\rbrack

* * *

Large Language Models Can Be Easily Distracted by Irrelevant Context

Original Problem Kim plants 80 cherry pits. 25% of them sprout and Kim sells 6 of the saplings. How many cherry saplings does she have left?

Added Sentence Kim’s mother plants 20 more potatoes.

Ambiguous Problem Kim plants 80 cherry pits. 25% of them sprout and Kim sells 6 of the saplings. Kim’s mother plants 20 more potatoes. How many cherry saplings does she have left?

Fixed Problem Kim plants 80 cherry pits. 25% of them sprout and Kim sells 6 of the saplings. Kim’s mother plants 20 more potatoes. How many cherry saplings does Kim have left?

_Table 10. An example that adding irrelevant contexts causes ambiguity: after adding the sentence, it is unclear whether she refers to Kim_

or Kim’s mother. To ensure that the standard answer is unchanged, we modify the final question to make it clear and faithful to the original problem.

(b) For out-of-range numbers, we choose from the range of \[2, +∞)\[\
10 ℓ , 10r\]. For very few problems that ℓ is relatively large (i.e., ℓ > 10 5 ) where we choose out-of-range numbers from the range of \[2, 10 ℓ \]; for other problems we choose out-of-range numbers n = a × 10 b from the range \[10r, ∞), where a and b are both non-negative integers.\
\
(c)We write four in-range numbers and four out-of-range numbers for each problem.\
4\. Finally, if adding the irrelevant sentence causes ambiguity (e.g., Table 10), we fix the question to ensure that the standard solution to the generated problem remain the same as the base problem.\
B. Sample Predictions on GSM-IC In addition to the example outputs shown in Figure 3, we include more example problems and the predictions by different techniques (Tables 11 and 12).\
C. Full prompts in experiments We list the prompts for all experiments in Tables 13 and 14.\
\
* * *\
\
\| Method \| Original GSM8K Problem\
Jessica is six years older than Claire. In two years, Claire will be 20 years old. How old is Jessica now? \| Modified Problem (w/ Irrelevant Sentence)\
\
Jessica is six years older than Claire. In two years, Claire will be 20 years old. Twenty years ago, the age of Claire's father is 3 times of Jessica's age. How old is Jessica now? \|\
\| \-\-\- \| \-\-\- \| \-\-\- \|\
\| COT \| In two years, Claire will be 20 years old. So, Claire is 18 years old now. Jessica is six years older than Claire, so Jessica is 18+6=24 years old now. The answer is 24. \| Jessica is six years older than Claire, so Jessica is 20-6=14 years old. Twenty years ago, the age of Claire's father is 3 times of Jessica's age, so 20 years ago, the age of Claire's father is 3 _14=42 years old. The answer is 14. \|_\
_\| LTM \| Let's break down this problem:1.How old is Claire now?2.How old is Jessica now?_\
_1.In two years, Claire will be 20 years old.So Claire is 20-2=18 years old now._\
_2.Jessica is six years older than Claire.So Jessica is 18+6=24 years old now._\
_The answer is 24. \| A:Let's break down this problem:1.How old is Claire now?2.How old is Jessica now?_\
_1.In two years, Claire will be 20 years old.So Claire is 18 years old now._\
_2.Twenty years ago,the age of Claire's father is 3 times of Jessica's age.So 20 years ago,Claire's father is 3_ Jessica's age.So Claire's father is 3 _Jessica's age-20+18=3_ Jessica's age-2 years old now.So Claire's father is 3 _Jessica's age-2+6=3_ Jessica's age+4 years old now.So Claire's father is 3 _Jessica's age-14 years old now.So Claire's father is 3_ Jessica's age-14+20=3 _Jessica's age+6 years old now.So 3_ Jessica's age+6=3 _Jessica's age-2+6=3_ Jessica's age+4.So 3 _Jessica's age+6=3_ Jessica's age+4.So 6=4.So Jessica's age=2.So Jessica is 2 years old now.The answer is 2. \|\
\| PROGRAM \| Claire\_age=20-2\
Jessica\_age=Claire\_age+6\
print(Jessica\_age) \| Claire\_age=20-2\
Jessica\_age=Claire\_age-6\
Claire\_father\_age=3\*Jessica\_age\
print(Jessica\_age) \|\
\
Table 11. Output example #1 for different prompting techniques, on a GSM8K problem and a corresponding GSM-IC problem. While all\
techniques give correct answers to the original problem, they output different different results for the modified GSM-IC problem.\
\
* * *\
\
\| Method \| Original GSM8K Problem\
Lucy has $65 in the bank. She made a $15 deposit and then followed by a $4 withdrawal. What is Lucy's bank balance? \| Modified Problem (w/ Irrelevant Sentence)\
\
Lucy has $65 in the bank. She made a $15 deposit and then followed by a $4 withdrawal. Lucy's mother's monthly rent is $10. What is Lucy's bank balance? \|\
\| \-\-\- \| \-\-\- \| \-\-\- \|\
\| COT \| Lucy has $65 in the bank. She made a $15 deposit, so she has $65+$15=$80. She then made a $4 withdrawal, so she has $80-$4=$76. The answer is $76. \| Lucy has $65 in the bank. She made a $15 deposit and then followed by a $4 withdrawal. Lucy's mother's monthly rent is $10. Lucy's bank balance is $65+$15-$4-$10=$66. The answer is $66. \|\
\| LTM \| Let's break down this problem: 1. How much money did Lucy deposit? 2. How much money did Lucy withdraw? 3. How much money does Lucy have in the bank?\
\
1. Lucy deposited $15.\
2. Lucy withdrew $4.\
3. Lucy has $65+$15-$4=$76 in the bank.\
   The answer is $76. \| Let's break down this problem: 1. How much money did Lucy deposit? 2. How much money did Lucy withdraw? 3. How much money does Lucy have in the bank?\
4. Lucy deposited $15.\
5. Lucy withdrew $4.\
6. Lucy has $65+$15-$4-$10=$66 in the bank.\
   The answer is $66. \|\
   \| PROGRAM \| Lucy\_balance=65\
   Lucy\_balance=Lucy\_balance+15\
   Lucy\_balance=Lucy\_balance-4\
   print(Lucy\_balance) \| Lucy\_bank=65\
   Lucy\_bank=Lucy\_bank+15\
   Lucy\_bank=Lucy\_bank-4\
   Lucy\_bank=Lucy\_bank-10\
   print(Lucy\_bank) \|\
\
Table 12. Output example #2 for different prompting techniques, on a GSM8K problem and a corresponding GSM-IC problem. While all\
techniques give correct answers to the original problem, they output the same incorrect result for the modified GSM-IC problem.\
\
* * *\
\
| Method | Example w/IrrCx? | Prompt |\
| --- | --- | --- |\
| COT | X | Q: Elsa has 5 apples. Anna has 2 more apples than Elsa. How many apples do they have together? |\
| A: Anna has 2 more apples than Elsa, so Anna has 2+5=7 apples. Elsa and Anna have 5+7=12 apples together.The answer is 12. |  |  |\
| Q: \[Problem of Interest\] |  |  |\
| A: |  |  |\
| COT | √ | Q: Elsa has 5 apples. Anna has 2 more apples than Elsa. Liz has 4 peaches. How many apples do they have together? |\
| A: Anna has 2 more apples than Elsa, so Anna has 2+5=7 apples. Elsa and Anna have 5+7=12 apples together.The answer is 12. |  |  |\
| Q: \[Problem of Interest\] |  |  |\
| A: |  |  |\
| LTM | X | Q: Elsa has 5 apples. Anna has 2 more apples than Elsa. How many apples do they have together? |\
| A:Let's break down this problem:1.How many apples does Anna have?2.How many apples do Elsa and Anna have together? |  |  |\
| 1.Anna has 2 more apples than Elsa.So Anna has 2+5=7 apples. |  |  |\
| 2.Elsa and Anna have 5+7=12 apples together. |  |  |\
| Q:\[Problem of Interest\] |  |  |\
| A:Let's break down this problem: |  |  |\
| LTM | √ | Q: Elsa has 5 apples. Anna has 2 more apples than Elsa.Liz has 4 peaches. How many apples do they have together? |\
| A:Let's break down this problem:1.How many apples does Anna have?2.How many apples do Elsa and Anna have together? |  |  |\
| 1.Anna has 2 more apples than Elsa.So Anna has 2+5=7 apples. |  |  |\
| 2.Elsa and Anna have 5+7=12 apples together. |  |  |\
| Q:\[Problem of Interest\] |  |  |\
| A:Let's break down this problem: |  |  |\
| 0-COT | N/A | Q: \[Problem of Interest\] |\
| A:Let's think step by step: |  |  |\
| PROGRAM | X | Q: Elsa has 5 apples. Anna has 2 more apples than Elsa. How many apples do they have together? |\
| A:Let's solve the problem by a Python program: |  |  |\
| Elsa\_apples=5 |  |  |\
| Anna\_apples=2+Elsa\_apples |  |  |\
| Elsa\_Anna\_apples=Elsa\_apples+Anna\_apples |  |  |\
| print(Elsa\_Anna\_apples) |  |  |\
| Q:\[Problem of Interest\] |  |  |\
| A:Let's solve the problem by a Python program: |  |  |\
| PROGRAM | √ | Q: Elsa has 5 apples. Anna has 2 more apples than Elsa.Liz has 4 peaches. How many apples do they have together? |\
| A:Let's solve the problem by a Python program: |  |  |\
| Elsa\_apples=5 |  |  |\
| Anna\_apples=2+Elsa\_apples |  |  |\
| Elsa\_Anna\_apples=Elsa\_apples+Anna\_apples |  |  |\
| print(Elsa\_Anna\_apples) |  |  |\
| Q:\[Problem of Interest\] |  |  |\
| A:Let's solve the problem by a Python program: |  |  |\
\
5+7=12\
\
2+5=7\
\
5!7!=!12\
\
Table 13. Prompts used for all investigated techniques, without instruction. The placeholder \[Problem of Interest\] is substituted for each\
problem at the test time.\
\
* * *\
\
| Method | Example w/IrrCtx? | Prompt |\
| --- | --- | --- |\
| COt | ✕ | Solve grade school math problems. Feel free to ignore irrelevant information given in the questions.Q: Elsa has 5 apples. Anna has 2 more apples than Elsa. How many apples do they have together?A: Anna has 2 more apples than Elsa, so Anna has 2+5=7 apples. Elsa and Anna have 5+7=14 apples together.The answer is 12.Q:\[Problem of Interest\]A: |\
| COt | ✓ | Solve grade school math problems. Feel free to ignore irrelevant information given in the questions.Q: Elsa has 5 apples. Anna has 2 more apples than Elsa. Liz has 4 peaches. How many apples do they have together?A: Anna has 2 more apples than Elsa, so Anna has 2+5=7 apples. Elsa and Anna have 5+7=14 apples together.The answer is 12.Q:\[Problem of Interest\]A: |\
| LTM | ✕ | Solve grade school math problems. Feel free to ignore irrelevant information given in the questions.Q: Elsa has 5 apples. Anna has 2 more apples than Elsa. How many apples do they have together?A: Let's break down this problem:1. How many apples does Anna have?2. How many apples do Elsa and Anna have together?1. Anna has 2 more apples than Elsa.So Anna has 2+5=7 apples.2. Elsa and Anna have 5+7=12 apples together.Q:\[Problem of Interest\]A: Let's break down this problem: |\
| LTM | ✓ | Solve grade school math problems. Feel free to ignore irrelevant information given in the questions.Q: Elsa has 5 apples. Anna has 2 more apples than Elsa.Liz has 4 peaches.How many apples do they have together?A: Let's break down this problem:1. How many apples does Anna have?2. How many apples do Elsa and Anna have together?1. Anna has 2 more apples than Elsa.So Anna has 2+5=7 apples.2. Elsa and Anna have 5+7=12 apples together.Q:\[Problem of Interest\]A: Let's break down this problem: |\
| 0-COT | N/A | Solve grade school math problems. Feel free to ignore irrelevant information given in the questions.Q:\[Problem of Interest\]A: Let's think step by step: |\
| PROGRAM | ✕ | Solve grade school math problems. Feel free to ignore irrelevant information given in the questions.Q: Elsa has 5 apples. Anna has 2 more apples than Elsa. How many apples do they have together?A: Let's solve the problem by a Python program:Elsa\_apples=5Anna\_apples=2+Elsa\_applesElsa\_anna\_apples=Elsa\_apples+Anna\_applesprint(Elsa\_anna\_apples)Q:\[Problem of Interest\]A: Let's solve the problem by a Python program: |\
| PROGRAM | ✓ | Solve grade school math problems. Feel free to ignore irrelevant information given in the questions.Q: Elsa has 5 apples. Anna has 2 more apples than Elsa.Liz has 4 peaches.How many apples do they have together?A: Let's solve the problem by a Python program:Elsa\_apples=5Anna\_apples=2+Elsa\_applesElsa\_anna\_apples=Elsa\_apples+Anna\_applesprint(Elsa\_anna\_apples)Q:\[Problem of Interest\]A: Let's solve the problem by a Python program: |\
\
5+7=12\
\
Table 14. All prompts with instructions. The placeholder \[Problem of Interest\] is substituted for each problem at the test time.

──────── [TRUNCATED] ────────
Showing 37,489 chars (head) + 12,449 chars (tail) of 74,746 total clean characters.
Full text saved to: /home/hermes/.hermes/cache/web/arxiv.org-8a1140e88d.md
To read the omitted middle: read_file path="/home/hermes/.hermes/cache/web/arxiv.org-8a1140e88d.md" offset=756 limit=200  (the file is the complete page; raise/lower offset to page through it).
─────────────────────────────