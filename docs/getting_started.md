# Getting Started

1. Review the project structure and baseline model information in the [README](../README.md)
2. Examine the sample training files in `data/training/` to understand zero-hallucination data formats
3. Study the NuExtract model family as the reference baseline for structured extraction
4. Explore open datasets in [open_data_ref.md](open_data_ref.md) for training augmentation
5. Start with simple extraction tasks before moving to complex nested schemas
6. Experiment with different quantization techniques for CPU optimization
7. Document your learning journey, especially hallucination edge cases encountered

## FAQ

**Q: How do I validate my training data?**  
A: Use the [training-data-validator skill](.github/skills/training-data-validator/) to check for structural validity and semantic accuracy.

**Q: What if my model hallucinates?**  
A: Review anti-hallucination techniques in [key_concepts.md](key_concepts.md) and ensure temperature is set to 0.

**Q: Can I use GPUs for fine-tuning?**  
A: While possible, Exactus prioritizes CPU deployment; use LoRA/QLoRA for efficiency.

**Q: Where can I find more datasets?**  
A: Check [open_data_ref.md](open_data_ref.md) and resources in [resources.md](resources.md).