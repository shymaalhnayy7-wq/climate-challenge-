import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer
from streamlit_mic_recorder import speech_to_text
from codecarbon import EmissionsTracker
import time

# إعداد تتبع انبعاثات الكشك
tracker = EmissionsTracker(save_to_file=False)
tracker.start()

st.set_page_config(page_title="AI Climate Pod", layout="centered")

st.title("🌍 صندوق التحدي المناخي (Replit Edition)")

# 1. التعرف على الوجه
st.header("👤 التعرف على الزائر")
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(key="face", video_frame_callback=video_frame_callback)

# 2. الأوامر الصوتية
st.header("🎤 سجل بصمتك الصوتية")
text = speech_to_text(language='ar', start_prompt="تحدث الآن...", key='speech')
if text:
    st.success(f"الذكاء الاصطناعي سمع: {text}")

# 3. حساب الأثر البيئي
if st.button("تحليل البصمة النهائية"):
    emissions = tracker.stop()
    st.metric("بصمة الكود الكربونية لهذا الاستخدام", f"{emissions:.6f} kg CO2")
    st.balloons()
