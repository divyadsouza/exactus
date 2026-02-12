# Resources

## Core Papers

- [Attention is All You Need](https://arxiv.org/abs/1706.03762) - Original transformer architecture (Vaswani et al., 2017)
- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531) - Knowledge distillation foundations (Hinton, Vinyals, Dean, 2015)
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) - Parameter-efficient fine-tuning (Hu et al., 2021)
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) - Memory-efficient fine-tuning with 4-bit quantization (Dettmers et al., 2023)

## Hallucination Research

- [Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models](https://arxiv.org/abs/2309.01219) - Comprehensive survey on hallucination detection, explanation, and mitigation (Zhang et al., 2023)
- [R-Tuning: Instructing Large Language Models to Say 'I Don't Know'](https://arxiv.org/abs/2311.09677) - Refusal-aware instruction tuning to prevent fabrication (Zhang et al., 2023)

## Reference Models

- [NuExtract-2.0](https://huggingface.co/collections/numind/nuextract-20) - State-of-the-art structured extraction model family (NuMind)
- [NuExtract Blog Post](https://numind.ai/blog/nuextract-a-foundation-model-for-structured-extraction) - NuMind's approach to zero-hallucination extraction
- [Qwen2.5 Model Family](https://huggingface.co/Qwen) - Base models for NuExtract and Exactus candidates
- [Qwen3 Model Family](https://huggingface.co/collections/Qwen/qwen3) - Latest Qwen models with advanced reasoning capabilities and thinking mode
- [Phi-4](https://huggingface.co/microsoft/phi-4) - Microsoft's efficient reasoning model

## Practical Tutorials

- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft/index) - Parameter-efficient fine-tuning library
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/index) - Core library for working with LLMs
- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/) - Cross-platform inference optimization
- [OpenVINO Toolkit](https://docs.openvino.ai/) - Intel's toolkit for CPU inference optimization
- [llama.cpp](https://github.com/ggerganov/llama.cpp) - CPU/edge deployment for LLMs

## Evaluation & Benchmarking

- [SQuAD (Stanford Question Answering Dataset)](https://rajpurkar.github.io/SQuAD-explorer/) - Reading comprehension benchmark
- [TruthfulQA](https://github.com/sylinrl/TruthfulQA) - Benchmark for measuring model truthfulness
- [HaluEval](https://github.com/RUCAIBox/HaluEval) - Hallucination evaluation benchmark

## Courses & Learning Paths

- [Deep Learning Specialization](https://www.deeplearning.ai/courses/deep-learning-specialization/) - Andrew Ng's foundational course (alternative access)
- [Fast.ai Practical Deep Learning](https://course.fast.ai/) - Hands-on practical approach
- [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course) - Free course on NLP with transformers
- [LLM University by Cohere](https://cohere.com/llmu) - Comprehensive LLM fundamentals

## Project-Specific Resources

- [Open Data References](open_data_ref.md) - Curated datasets for training and validation
- [Training Data Samples](../data/training/) - Example JSONL files demonstrating data formats
- [training-data-validator Skill](.github/skills/training-data-validator/) - Tool for validating synthetic training data