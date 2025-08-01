import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# Read data from csv file
df = pd.read_csv("danhsach_due_cleaned_p2.csv", sep=';')

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('due.jpg')

col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image(image, width=180)  # Điều chỉnh width ở đây để logo lớn hơn, chẳng hạn width=200

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding: 20px 5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">KẾT QUẢ KHẢO SÁT HỌC PHẦN HỌC KỲ I NĂM HỌC 2024-2025</h1></center>"""
with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(html_title, unsafe_allow_html=True)


# Thêm cột cho thông tin Last updated
# col3, col4, col5, col6 = st.columns([0.2, 0.45, 0.45, 0.45])
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
# col4, col5, col6 = st.columns([0.45, 0.45, 0.45])

# total_students = df['Stu_id'].nunique()
# total_teachers = df['Teacher_name'].nunique()
# total_subjects = df['Subject_name'].nunique()

# # Thêm các box thông tin tổng quát
# with col4:
#     st.markdown(f"""
#         <div style='text-align: center; font-size: 32px;'>
#             👨‍🎓<br><strong>{total_students}</strong><br><span style='font-size:24px'>Số sinh viên</span>
#         </div>
#     """, unsafe_allow_html=True)

# with col5:
#     st.markdown(f"""
#         <div style='text-align: center; font-size: 32px;'>
#             👩‍🏫<br><strong>{total_teachers}</strong><br><span style='font-size:24px'>Số giảng viên</span>
#         </div>
#     """, unsafe_allow_html=True)

# with col6:
#     st.markdown(f"""
#         <div style='text-align: center; font-size: 32px;'>
#             📚<br><strong>{total_subjects}</strong><br><span style='font-size:24px'>Số môn học</span>
#         </div>
#     """, unsafe_allow_html=True)

####################
# filtered_data = df[(df['Teacher_name'] == selected_teacher) & 
#                    (df['Subject_name'] == selected_subject)]

# Tạo danh sách các câu hỏi (Q1 đến Q12)

q_cols = [f'Q{i}' for i in range(1, 13)]
result_list = []

if not filtered_data.empty:
    # Lấy tổng số câu từ câu hỏi đầu tiên Q1
    total_count_q1 = filtered_data['Q1'].count()

    for q in q_cols:
        avg_score = filtered_data[q].mean()
        std_score = filtered_data[q].std()

        # Trung bình các lớp cùng học phần
        if selected_subjects and 'Tất cả' not in selected_subjects:
            subject_data = df[df['Subject_name'].isin(selected_subjects)]
        else:
            subject_data = df.copy()
        avg_class_hp = subject_data[q].mean()

        # Trung bình toàn trường
        avg_score_all = df[q].mean()

        result_list.append([
            q, round(avg_score, 2), round(std_score, 2),
            round(avg_class_hp, 2), round(avg_score_all, 2), total_count_q1
        ])

    # Tạo DataFrame kết quả
    result_df = pd.DataFrame(result_list, columns=[
        'Câu hỏi', 'Đánh giá trung bình', 'Độ lệch chuẩn',
        'TB các lớp của cùng HP', 'TB toàn trường', 'Tổng số câu'
    ])

    # Ánh xạ nội dung câu hỏi
    question_labels = {
        'Q1': '1.  Giảng viên giới thiệu rõ ràng, đầy đủ về đề cương chi tiết học phần, gồm: chuẩn đầu ra, nội dung, phương pháp dạy - học, phương pháp kiểm tra - đánh giá, tài liệu học tập của học phần',
        'Q2': '2. Nội dung của học phần phù hợp với năng lực của người học',
        'Q3': '3. Phương pháp dạy - học phù hợp với chuẩn đầu ra và nội dung của học phần',
        'Q4': '4. Giảng viên thực hiện đầy đủ kế hoạch dạy - học đã công bố và tuân thủ các quy định trong giảng dạy',
        'Q5': '5. Giảng viên có cập nhật kiến thức mới và thực tế trong bài giảng',
        'Q6': '6. Hoạt động dạy - học khơi gợi đam mê khám phá và giúp phát triển khả năng tự học',
        'Q7': '7. Giảng viên khuyến khích người học chủ động tham gia thảo luận, giải quyết vấn đề trong giờ học',
        'Q8': '8. Giảng viên tận tụy, sẵn sàng giúp đỡ, giải đáp thỏa đáng các thắc mắc của người học',
        'Q9': '9. Giảng viên sử dụng hiệu quả Elearning và các phương tiện công nghệ trong tổ chức dạy học',
        'Q10': '10. Phương pháp kiểm tra, đánh giá phù hợp với chuẩn đầu ra và nội dung của học phần',
        'Q11': '11. Việc đánh giá được thực hiện công bằng, khách quan và đảm bảo độ tin cậy',
        'Q12': '12. Anh/Chị hài lòng về chất lượng và hiệu quả giảng dạy của giảng viên đối với sự tiến bộ trong học tập của bản thân'
    }
    result_df['Câu hỏi'] = result_df['Câu hỏi'].map(question_labels)

    # Tính trung bình toàn bảng cho các cột số
    avg_overall = {
        'Câu hỏi': 'Trung bình chung',
        'Đánh giá trung bình': round(result_df['Đánh giá trung bình'].mean(), 2),
        'Độ lệch chuẩn': '',
        'TB các lớp của cùng HP': round(result_df['TB các lớp của cùng HP'].mean(), 2),
        'TB toàn trường': round(result_df['TB toàn trường'].mean(), 2),
        'Tổng số câu': ''  # ✅ Không tính trung bình, để trống
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
# Lựa chọn top N (kèm "Tất cả")
top_n_options = ['Tất cả', 3, 5, 7, 10, 15, 20]
selected_top = st.selectbox("📌 Chọn số giảng viên có điểm đánh giá trung bình cao nhất:", top_n_options, index=1)

# Kiểm tra dữ liệu
if not df.empty:
    # Tính điểm trung bình các câu hỏi theo từng giảng viên
    teacher_scores = (
        df.groupby('Teacher_name')[q_cols]
        .mean()
        .mean(axis=1)
        .reset_index(name='Điểm trung bình')
    )

    # Làm tròn điểm
    teacher_scores['Điểm trung bình'] = teacher_scores['Điểm trung bình'].round(2)

    # Thêm cột Đơn vị (khoa)
    # Lấy thông tin duy nhất giữa Teacher_name và Đơn vị
    teacher_units = df[['Teacher_name', 'Đơn vị']].drop_duplicates()

    # Gộp với bảng điểm trung bình
    teacher_scores = teacher_scores.merge(teacher_units, on='Teacher_name', how='left')

    # Sắp xếp theo điểm giảm dần
    teacher_scores = teacher_scores.sort_values(by='Điểm trung bình', ascending=False)

    # Lọc theo top N nếu không phải "Tất cả"
    if selected_top != 'Tất cả':
        teacher_scores = teacher_scores.head(selected_top)

    # Đổi thứ tự cột: Teacher_name, Đơn vị, Điểm trung bình
    teacher_scores = teacher_scores[['Teacher_name', 'Đơn vị', 'Điểm trung bình']]

    # # Hiển thị kết quả
    # title = f"🎓 **Top {selected_top} giảng viên có điểm đánh giá trung bình cao nhất:**" if selected_top != 'Tất cả' else "🎓 **Danh sách toàn bộ giảng viên theo thứ tự điểm đánh giá:**"
    # st.markdown(title)
    # st.dataframe(teacher_scores.reset_index(drop=True), use_container_width=True)

else:
    st.warning("Không có dữ liệu giảng viên để hiển thị.")

import matplotlib.pyplot as plt

# Hiển thị tiêu đề
title = f"🎓 **Top {selected_top} giảng viên có điểm đánh giá trung bình cao nhất:**" if selected_top != 'Tất cả' else "🎓 **Danh sách toàn bộ giảng viên theo thứ tự điểm đánh giá:**"
st.markdown(title)

# Chia bố cục cột cân bằng
col1, col2 = st.columns(2)

with col1:
    st.dataframe(teacher_scores.reset_index(drop=True), use_container_width=True)

with col2:
    st.markdown("📊 **Phân phối điểm trung bình**")
    fig, ax = plt.subplots(figsize=(5, 3.5))  # Tăng nhẹ kích thước để phù hợp
    ax.hist(teacher_scores['Điểm trung bình'], bins=15, color='#1f77b4', edgecolor='black')
    
    # Cài đặt font nhỏ
    ax.set_xlabel('Điểm trung bình', fontsize=10)
    ax.set_ylabel('Số giảng viên', fontsize=10)
    ax.set_title('Biểu đồ histogram', fontsize=11)
    ax.tick_params(axis='both', labelsize=9)

    # Tuỳ chỉnh tick (tuỳ thuộc dữ liệu)
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))  # Tối đa 10 tick trên trục x

    st.pyplot(fig)



# Tạo 2 cột cạnh nhau
# chart_col, comment_col = st.columns(2)

# ==== CỘT BIỂU ĐỒ CẢM XÚC ====
# with chart_col:
#     st.markdown("### 😊 Nhận xét đánh giá ")

#     if 'sentiment' in filtered_data.columns:
#         sentiment_counts = Counter({'Positive': 0, 'Neutral': 0, 'Negative': 0})
#         sentiment_counts.update(filtered_data['sentiment'].dropna())

#         labels = ['Positive', 'Neutral', 'Negative']
#         values = [sentiment_counts[label] for label in labels]
#         colors = ['green', 'gray', 'red']

#         fig = go.Figure(data=[go.Bar(
#             x=labels,
#             y=values,
#             marker_color=colors,
#             text=values,
#             textposition='outside'
#         )])

#         fig.update_layout(
#             title=f'Phân bố cảm xúc - {selected_teachers} - {selected_subjects}',
#             xaxis_title='Cảm xúc',
#             yaxis_title='Số lượng',
#             yaxis=dict(range=[0, max(values)+10000]),
#             height=500
#         )
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("Không tìm thấy cột `sentiment` trong dữ liệu.")

# ==== CỘT TOP 10 BÌNH LUẬN ====
# with comment_col:
#     st.markdown("### 📝 Những bình luận nổi bật")

#     if 'comment_processed' in final_filtered_df.columns:
#         sorted_comments = sorted(
#             final_filtered_df['comment_processed'].dropna().unique(), 
#             key=len, reverse=True
#         )

#         comments_df = pd.DataFrame({
#             "STT": list(range(1, len(sorted_comments) + 1)),
#             "Bình luận": sorted_comments
#         })

#         st.dataframe(comments_df, use_container_width=True, hide_index=True)
#     else:
#         st.info("Không tìm thấy cột `comment_processed` trong dữ liệu.")

st.markdown("### 📝 Những bình luận nổi bật")

if 'comment_processed' in final_filtered_df.columns:
    sorted_comments = sorted(
        final_filtered_df['comment_processed'].dropna().unique(), 
        key=len, reverse=True
    )

    comments_df = pd.DataFrame({
        "STT": list(range(1, len(sorted_comments) + 1)),
        "Bình luận": sorted_comments
    })

    st.dataframe(comments_df, use_container_width=True, hide_index=True)
else:
    st.info("Không tìm thấy cột `comment_processed` trong dữ liệu.")

#######Xuất excel
import io
def generate_excel_file(evaluation_df, comments_df,
                        selected_khoa, selected_teachers,
                        selected_subjects, selected_classes):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Ghi sheet "Báo cáo"
        sheet_name = "Báo cáo"
        worksheet = writer.book.add_worksheet(sheet_name)
        writer.sheets[sheet_name] = worksheet

        # Tiêu đề lớn
        title_format = workbook.add_format({'bold': True, 'font_size': 16})
        worksheet.write("A1", "📊 KẾT QUẢ KHẢO SÁT HỌC PHẦN HỌC KỲ I NĂM HỌC 2024-2025", title_format)

        # Thông tin bộ lọc
        info_format = workbook.add_format({'italic': True})
        worksheet.write("A3", f"Đơn vị: {', '.join(selected_khoa) if selected_khoa else 'Tất cả'}", info_format)
        worksheet.write("A4", f"Giảng viên: {', '.join(selected_teachers) if selected_teachers else 'Tất cả'}", info_format)
        worksheet.write("A5", f"Môn học: {', '.join(selected_subjects) if selected_subjects else 'Tất cả'}", info_format)
        worksheet.write("A6", f"Lớp học: {', '.join(selected_classes) if selected_classes else 'Tất cả'}", info_format)

        # --- Ghi bảng kết quả đánh giá bắt đầu từ dòng 8 ---
        startrow_eval = 7  # (vì dòng 1-6 đã dùng)
        evaluation_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow_eval)

        # --- Ghi bảng bình luận nổi bật cách ra sau ---
        startrow_comment = startrow_eval + len(evaluation_df) + 4
        worksheet.write(startrow_comment - 1, 0, "📝 BÌNH LUẬN NỔI BẬT", title_format)
        comments_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=startrow_comment)

    output.seek(0)
    return output


# Tạo nút xuất file Excel
if not result_df.empty and not comments_df.empty:
    excel_data = generate_excel_file(
        result_df,
        comments_df,
        selected_khoa,
        selected_teachers,
        selected_subjects,
        selected_classes
    )

    st.download_button(
        label="📥 Tải xuống báo cáo (.xlsx)",
        data=excel_data,
        file_name='bao_cao_danh_gia.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

#### xuất excel toàn bộ
import os
import io
import zipfile
import tempfile
import pandas as pd
import xlsxwriter
import streamlit as st

def generate_all_reports_zip(df):
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "BaoCaoTong.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for don_vi in df['Đơn vị'].dropna().unique():
            df_khoa = df[df['Đơn vị'] == don_vi]
            for gv in df_khoa['Teacher_name'].dropna().unique():
                df_gv = df_khoa[df_khoa['Teacher_name'] == gv]
                for mon in df_gv['Subject_name'].dropna().unique():
                    df_mon = df_gv[df_gv['Subject_name'] == mon]
                    class_codes = df_mon['Class_code'].dropna().unique()

                    file_buffer = io.BytesIO()
                    with pd.ExcelWriter(file_buffer, engine='xlsxwriter') as writer:
                        workbook = writer.book

                        for class_code in class_codes:
                            df_lop = df_mon[df_mon['Class_code'] == class_code]
                            sheet_name = str(class_code)[:31]  # Giới hạn 31 ký tự cho tên sheet

                            # --- Tạo bảng kết quả đánh giá ---
                            q_cols = [f'Q{i}' for i in range(1, 13)]
                            total_count = df_lop['Q1'].count()
                            result_list = []

                            for q in q_cols:
                                avg_score = df_lop[q].mean()
                                std_score = df_lop[q].std()
                                avg_class_hp = df_mon[q].mean()
                                avg_score_all = df[q].mean()
                                # total_count = df_lop[q].count()

                                result_list.append([
                                    q, round(avg_score, 2), round(std_score, 2),
                                    round(avg_class_hp, 2), round(avg_score_all, 2), total_count
                                ])

                            evaluation_df = pd.DataFrame(result_list, columns=[
                                'Câu hỏi', 'Đánh giá trung bình', 'Độ lệch chuẩn',
                                'TB các lớp của cùng HP', 'TB toàn trường', 'Tổng số câu'
                            ])

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
                                'Q10': '10. Phương pháp kiểm tra, đánh giá phù hợp với chuẩn đầu ra và nội dung của học phần',
                                'Q11': '11. Việc đánh giá được thực hiện công bằng, khách quan và đảm bảo độ tin cậy',
                                'Q12': '12. Anh/Chị hài lòng về chất lượng và hiệu quả giảng dạy của giảng viên đối với sự tiến bộ trong học tập của bản thân'
                            }
                            evaluation_df['Câu hỏi'] = evaluation_df['Câu hỏi'].map(question_labels)

                            avg_row = {
                                'Câu hỏi': 'Trung bình chung',
                                'Đánh giá trung bình': round(evaluation_df['Đánh giá trung bình'].mean(), 2),
                                'Độ lệch chuẩn': '',
                                'TB các lớp của cùng HP': round(evaluation_df['TB các lớp của cùng HP'].mean(), 2),
                                'TB toàn trường': round(evaluation_df['TB toàn trường'].mean(), 2),
                                'Tổng số câu': ''
                            }

                            evaluation_df = pd.concat([evaluation_df, pd.DataFrame([avg_row])], ignore_index=True)

                            # --- Tạo bảng bình luận ---
                            if 'comment_processed' in df_lop.columns:
                                sorted_comments = sorted(
                                    df_lop['comment_processed'].dropna().unique(),
                                    key=len, reverse=True
                                )
                                comments_df = pd.DataFrame({
                                    "STT": list(range(1, len(sorted_comments) + 1)),
                                    "Bình luận": sorted_comments
                                })
                            else:
                                comments_df = pd.DataFrame(columns=["STT", "Bình luận"])

                            # --- Ghi sheet ---
                            worksheet = workbook.add_worksheet(sheet_name)
                            writer.sheets[sheet_name] = worksheet

                            title_format = workbook.add_format({'bold': True, 'font_size': 14})
                            info_format = workbook.add_format({'italic': True})

                            worksheet.write("A1", "📊 KẾT QUẢ KHẢO SÁT HỌC PHẦN HỌC KỲ I NĂM HỌC 2024-2025", title_format)
                            worksheet.write("A2", f"Đơn vị: {don_vi}", info_format)
                            worksheet.write("A3", f"Giảng viên: {gv}", info_format)
                            worksheet.write("A4", f"Môn học: {mon}", info_format)
                            worksheet.write("A5", f"Lớp học: {class_code}", info_format)

                            evaluation_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=7)
                            comments_df.to_excel(writer, sheet_name=sheet_name, index=False,
                                                 startrow=8 + len(evaluation_df) + 2)

                    file_buffer.seek(0)
                    folder_path = f"{don_vi}/{gv}"
                    file_name = f"{mon}.xlsx"
                    zipf.writestr(f"{folder_path}/{file_name}", file_buffer.read())

    with open(zip_path, "rb") as f:
        return f.read()


# Gọi trong Streamlit
if st.button("📦 Tải xuống tất cả báo cáo"):
    with st.spinner("⏳ Đang tạo báo cáo tổng hợp..."):
        zip_data = generate_all_reports_zip(df)
        st.download_button(
            label="⬇️ Tải toàn bộ báo cáo (.zip)",
            data=zip_data,
            file_name="BaoCaoTong.zip",
            mime="application/zip"
        )
