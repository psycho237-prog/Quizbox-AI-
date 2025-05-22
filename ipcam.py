import cv2
import pytesseract
from llama_cpp import Llama

# Chargement du modèle local (CPU)
llm = Llama(
        model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf",  # remplace par le chemin vers ton modèle
            n_ctx=2048,
                n_threads=8,  # ajuste selon ton CPU
                    use_mlock=True
)

def is_question(text):
    text = text.strip().lower()
        return (
                    text.endswith('?') or
                            text.startswith(('what', 'how', 'why', 'when', 'where', 'who',
                                                     'quel', 'quelle', 'quand', 'comment', 'pourquoi', 'qui'))
        )

        def ask(question):
            prompt = f"[INST] {question} [/INST]"
                output = llm(prompt, max_tokens=256, stop=["</s>"])
     ''               return output['choices'][0]['text'].strip()

                    # Accès à la caméra IP
                    ip_camera_url = 'http://10.53.59.86:8080/video'
                    cap = cv2.VideoCapture(ip_camera_url)

                    if not cap.isOpened():
                        print("Erreur : impossible d'ouvrir le flux vidéo.")
                            exit()

                            frame_skip = 2
                            frame_count = 0

                            while True:
                                ret, frame = cap.read()
                                    if not ret:
                                            print("Erreur : frame non lue.")
                                                    break

                                                        frame_count += 1
                                                            if frame_count % frame_skip != 0:
                                                                    continue

                                                                        frame = cv2.resize(frame, (640, 480))
                                                                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                                                                boxes = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

                                                                                    full_text = ""
                                                                                        for i in range(len(boxes['text'])):
                                                                                                if int(boxes['conf'][i]) > 60:
                                                                                                            x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                                                                                                                        text = boxes['text'][i].strip()
                                                                                                                                    full_text += text + " "

                                                                                                                                                if is_question(text):
                                                                                                                                                                try:
                                                                                                                                                                                    answer = ask(text)
                                                                                                                                                                                                        print(f"\nQUESTION : {text}\nRÉPONSE  : {answer}\n")
                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                            print(f"Erreur LLM : {e}")

                                                                                                                                                                                                                                                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                                                                                                                                                                                                                                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                                                                                                                                                                                                                                                                        cv2.imshow("OCR avec caméra IP", frame)
                                                                                                                                                                                                                                                                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                                                                                                                                                                                                                                                                    break

                                                                                                                                                                                                                                                                                    cap.release()
                                                                                                                                                                                                                                                                                    cv2.destroyAllWindows()
        )
)