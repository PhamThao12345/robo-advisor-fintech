import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. CẤU HÌNH UI & CSS TÙY CHỈNH
st.set_page_config(page_title="Smart Payment Routing", layout="wide", page_icon="🏦")
st.markdown("""
    <style>
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #1E3A8A; box-shadow: 1px 1px 5px rgba(0,0,0,0.05); }
    .big-font { font-size:20px !important; font-weight: 600; color: #1E3A8A; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #0f3460;'>🏦 Enterprise Robo-Advisor: Smart Routing Engine</h2>", unsafe_allow_html=True)
st.markdown("---")

# 2. BỐ CỤC ĐA TAB TỐI ƯU UX
tab1, tab2 = st.tabs(["💳 Cửa sổ Giao dịch (Front-end)", "⚙️ Tham số Thuật toán (Back-end)"])

with tab1:
    st.markdown('<p class="big-font">Nhập thông số giao dịch</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        amount = st.number_input("Giá trị (VND):", min_value=5000, step=50000, value=35000)
    with col2:
        merchant_tier = st.selectbox("Điểm bán (Merchant):", ["Chợ truyền thống/Vỉa hè", "Cửa hàng tiện lợi", "Siêu thị/TTTM", "Thương mại điện tử"])
    with col3:
        require_invoice = st.checkbox("Cần xuất hóa đơn điện tử (VAT)?", help="Yêu cầu giao dịch qua ngân hàng để hợp lệ chứng từ thuế doanh nghiệp.")

    if st.button("⚡ Phân tích đa chiều", type="primary", use_container_width=True):
        with st.spinner("Hệ thống đang quét ma trận định tuyến..."):
            time.sleep(1) # Giả lập API call
            
            # 3. LÕI LOGIC (Bao gồm Tiền mặt & Thuế)
            if require_invoice and amount >= 20000000:
                primary = "Chuyển khoản Doanh nghiệp (UNC)"
                reason = "Bắt buộc thanh toán không dùng tiền mặt để hợp lệ chi phí thuế theo quy định về Hóa đơn điện tử."
                cashback = 0
            elif merchant_tier == "Chợ truyền thống/Vỉa hè":
                if amount <= 50000:
                    primary = "💵 Tiền mặt"
                    reason = "Tốc độ nhanh nhất, không phụ thuộc kết nối mạng mạng. Điểm bán siêu nhỏ thường không sẵn sàng mã QR."
                    cashback = 0
                else:
                    primary = "📱 Mã VietQR Cá nhân"
                    reason = "Hạn chế mang tiền mặt mệnh giá lớn, tiểu thương hiện nay đã phổ cập VietQR."
                    cashback = 0
            elif merchant_tier == "Thương mại điện tử":
                primary = "💳 Thẻ Tín dụng trực tuyến"
                reason = "Bảo vệ quyền lợi (Chargeback) khi hàng lỗi, tích lũy hoàn tiền lên tới 10%."
                cashback = amount * 0.10
            else:
                primary = "📱 Ví điện tử (Quét VNPAY/MoMo)"
                reason = "Kết hợp thẻ thành viên và voucher giảm giá trực tiếp tại hệ thống máy POS."
                cashback = min(amount * 0.05, 50000)
                
            # 4. HIỂN THỊ KẾT QUẢ TRỰC QUAN
            st.success(f"✅ Khuyến nghị phương thức ưu tiên: **{primary}**")
            st.info(f"💡 Cơ sở ra quyết định: {reason}")
            
            if cashback > 0:
                st.metric(label="Giá trị hoàn tiền/Giảm giá ước tính", value=f"+{int(cashback):,} ₫")

            st.markdown("---")
            # 5. BIỂU ĐỒ RADAR TƯƠNG TÁC BẰNG PLOTLY
            st.markdown('<p class="big-font">📊 Phân tích chấm điểm đa phương thức</p>', unsafe_allow_html=True)
            
            # Tạo DataFrame linh động theo kịch bản
            cash_accept = 10 if merchant_tier == "Chợ truyền thống/Vỉa hè" else 5
            card_accept = 1 if merchant_tier == "Chợ truyền thống/Vỉa hè" else 9
            
            df_scores = pd.DataFrame({
                "Tiêu chí": ["Tốc độ", "Chi phí giao dịch", "Bảo mật rủi ro", "Khả năng sinh lời", "Mức độ chấp nhận"],
                "Tiền mặt": [9, 10, 3, 1, cash_accept],
                "Chuyển khoản": [7, 10, 9, 2, 8],
                "Thẻ Tín dụng": [8, 6, 9, 10, card_accept]
            })
            
            # Chuyển đổi dữ liệu để vẽ biểu đồ Radar
            df_melt = df_scores.melt(id_vars=["Tiêu chí"], var_name="Phương thức", value_name="Điểm (1-10)")
            fig = px.line_polar(df_melt, r='Điểm (1-10)', theta='Tiêu chí', color='Phương thức', 
                                line_close=True, markers=True, color_discrete_sequence=["#2ca02c", "#1f77b4", "#ff7f0e"])
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), margin=dict(l=40, r=40, t=20, b=20))
            
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.write("Bảng tham chiếu trọng số quyết định (Decision Matrix). Cập nhật theo thời gian thực từ Database.")
    df_admin = pd.DataFrame({
        "Biến số": ["Hệ số rủi ro tiền mặt", "Trần phí MDR Thẻ", "Tỷ lệ gián đoạn mạng"],
        "Giá trị hiện tại": [0.85, "1.5% - 2.5%", "0.01%"]
    })
    st.dataframe(df_admin, use_container_width=True)
