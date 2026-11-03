import streamlit as st
import time

# Cấu hình trang rộng và tiêu đề
st.set_page_config(page_title="FinTech Robo-Advisor PRO", layout="wide", page_icon="🤖")

# Tiêu đề với CSS tùy chỉnh
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🤖 Hệ Thống Cố Vấn Thanh Toán Cấp Cao</h2>", unsafe_allow_html=True)
st.markdown("---")

# 1. SIDEBAR: Thu thập hồ sơ tài chính (User Profiling)
with st.sidebar:
    st.header("⚙️ Hồ Sơ Người Dùng")
    reward_pref = st.radio("Mục tiêu tối ưu:", ["Tối đa Cashback", "Tích lũy Dặm bay", "Tối giản chi phí"])
    has_cards = st.multiselect("Thẻ đang sở hữu:", ["VIB Super Card", "VPBank StepUp", "Sacombank Platinum", "Thẻ Ghi nợ (ATM)"])
    has_wallets = st.multiselect("Ví điện tử:", ["MoMo", "VNPay", "ZaloPay", "ShopeePay"])

# 2. KHU VỰC CHÍNH: Dữ liệu giao dịch (Transaction Data)
st.subheader("📥 Thông tin giao dịch hiện tại")
col1, col2, col3 = st.columns(3)
with col1:
    amount = st.number_input("Giá trị giao dịch (VND):", min_value=0, step=100000, value=500000)
with col2:
    category = st.selectbox("Danh mục:", ["Siêu thị & Tạp hóa", "Du lịch & Đặt phòng", "Thương mại điện tử", "Ăn uống", "Chuyển tiền cá nhân"])
with col3:
    merchant_tier = st.selectbox("Quy mô Cửa hàng (Merchant):", ["Chuỗi/Doanh nghiệp lớn", "Cửa hàng vừa & nhỏ (SME)", "Cá nhân"])

# 3. LÕI THUẬT TOÁN (Decision Engine)
if st.button("🚀 Kích hoạt Thuật toán Định tuyến", use_container_width=True):
    with st.spinner("Đang chạy mô hình định tuyến (Payment Routing)..."):
        time.sleep(1.2) # Tạo độ trễ giả lập xử lý API
        
        primary_method = ""
        reason = ""
        saved_amount = 0
        
        # Logic xử lý phức tạp
        if amount >= 15000000 or category == "Chuyển tiền cá nhân":
            primary_method = "Chuyển khoản NAPAS 24/7 (Mã VietQR)"
            reason = "Tránh phí quẹt thẻ (MDR) ~2% cho số tiền lớn. Giao dịch thời gian thực (Real-time clearing)."
            saved_amount = amount * 0.02
        elif category == "Du lịch & Đặt phòng" and reward_pref == "Tích lũy Dặm bay":
            primary_method = "Thẻ Tín dụng Sacombank Platinum / VIB Travel Élite"
            reason = "Tối ưu hóa dặm thưởng Bông Sen Vàng, tặng kèm bảo hiểm du lịch toàn cầu."
            saved_amount = amount * 0.015 # Ước tính quy đổi dặm
        elif category == "Thương mại điện tử" and "VIB Super Card" in has_cards:
            primary_method = "Thẻ Tín dụng VIB Super Card"
            reason = "Khớp với thẻ bạn đang có: Kích hoạt mức Hoàn tiền (Cashback) 15% cho mua sắm trực tuyến."
            saved_amount = min(amount * 0.15, 1000000)
        elif merchant_tier == "Cửa hàng vừa & nhỏ (SME)":
            primary_method = "Quét mã VNPay-QR / Ví MoMo"
            reason = "Chấp nhận rộng rãi tại SME, tận dụng ngân sách khuyến mãi (Promotion) từ các ví."
            saved_amount = 15000 
        else:
            primary_method = "Thẻ tín dụng đa năng (VPBank StepUp / HSBC)"
            reason = "Tận dụng 45 ngày không lãi suất, tối ưu hóa vốn lưu động cá nhân và nhận cashback 2% cơ bản."
            saved_amount = amount * 0.02

        # 4. HIỂN THỊ KẾT QUẢ CHUYÊN NGHIỆP
        st.success("✅ Phân tích hoàn tất! Dưới đây là phương án định tuyến tối ưu nhất.")
        
        res_col1, res_col2 = st.columns([2, 1])
        with res_col1:
            st.info(f"**Phương thức đề xuất:** {primary_method}\n\n**Cơ sở ra quyết định:** {reason}")
        with res_col2:
            # Hiển thị số liệu nổi bật bằng st.metric
            st.metric(label="Lợi ích tài chính ước tính", value=f"+{int(saved_amount):,} ₫", delta="Tối ưu")
            
        # Log hệ thống cho dân chuyên nghiệp
        with st.expander("📊 Xem log xử lý hệ thống (Developer View)"):
            st.code(f"""
            {{
                "transaction_class": "{category}",
                "merchant_tier": "{merchant_tier}",
                "user_objective": "{reward_pref}",
                "available_instruments": {has_cards + has_wallets},
                "routing_decision": "{primary_method}",
                "estimated_yield": {saved_amount}
            }}
            """, language="json")
