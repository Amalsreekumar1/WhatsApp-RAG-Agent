from sentence_transformers import SentenceTransformer, util

def embed_chunks(model, chunks):  
    text = [chunk["heading"] + "\n" + chunk["text"] for chunk in chunks]
    vector = model.encode(text)
    return vector

def best_chunk(model, embeddings, message):
    question_vector = model.encode(message)
    best_chunks = util.semantic_search(question_vector, embeddings)
    return best_chunks

if __name__ == "__main__":
    from business import load_business
    from chunk import split_sections

    business = load_business("data/demo_academy")
    chunks = split_sections(business["documents"][0]["pages"][0]["text"])

    model = SentenceTransformer("BAAI/bge-m3")
    vectors = embed_chunks(model, chunks)

    """for q in ["Refund undo?", "paisa thirike kittumo", "hostel evide close cheyyum"]:
        hits = best_chunk(model, vectors, q)[0][:3]
        print(q)
        for h in hits:
            print("   ", round(h["score"], 3), chunks[h["corpus_id"]]["heading"])
    """
    
    tests = [
    # English
    ("How do I get admission?", "Admission process"),
    ("What are the class timings?", "Class timings"),
    ("What time must students return to the hostel?", "Hostel rules"),
    ("Will I get my money back if I cancel?", "Cancellation and refund"),
    ("Where do I check exam dates?", "Examination notifications"),
    ("Can I change my batch?", "Frequently asked questions"),

    # Malayalam script
    ("പ്രവേശനത്തിന് എന്ത് ചെയ്യണം?", "Admission process"),
    ("ക്ലാസ് എപ്പോഴാണ്?", "Class timings"),
    ("ഹോസ്റ്റൽ എപ്പോൾ അടയ്ക്കും?", "Hostel rules"),
    ("പണം തിരികെ കിട്ടുമോ?", "Cancellation and refund"),
    ("പരീക്ഷയുടെ തീയതി എവിടെ നോക്കണം?", "Examination notifications"),
    ("ബാച്ച് മാറ്റാൻ പറ്റുമോ?", "Frequently asked questions"),

    # Manglish
    ("admission engane edukkum", "Admission process"),
    ("class ethra manikku", "Class timings"),
    ("hostel evide close cheyyum", "Hostel rules"),
    ("paisa thirike kittumo", "Cancellation and refund"),
    ("exam date evide nokkam", "Examination notifications"),
    ("batch maaran pattumo", "Frequently asked questions"),

    # Not in the documents: expected None
    ("Do you have a swimming pool?", None),
    ("നീന്തൽക്കുളം ഉണ്ടോ?", None),
    ("what is the capital of france", None),
    ]
    right = 0
    for q, expected in tests:
        hit = best_chunk(model, vectors, q)[0][0]
        heading = chunks[hit["corpus_id"]]["heading"]
        score = round(hit["score"], 3)
        ok = heading == expected
        if expected is not None:
            right += ok
        print(score, "OK " if ok else "MISS", q, "->", heading)
  
    print(right, "of 18")