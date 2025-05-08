import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# Read data from csv file
df = pd.read_csv("danhsach_due.csv")

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('due.jpg')

col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.markdown("<br><br>")  # Thêm 2 dòng trắng phía trên logo
    st.image(image, width=180)  # Điều chỉnh width ở đây để logo lớn hơn, chẳng hạn width=200

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding: 20px 5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Courses Evaluation Dashboard</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)


# Thêm cột cho thông tin Last updated
# col3, col4, col5, col6 = st.columns([0.2, 0.45, 0.45, 0.45])

# Hiển thị ngày cập nhật
col3, filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([0.2, 0.3, 0.3, 0.3, 0.3])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")

# ---------- Bộ lọc Đơn vị (Khoa) ----------
with filter_col1:
    all_khoa = sorted(df['Đơn vị'].dropna().unique())
    selected_khoa = st.multiselect('Chọn Khoa (Đơn vị)', ['Tất cả'] + all_khoa)

    # Nếu chọn "Tất cả", lấy toàn bộ
    if 'Tất cả' in selected_khoa or not selected_khoa:
        filtered_df_khoa = df.copy()
    else:
        filtered_df_khoa = df[df['Đơn vị'].isin(selected_khoa)]

# ---------- Bộ lọc Giảng viên ----------
with filter_col2:
    all_teachers = sorted(filtered_df_khoa['Teacher_name'].dropna().unique())
    selected_teachers = st.multiselect('Chọn Giảng viên', ['Tất cả'] + all_teachers)

    if 'Tất cả' in selected_teachers or not selected_teachers:
        filtered_df_teacher = filtered_df_khoa
    else:
        filtered_df_teacher = filtered_df_khoa[filtered_df_khoa['Teacher_name'].isin(selected_teachers)]

# ---------- Bộ lọc Môn học ----------
with filter_col3:
    all_subjects = sorted(filtered_df_teacher['Subject_name'].dropna().unique())
    selected_subjects = st.multiselect('Chọn Môn học', ['Tất cả'] + all_subjects)

    if 'Tất cả' in selected_subjects or not selected_subjects:
        filtered_df_subject = filtered_df_teacher
    else:
        filtered_df_subject = filtered_df_teacher[filtered_df_teacher['Subject_name'].isin(selected_subjects)]

# ---------- Bộ lọc Mã lớp ----------
with filter_col4:
    all_classes = sorted(filtered_df_subject['Class_code'].dropna().unique())
    selected_classes = st.multiselect('Chọn Mã lớp học', ['Tất cả'] + all_classes)

    if 'Tất cả' in selected_classes or not selected_classes:
        final_filtered_df = filtered_df_subject
    else:
        final_filtered_df = filtered_df_subject[filtered_df_subject['Class_code'].isin(selected_classes)]

# ---------- Hiển thị kết quả ----------
# st.write("🔍 **Dữ liệu đã lọc:**")
# st.dataframe(final_filtered_df)


# # (Tuỳ chọn) Hiển thị dữ liệu đã lọc
# st.write("🔍 **Dữ liệu đã lọc:**")
# st.dataframe(final_filtered_df[final_filtered_df['Class_code'] == selected_class])

# Lọc dữ liệu theo giảng viên và môn học đã chọn
filtered_data = final_filtered_df.copy()

# st.dataframe(final_filtered_df)
col4, col5, col6 = st.columns([0.45, 0.45, 0.45])

total_students = df['Stu_id'].nunique()
total_teachers = df['Teacher_name'].nunique()
total_subjects = df['Subject_name'].nunique()

# Thêm các box thông tin tổng quát
with col4:
    st.markdown(f"""
        <div style='text-align: center; font-size: 32px;'>
            👨‍🎓<br><strong>{total_students}</strong><br><span style='font-size:24px'>Số sinh viên</span>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div style='text-align: center; font-size: 32px;'>
            👩‍🏫<br><strong>{total_teachers}</strong><br><span style='font-size:24px'>Số giảng viên</span>
        </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
        <div style='text-align: center; font-size: 32px;'>
            📚<br><strong>{total_subjects}</strong><br><span style='font-size:24px'>Số môn học</span>
        </div>
    """, unsafe_allow_html=True)

####################
# filtered_data = df[(df['Teacher_name'] == selected_teacher) & 
#                    (df['Subject_name'] == selected_subject)]

# Tạo danh sách các câu hỏi (Q1 đến Q12)

q_cols = [f'Q{i}' for i in range(1, 13)]
result_list = []

if not filtered_data.empty:
    for q in q_cols:
        avg_score = filtered_data[q].mean()
        std_score = filtered_data[q].std()
        count_level = [(filtered_data[q] == i).sum() for i in range(1, 6)]

        # Trung bình các lớp cùng học phần
        if selected_subjects and 'Tất cả' not in selected_subjects:
            subject_data = df[df['Subject_name'].isin(selected_subjects)]
        else:
            subject_data = df.copy()
        avg_class_hp = subject_data[q].mean()

        # Trung bình toàn trường
        avg_score_all = df[q].mean()

        result_list.append([
            q, round(avg_score, 2), round(std_score, 2), *count_level,
            round(avg_class_hp, 2), round(avg_score_all, 2)
        ])

    # Tạo DataFrame kết quả
    result_df = pd.DataFrame(result_list, columns=[
        'Câu hỏi', 'Đánh giá trung bình', 'Độ lệch chuẩn',
        'Số câu ở mức 1', 'Số câu ở mức 2', 'Số câu ở mức 3',
        'Số câu ở mức 4', 'Số câu ở mức 5',
        'TB các lớp của cùng HP', 'TB toàn trường'
    ])

    # Ánh xạ nội dung câu hỏi
    question_labels = {
        'Q1': 'đầy đủ về đề cương chi tiết học phần, gồm: chuẩn đầu ra, nội dung, phương pháp dạy - học, phương pháp kiểm tra - đánh giá, tài liệu học tập của học phần',
        'Q2': '2. Nội dung của học phần phù hợp với năng lực của người học',
        'Q3': '3. Phương pháp dạy - học phù hợp với chuẩn đầu ra và nội dung của học phần',
        'Q4': '4. Giảng viên thực hiện đầy đủ kế hoạch dạy - học đã công bố và tuân thủ các quy định trong giảng dạy',
        'Q5': '5. Giảng viên có cập nhật kiến thức mới và thực tế trong bài giảng',
        'Q6': '6. Hoạt động dạy - học khơi gợi đam mê khám phá và giúp phát triển khả năng tự học',
        'Q7': '7. Giảng viên khuyến khích người học chủ động tham gia thảo luận, giải quyết vấn đề trong giờ học',
        'Q8': '8. Giảng viên tận tụy, sẵn sàng giúp đỡ, giải đáp thỏa đáng các thắc mắc của người học',
        'Q9': '9. Giảng viên sử dụng hiệu quả Elearning và các phương tiện công nghệ trong tổ chức dạy học',
        'Q10':'10. Phương pháp kiểm tra, đánh giá phù hợp với chuẩn đầu ra và nội dung của học phần',
        'Q11': '11. Việc đánh giá được thực hiện công bằng, khách quan và đảm bảo độ tin cậy',
        'Q12': '12. Anh/Chị hài lòng về chất lượng và hiệu quả giảng dạy của giảng viên đối với sự tiến bộ trong học tập của bản thân'
    }
    result_df['Câu hỏi'] = result_df['Câu hỏi'].map(question_labels)

    # Tính trung bình toàn bảng cho các cột số
    avg_overall = {
        'Câu hỏi': 'Trung bình chung',
        'Đánh giá trung bình': round(result_df['Đánh giá trung bình'].mean(), 2),
        'Độ lệch chuẩn': '',
        'Số câu ở mức 1': '',
        'Số câu ở mức 2': '',
        'Số câu ở mức 3': '',
        'Số câu ở mức 4': '',
        'Số câu ở mức 5': '',
        'TB các lớp của cùng HP': round(result_df['TB các lớp của cùng HP'].mean(), 2),
        'TB toàn trường': round(result_df['TB toàn trường'].mean(), 2)
    }

    result_df = pd.concat([result_df, pd.DataFrame([avg_overall])], ignore_index=True)

    # Hiển thị tiêu đề
    st.write(f"📊 **Kết quả đánh giá**")
    if selected_teachers and 'Tất cả' not in selected_teachers:
        st.markdown(f"Giảng viên: **{', '.join(selected_teachers)}**")
    if selected_subjects and 'Tất cả' not in selected_subjects:
        st.markdown(f"Môn học: **{', '.join(selected_subjects)}**")

    # Hàm hiển thị HTML bảng
    def render_html_table(df):
        html = """
        <style>
            table {width: 100%; table-layout: fixed;}
            th, td {
                word-wrap: break-word;
                padding: 8px;
                text-align: center;
                vertical-align: top;
            }
            th:nth-child(1), td:nth-child(1) {
                text-align: left;
                width: 40%;
            }
        </style>
        """
        html += "<table border='1' style='border-collapse: collapse;'>"
        html += "<thead><tr>"
        for col in df.columns:
            html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"
        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                html += f"<td>{row[col]}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html

    st.markdown(render_html_table(result_df), unsafe_allow_html=True)

else:
    st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn.")

# Tạo 2 cột cạnh nhau
chart_col, comment_col = st.columns(2)

# ==== CỘT BIỂU ĐỒ CẢM XÚC ====
with chart_col:
    st.markdown("### 😊 Nhận xét đánh giá ")

    if 'sentiment' in filtered_data.columns:
        sentiment_counts = Counter({'Positive': 0, 'Neutral': 0, 'Negative': 0})
        sentiment_counts.update(filtered_data['sentiment'].dropna())

        labels = ['Positive', 'Neutral', 'Negative']
        values = [sentiment_counts[label] for label in labels]
        colors = ['green', 'gray', 'red']

        fig = go.Figure(data=[go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=values,
            textposition='outside'
        )])

        fig.update_layout(
            title=f'Phân bố cảm xúc - {selected_teachers} - {selected_subjects}',
            xaxis_title='Cảm xúc',
            yaxis_title='Số lượng',
            yaxis=dict(range=[0, max(values)+10000]),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Không tìm thấy cột `sentiment` trong dữ liệu.")

# ==== CỘT TOP 10 BÌNH LUẬN ====
with comment_col:
    st.markdown("### 📝 Những bình luận nổi bật")

    if 'comment_processed' in filtered_data.columns:
        sorted_comments = sorted(
            filtered_data['comment_processed'].dropna().unique(), 
            key=len, reverse=True
        )[:10]

        comments_df = pd.DataFrame({
            "STT": list(range(1, len(sorted_comments) + 1)),
            "Bình luận": sorted_comments
        })


        # Hiển thị bảng mà không có cột index thừa
        st.dataframe(comments_df, use_container_width=True, hide_index=True)
    else:
        st.info("Không tìm thấy cột `comment_processed` trong dữ liệu.")

