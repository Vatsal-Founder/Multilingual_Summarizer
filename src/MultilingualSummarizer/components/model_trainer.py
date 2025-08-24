import os, gc, torch
from datasets import load_from_disk
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq, TrainingArguments, Trainer
)

class ModelTrainer:
    def __init__(self, config):
        self.config = config

    def train(self):

        if torch.backends.mps.is_available():
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"

        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_mt5 = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_mt5)

        #loading the data
        dataset_samsum_pt = load_from_disk(self.config.data_path)


        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=1,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            gradient_accumulation_steps=8,     # effective batch = 8
            eval_strategy="steps",       # <-- correct arg name
            eval_steps=500,
            save_steps=1000000,                # int, not 1e6 float
            logging_steps=10,
            warmup_steps=200,                  # lower warmup to cut steps/memory
            weight_decay=0.01,
            optim="adafactor",                 # big memory win vs AdamW
            dataloader_pin_memory=False,       # CUDA-specific; off on MPS
            report_to="none",
            load_best_model_at_end=False,      # can set True if you also set metric_for_best_model
        )
        trainer = Trainer(model=model_mt5, args=trainer_args,
                  tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                  train_dataset=dataset_samsum_pt["test"],
                  eval_dataset=dataset_samsum_pt["validation"])
        

        
        #trainer.train()

        ## Save model
        #model_mt5.save_pretrained(os.path.join(self.config.root_dir,"mT5_multilingual-model"))
        ## Save tokenizer
        #tokenizer.save_pretrained(os.path.join(self.config.root_dir,"tokenizer"))
