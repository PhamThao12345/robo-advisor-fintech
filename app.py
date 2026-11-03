import streamlit as st
import time

# 1. Cấu hình trang cơ bản (Mở rộng toàn màn hình)
st.set_page_config(page_title="SmartPay Robo-Advisor", layout="wide", page_icon="💳", initial_sidebar_state="expanded")

# 2. Tiêm CSS tùy chỉnh để làm đẹp UI/UX (Màu sắc, bo góc thẻ, đổ bóng)
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; color: #1E3A8A; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #64748B; text-align: center; margin-bottom: 30px; }
    .card { background-color: #F8FAFC; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-left: 5px solid #3B82F6; margin-bottom: 20px; }
    .card-success { border-left-color: #10B981; background-color: #ECFDF5; }
    .card-warning { border-left-color: #F59E0B; background-color: #FFFBEB; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💳 SmartPay Robo-Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Hệ thống phân tích và định tuyến thanh toán đa kênh thông minh</div>', unsafe_allow_html=True)

# 3. SIDEBAR: Tùy chỉnh hồ sơ ví tiền của người dùng
with st.sidebar:
    st.markdown("### 👤 Hồ Sơ Khách Hàng")
    user_type = st.select_slider("Phong cách chi tiêu:", options=["Tiết kiệm", "Cân bằng", "Tận hưởng"], value="Cân bằng")
    
    st.markdown("**💰 Ví tiền & Thẻ hiện có:**")
    has_cash = st.checkbox("Tiền mặt (Cash)", value=True)
    has_banking = st.checkbox("App Ngân hàng (VietQR)", value=True)
    wallets = st.multiselect("Ví điện tử & Công nghệ:", ["MoMo", "ZaloPay", "ShopeePay", "Apple Pay / Google Pay"], default=["MoMo", "Apple Pay / Google Pay"])
    cards = st.multiselect("Thẻ Tín dụng / Ghi nợ:", ["VIB Super Card", "VPBank StepUp", "Thẻ Ghi nợ (ATM)"], default=["Thẻ Ghi nợ (ATM)"])

# 4. KHU VỰC CHÍNH: Phân chia Tabs để tránh rối mắt
tab1, tab2 = st.tabs(["💡 Tư vấn Giao dịch", "📊 Bảng phân tích Phí"])

with tab1:
    st.markdown("### 🛒 Hoàn cảnh Giao dịch")
    with st.form("transaction_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            amount = st.number_input("Số tiền (VNĐ):", min_value=1000, step=10000, value=35000)
        with col2:
            category = st.selectbox("Mục đích chi tiêu:", ["Ăn uống/Cà phê", "Siêu thị/Tạp hóa", "Mua sắm Online", "Đổ xăng/Gửi xe", "Chuyển tiền trả nợ"])
        with col3:
            merchant_type = st.selectbox("Điểm bán hàng (Merchant):", ["Vỉa hè/Chợ truyền thống", "Cửa hàng tiện lợi", "Chuỗi thương hiệu lớn", "Sàn TMĐT/App"])
        
        submitted = st.form_submit_button("🧠 Phân Tích Phương Án Tối Ưu")

    if submitted:
        with st.spinner("Đang phân tích điều kiện môi trường và biểu phí..."):
            time.sleep(1) # Giả lập thời gian load API
            
            primary = ""
            alt = "Không có"
            reason = ""
            saved = 0
            
            # THUẬT TOÁN LOGIC (Decision Tree)
            # Tình huống 1: Vỉa hè/Chợ truyền thống, tiền lẻ
            if merchant_type == "Vỉa hè/Chợ truyền thống" and amount <= 50000:
                primary = "💵 Tiền mặt (Cash)" if has_cash else "🏦 Quét mã QR cá nhân"
                alt = "🏦 Quét mã QR cá nhân" if has_banking and has_cash else "💵 Tiền mặt"
                reason = "Giao dịch quá nhỏ. Tiểu thương ở chợ/vỉa hè thao tác nhanh nhất với tiền mặt, không lo nghẽn mạng VietQR hoặc phải kiểm tra app."
            
            # Tình huống 2: Đổ xăng, gửi xe (Cần tốc độ cực cao)
            elif category == "Đổ xăng/Gửi xe":
                if has_cash:
                    primary = "💵 Tiền mặt (Cash)"
                    alt = "🏦 Quét VietQR" if has_banking else "Không có"
                    reason = "Tại cây xăng, thao tác rút điện thoại quét QR thường bất tiện và chậm hơn đưa tiền mặt chẵn."
            
            # Tình huống 3: Số tiền lớn hoặc chuyển nợ
            elif category == "Chuyển tiền trả nợ" or amount >= 10000000:
                primary = "🏦 Chuyển khoản NAPAS 24/7 (VietQR)"
                reason = "Miễn phí hoàn toàn. Tránh rủi ro mang vác tiền mặt lớn, không bị tính phí quẹt thẻ (MDR)."
                saved = amount * 0.02 
            
            # Tình huống 4: Chuỗi lớn / Cửa hàng tiện lợi (Hỗ trợ Contactless)
            elif merchant_type in ["Chuỗi thương hiệu lớn", "Cửa hàng tiện lợi"]:
                if "Apple Pay / Google Pay" in wallets:
                    primary = "📲 Apple Pay / Google Pay (Chạm NFC)"
                    alt = "💳 Quẹt Thẻ / Chạm Thẻ"
                    reason = "Tốc độ thanh toán 1-2 giây, bảo mật cao nhất qua Tokenization, không cần mở app hay mạng internet."
                elif len(cards) > 0:
                    primary = "💳 Chạm Thẻ (Contactless)"
                    alt = "📱 Quét mã VNPay / MoMo"
                    reason = "Nhanh gọn, có cơ hội tích điểm/hoàn tiền từ thẻ tín dụng."
                    saved = amount * 0.02
            
            # Tình huống 5: Online / TMĐT
            elif merchant_type == "Sàn TMĐT/App":
                if "ShopeePay" in wallets:
                    primary = "📱 Ví ShopeePay / MoMo"
                    reason = "Tối ưu hóa các mã Freeship và Voucher giảm giá độc quyền của sàn."
                    saved = min(amount * 0.1, 50000)
                elif "VIB Super Card" in cards:
                    primary = "💳 Thẻ tín dụng VIB Super Card"
                    reason = "Tối đa hóa lợi nhuận với mức hoàn tiền 15% cho giao dịch online."
                    saved = min(amount * 0.15, 500000)
            
            # Mặc định
            if not primary:
                primary = "🏦 App Ngân hàng (Quét VietQR)"
                alt = "💵 Tiền mặt" if has_cash else "Không có"
                reason = "Phương thức quốc dân, dễ đối soát quản lý chi tiêu."

            # HIỂN THỊ KẾT QUẢ UX/UI CAO CẤP
            st.markdown("### 🏆 Quyết định Định tuyến")
            st.markdown(f"""
            <div class="card card-success">
                <h4 style="margin-top: 0; color: #047857;">🥇 Khuyên dùng: {primary}</h4>
                <p style="margin-bottom: 0;"><b>Lý do:</b> {reason}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.markdown(f"""
                <div class="card card-warning">
                    <h5 style="margin-top: 0; color: #B45309;">🥈 Phương án dự phòng</h5>
                    <p style="margin-bottom: 0;">{alt}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_res2:
                st.markdown(f"""
                <div class="card">
                    <h5 style="margin-top: 0; color: #1D4ED8;">💰 Ước tính Lợi ích / Tiết kiệm</h5>
                    <h3 style="margin: 0; color: #10B981;">+{int(saved):,} VNĐ</h3>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📈 Bảng Đối soát Thuộc tính Thanh toán")
    st.table({
        "Phương thức": ["Tiền mặt", "VietQR (Chuyển khoản)", "Ví Điện Tử (MoMo/VNPAY)", "Thẻ Tín Dụng (POS)", "Apple Pay / Google Pay"],
        "Phí Người Dùng": ["0đ", "0đ", "0đ", "0đ (Trừ rút tiền)", "0đ"],
        "Phí Cửa Hàng (MDR)": ["0đ", "0đ", "0.5% - 1.5%", "1.5% - 2.5%", "Bằng phí thẻ liên kết"],
        "Tốc độ giao dịch": ["Chậm (Chờ thối tiền)", "Trung bình (Mở app, quét)", "Trung bình", "Nhanh (Chạm)", "Cực nhanh (1 giây)"],
        "Phạm vi sử dụng": ["Mọi nơi", "Hầu hết mọi nơi", "SME, Chuỗi lớn", "Chuỗi, Siêu thị", "Chuỗi lớn (Có máy POS hỗ trợ NFC)"]
    })
