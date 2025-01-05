from googleapiclient.discovery import build
import os  # Untuk mengakses environment variables
import joblib  # Untuk memuat model machine learning
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key YouTube
API_KEY = os.getenv('YOUTUBE_API_KEY')

# Inisialisasi YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Muat model dan vectorizer
model = os.path.join(os.path.dirname(__file__), 'model/toxicity_model.pkl')
vectorizer = os.path.join(os.path.dirname(
    __file__), 'model/tfidf_vectorizer.pkl')


# Fungsi untuk mendapatkan live chat ID
def get_live_chat_id(video_id):
    try:
        request = youtube.videos().list(
            part='liveStreamingDetails',
            id=video_id
        )
        response = request.execute()
        live_chat_id = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
        return live_chat_id
    except Exception as e:
        print(f"Error in getting live chat ID: {e}")
        return None


# Fungsi untuk mengambil pesan live chat
def get_live_chat_messages(live_chat_id):
    try:
        request = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part='snippet',
            maxResults=200
        )
        response = request.execute()
        messages = []
        for item in response.get('items', []):
            snippet = item.get('snippet', {})
            if 'displayMessage' in snippet:
                messages.append({
                    'author': snippet.get('authorChannelId', 'Unknown Author'),
                    'message': snippet['displayMessage']
                })
        return messages
    except Exception as e:
        print(f"Error in getting live chat messages: {e}")
        return []


# Fungsi untuk memprediksi toxicitas
def predict_toxicity(message):
    message_vectorized = vectorizer.transform([message])  # Vectorize pesan
    prediction = model.predict(message_vectorized)  # Prediksi toxicitas
    return "TOXIC" if prediction[0] == 1 else "NOT TOXIC"


# Fungsi untuk mengambil dan menganalisis chat
def get_chats_and_toxicity(video_id):
    live_chat_id = get_live_chat_id(video_id)
    if live_chat_id:
        messages = get_live_chat_messages(live_chat_id)
        results = []
        for message in messages:
            toxicity = predict_toxicity(message['message'])
            results.append({
                "author": message['author'],
                "message": message['message'],
                "toxicity": toxicity
            })
        return results
    return []
