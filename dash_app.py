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


# ---------- Hàm lọc dữ liệu ----------
def get_filtered_df(khoa, teacher, subject, class_code):
    filtered = df.copy()

    if khoa and 'Tất cả' not in khoa:
        filtered = filtered[filtered['Đơn vị'].isin(khoa)]

    if teacher and 'Tất cả' not in teacher:
        filtered = filtered[filtered['Teacher_name'].isin(teacher)]

    if subject and 'Tất cả' not in subject:
        filtered = filtered[filtered['Subject_name'].isin(subject)]

    if class_code and 'Tất cả' not in class_code:
        filtered = filtered[filtered['Class_code'].isin(class_code)]

    return filtered

# ---------- Thiết lập session_state mặc định ----------
for key in ['selected_khoa', 'selected_teacher', 'selected_subject', 'selected_class']:
    if key not in st.session_state:
        st.session_state[key] = ['Tất cả']

# ---------- Tính toán dữ liệu đã lọc ----------
filtered_df = get_filtered_df(
    st.session_state['selected_khoa'],
    st.session_state['selected_teacher'],
    st.session_state['selected_subject'],
    st.session_state['selected_class']
)

# ---------- Lấy danh sách chọn lọc từ filtered_df ----------
available_khoa = sorted(filtered_df['Đơn vị'].dropna().unique())
available_teacher = sorted(filtered_df['Teacher_name'].dropna().unique())
available_subject = sorted(filtered_df['Subject_name'].dropna().unique())
available_class = sorted(filtered_df['Class_code'].dropna().unique())

# ---------- Layout theo columns ----------
col3, filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([0.2, 0.3, 0.3, 0.3, 0.3])

with filter_col1:
    st.session_state['selected_khoa'] = st.multiselect(
        'Chọn Khoa (Đơn vị)',
        options=['Tất cả'] + available_khoa,
        default=st.session_state['selected_khoa']
    )

with filter_col2:
    st.session_state['selected_teacher'] = st.multiselect(
        'Chọn Giảng viên',
        options=['Tất cả'] + available_teacher,
        default=st.session_state['selected_teacher']
    )

with filter_col3:
    st.session_state['selected_subject'] = st.multiselect(
        'Chọn Môn học',
        options=['Tất cả'] + available_subject,
        default=st.session_state['selected_subject']
    )

with filter_col4:
    st.session_state['selected_class'] = st.multiselect(
        'Chọn Mã lớp học',
        options=['Tất cả'] + available_class,
        default=st.session_state['selected_class']
    )

# ---------- Tính từng bước để giữ tên biến ----------
filtered_df_khoa = get_filtered_df(st.session_state['selected_khoa'], ['Tất cả'], ['Tất cả'], ['Tất cả'])
filtered_df_teacher = get_filtered_df(st.session_state['selected_khoa'], st.session_state['selected_teacher'], ['Tất cả'], ['Tất cả'])
filtered_df_subject = get_filtered_df(st.session_state['selected_khoa'], st.session_state['selected_teacher'], st.session_state['selected_subject'], ['Tất cả'])
final_filtered_df = get_filtered_df(
    st.session_state['selected_khoa'],
    st.session_state['selected_teacher'],
    st.session_state['selected_subject'],
    st.session_state['selected_class']
)

# ---------- Hiển thị kết quả ----------
# st.write("🔍 **Dữ liệu đã lọc:**")
# st.dataframe(final_filtered_df)


# # (Tuỳ chọn) Hiển thị dữ liệu đã lọc
# st.write("🔍 **Dữ liệu đã lọc:**")
# st.dataframe(final_filtered_df[final_filtered_df['Class_code'] == selected_class])

# Lọc dữ liệu theo giảng viên và môn học đã chọn
filtered_data = final_filtered_df.copy()
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
        'Q1': '1. Giảng viên giới thiệu rõ ràng, đầy đủ về đề cương chi tiết học phần, gồm: chuẩn đầu ra, nội dung, phương pháp dạy - học, phương pháp kiểm tra - đánh giá, tài liệu học tập của học phần',
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

