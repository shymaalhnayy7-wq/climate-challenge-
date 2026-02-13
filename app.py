import streamlit as st
import cv2
import av
import time
import numpy as np
from streamlit_webrtc import webrtc_streamer
from codecarbon import EmissionsTracker

# 1. نظام تتبع الكربون (المصداقية التقنية)
tracker = EmissionsTracker(save_to_file=False)
tracker.start()

# إعدادات الواجهة المتطورة
st.set_page_config(page_title="Global Eco-Intelligence Hub", layout="wide", page_icon="🌱")

# تنسيق CSS احترافي (فلتر داكن مع لمسات خضراء)
st.markdown("""
    <style>
    .main { background: #05070a; }
    .stMetric { background: #0c1016; border-left: 5px solid #00ff7f; padding: 20px; border-radius: 10px; }
    .stButton>button { 
        background: linear-gradient(90deg, #004d40, #00c853); 
        color: white; border-radius: 12px; height: 3.5em; font-weight: bold; border: none;
    }
    .stExpander { background: #0c1016; border: 1px solid #1b5e20; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00ff7f;'>🌱 مركز الاستخبارات البيئية العالمي</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 🧠 وحدة قياس الوعي المعرفي (6 مستويات)")
    score = 0
    
    with st.expander("🔬 المستوى 1: كيمياء الغلاف الجوي", expanded=True):
        q1 = st.radio("أي من هذه الغازات يحبس الحرارة بفعالية أكبر بـ 80 مرة من CO2 على مدى 20 عاماً؟", 
                      ["الأكسجين", "الميثان (CH4)", "النيتروجين"])
        if q1 == "الميثان (CH4)": score += 16

    with st.expander("🌊 المستوى 2: النظم البحرية", expanded=True):
        q2 = st.selectbox("ما هي الظاهرة الناتجة عن امتصاص المحيطات لثاني أكسيد الكربون الزائد؟", 
                         ["تحمض المحيطات", "انخفاض الملوحة", "تجمد الأقطاب"])
        if q2 == "تحمض المحيطات": score += 16

    with st.expander("♻️ المستوى 3: الاقتصاد الدائري", expanded=True):
        q3 = st.radio("ما هي المادة التي يمكن إعادة تدويرها للأبد دون فقدان جودتها؟", 
                      ["البلاستيك", "الورق", "الألومنيوم والزجاج"])
        if q3 == "الألومنيوم والزجاج": score += 17

    with st.expander("⚡ المستوى 4: تحول الطاقة", expanded=False):
        q4 = st.selectbox("ما هو 'الهيدروجين الأخضر'؟", 
                         ["غاز مستخرج من النفط", "هيدروجين يُنتج باستخدام الطاقة المتجددة", "نوع من أنواع الفحم"])
        if q4 == "هيدروجين يُنتج باستخدام الطاقة المتجددة": score += 17

    with st.expander("🚜 المستوى 5: الزراعة المستدامة", expanded=False):
        q5 = st.radio("كم لتر من الماء يُستهلك لإنتاج كيلوغرام واحد من اللحم البقري تقريباً؟", 
                      ["100 لتر", "15,000 لتر", "500 لتر"])
        if q5 == "15,000 لتر": score += 17

    with st.expander("💻 المستوى 6: التكنولوجيا الخضراء", expanded=False):
        q6 = st.select_slider("مدى التزامك بتقليل البريد الإلكتروني غير الضروري (لتقليل طاقة الخوادم)؟", 
                             options=["منخفض", "متوسط", "عالٍ جداً"])
        if q6 == "عالٍ جداً": score += 17

    st.progress(score / 100)
    st.markdown(f"<p style='text-align: center; color: #00ff7f;'>مؤشر كفاءة الوعي: {score}%</p>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🖥️ رادار التحليل البصري (Green Cyber Filter)")
    
    def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")
        
        # --- إضافة الفلتر البيئي (Green Filter) ---
        green_overlay = np.zeros_like(img)
        green_overlay[:, :] = (0, 40, 0) # لون أخضر شفاف
        img = cv2.addWeighted(img, 0.8, green_overlay, 0.2, 0)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            color = (0, 255, 127)
            # رسم إطار تقني (Cyber Corners)
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 1)
            cv2.line(img, (x, y), (x+30, y), color, 5)
            cv2.line(img, (x, y), (x, y+30), color, 5)
            cv2.line(img, (x+w, y+h), (x+w-30, y+h), color, 5)
            cv2.line(img, (x+w, y+h), (x+w, y+h-30), color, 5)
            
            # عرض البيانات الفنية فوق الوجه
            cv2.putText(img, f"ID: ECO-AGENT-{hash(x)%1000}", (x, y-45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            status = "EXPERT" if score > 70 else "ANALYZING"
            cv2.putText(img, f"STATUS: {status}", (x, y-20), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)
            
            # شريط معالجة البيانات تحت الوجه
            cv2.rectangle(img, (x, y+h+15), (x+w, y+h+25), (255, 255, 255), 1)
            cv2.rectangle(img, (x, y+h+15), (x+int(w*(score/100)), y+h+25), color, -1)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(key="eco-radar", video_frame_callback=video_frame_callback)
    st.caption("الرؤية الحاسوبية تعمل الآن بفلتر تحليل الأثر البيئي النشط.")

# --- التقرير النهائي للمقيمين ---
st.divider()
if st.button("توليد التقرير التحليلي النهائي ✨", use_container_width=True):
    with st.status("جاري سحب البيانات التقنية وتحليل البصمة الرقمية...", expanded=True):
        time.sleep(2.5)
        emissions = tracker.stop()
        st.balloons()
        
    res_c1, res_c2, res_c3 = st.columns(3)
    with res_c1:
        st.metric("بصمة المعالجة (kg CO2)", f"{emissions:.7f}")
    with res_c2:
        st.metric("مستوى الوعي المحقق", f"{score}%")
    with res_c3:
        status_rank = "بطل مناخي (Elite)" if score > 80 else "ناشط بيئي"
        st.metric("الرتبة المكتشفة", status_rank)

    st.success(f"🌟 **الخلاصة التحليلية للمقيم:** 'هذا الكشك يدمج 6 مستويات من المعرفة العلمية مع الرؤية الحاسوبية المتطورة. الفلتر الأخضر المضاف ليس مجرد زينة، بل هو تمثيل بصري لكيفية رؤية الذكاء الاصطناعي للعالم من منظور مستدام. لقد أثبتنا اليوم أن التحليل الرقمي يمكن أن يكون أداة قوية لرفع الوعي وقياس الأثر في آن واحد.'")

st.markdown("---")
st.caption("نظام التطوير المستدام - نسخة التحكيم المتقدمة 2024")