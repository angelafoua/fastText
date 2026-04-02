Here is the full content of `docs/dataset-guide.md`:

---

## Using Your Own Dataset with fastText

This guide explains which files to run, in what order, and why.

---

### Step 0: Build the binary (one-time setup)

```bash
$ make opt
```

This produces a `./fasttext` binary in the repo root. Do this once before anything else.

---

### Choose your workflow

| Task | Data you have | Command |
|------|--------------|---------|
| **Word vectors** | Unlabeled plain text | `skipgram` or `cbow` |
| **Text classification** | Labeled text | `supervised` |

---

### Workflow 1: Word Vectors (Unsupervised)

**Dataset format** — one sentence or document per line, no labels:
```
the cat sat on the mat
fastText is a library for text classification
natural language processing is fun
```

**Train:**
```bash
$ ./fasttext skipgram -input corpus.txt -output vectors
# or, faster but slightly lower quality:
$ ./fasttext cbow -input corpus.txt -output vectors
```

**Get a word's vector:**
```bash
$ echo "cat" | ./fasttext print-word-vectors vectors.bin
```

**Works for unknown words too** — fastText uses character n-grams internally:
```bash
$ echo "someunknownword" | ./fasttext print-word-vectors vectors.bin
```

**Find nearest neighbors:**
```bash
$ ./fasttext nn vectors.bin
Query word? cat
```

**Solve analogies:**
```bash
$ ./fasttext analogies vectors.bin
Query triplet (A - B + C)? berlin germany france
```

**Key flags:**

| Flag | Purpose | Default |
|------|---------|---------|
| `-dim` | Vector dimension | 100 |
| `-epoch` | Training epochs | 5 |
| `-lr` | Learning rate | 0.05 |
| `-minCount` | Min word frequency to include | 5 |
| `-minn` / `-maxn` | Character n-gram range | 3 / 6 |
| `-ws` | Context window size | 5 |
| `-thread` | CPU threads to use | all CPUs |

Example with custom flags:
```bash
$ ./fasttext skipgram -input corpus.txt -output vectors -dim 300 -epoch 10 -minCount 3
```

**Python equivalent:**
```python
import fasttext

model = fasttext.train_unsupervised("corpus.txt", model="skipgram")
print(model["cat"])                          # vector for a word
print(model.get_nearest_neighbors("cat"))    # nearest neighbors
model.save_model("vectors.bin")
model = fasttext.load_model("vectors.bin")
```

**Output files:**

| File | What it is |
|------|-----------|
| `vectors.bin` | Full binary model — use for `nn`, `analogies`, reloading |
| `vectors.vec` | Text file, one word vector per line — for inspection or external tools |

---

### Workflow 2: Text Classification (Supervised)

**Dataset format** — one example per line, label(s) prefixed with `__label__`:
```
__label__positive this movie was fantastic
__label__negative terrible film, waste of time
__label__positive great acting and story
```
Split your data into `train.txt` and `test.txt` (e.g. 80/20).

**Train:**
```bash
$ ./fasttext supervised -input train.txt -output model
```

**Evaluate (precision & recall):**
```bash
$ ./fasttext test model.bin test.txt
# top-5 instead of top-1:
$ ./fasttext test model.bin test.txt 5
```

**Predict:**
```bash
$ echo "this film was amazing" | ./fasttext predict model.bin -
# with probabilities:
$ echo "this film was amazing" | ./fasttext predict-prob model.bin -
```

**Autotune** (if you have a validation set):
```bash
$ ./fasttext supervised -input train.txt -output model -autotune-validation valid.txt
```

**Python equivalent:**
```python
import fasttext

model = fasttext.train_supervised("train.txt")
result = model.test("test.txt")
print(f"P@1: {result[1]:.3f}  R@1: {result[2]:.3f}")
labels, probs = model.predict("this film was amazing")
model.save_model("model.bin")
```

---

### Reduce model size (optional)

```bash
$ ./fasttext quantize -output model
# produces model.ftz — all commands still work:
$ ./fasttext test model.ftz test.txt
```

---

### Quick reference

```bash
# Build (one-time)
make opt

# Unsupervised — word vectors
./fasttext skipgram -input corpus.txt -output vectors
./fasttext cbow     -input corpus.txt -output vectors

# Supervised — classification
./fasttext supervised   -input train.txt -output model
./fasttext test         model.bin test.txt
./fasttext predict      model.bin test.txt
./fasttext predict-prob model.bin test.txt

# Utilities
./fasttext nn        vectors.bin    # nearest neighbors
./fasttext analogies vectors.bin    # word analogies
./fasttext quantize  -output model  # compress model
```
