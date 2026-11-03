import streamlit as st

# 1. Cấu hình trang Dashboard
st.set_page_config(page_title="Smart Pay Advisor", page_icon="🏦", layout="wide")

# 2. Thanh bên (Sidebar) để thu thập dữ liệu
st.sidebar.header("⚙️ Hồ sơ Giao dịch")
amount = st.sidebar.number_input("Số tiền thanh toán (VNĐ):", min_value=10000, value=500000, step=50000)
category = st.sidebar.selectbox("Danh mục chi tiêu:", ["Siêu thị & Tạp hóa", "Du lịch & Khách sạn", "Mua sắm Online (Shopee, Tiktok)", "Thanh toán Hóa đơn"])
user_cards = st.sidebar.multiselect("Công cụ đang có:", ["Thẻ tín dụng (Credit)", "Thẻ ghi nợ (ATM)", "Ví điện tử (MoMo/ZaloPay)"])

# 3. Giao diện chính
st.title("🏦 Smart Pay: Thuật toán Tối ưu Thanh toán")
st.markdown("Hệ thống tự động đối chiếu giao dịch với các chính sách thẻ/ví để tối đa hóa lợi ích tài chính.")

# 4. Hàm Logic (Robo-Advisor Engine)
def analyze_payment(amount, category, cards):
    advice = {"method": "", "reason": "", "saving": 0, "action": ""}
    
    if amount >= 20000000:
        advice["method"] = "Chuyển khoản (VietQR)"
        advice["reason"] = "Với giao dịch lớn, quẹt thẻ có thể bị cửa hàng thu phụ phí ẩn 1.5% - 2%. Chuyển khoản giúp bảo toàn dòng tiền."
        advice["saving"] = amount * 0.015
        advice["action"] = "Sử dụng App ngân hàng quét mã VietQR."
        
    elif category == "Mua sắm Online (Shopee, Tiktok)":
        if "Ví điện tử (MoMo/ZaloPay)" in cards:
            advice["method"] = "Ví điện tử liên kết Thẻ"
            advice["reason"] = "Các sàn TMĐT thường trợ giá phí ship và tung voucher 30k-50k khi thanh toán qua ví đối tác."
            advice["saving"] = 50000
            advice["action"] = "Áp dụng mã giảm giá của Ví tại bước Checkout."
        else:
            advice["method"] = "Thanh toán khi nhận hàng (COD) hoặc Thẻ ATM"
            advice["reason"] = "Bạn đang bỏ lỡ ưu đãi. Nên mở Ví điện tử để tối ưu chi tiêu online."
            advice["saving"] = 0
            advice["action"] = "Chọn phương thức thanh toán an toàn, không tốn phí."
            
    elif category == "Du lịch & Khách sạn":
        if "Thẻ tín dụng (Credit)" in cards:
            advice["method"] = "Thẻ tín dụng Du lịch (Travel/Miles Card)"
            advice["reason"] = "Thanh toán vé máy bay/khách sạn qua thẻ thường được nhân 3 dặm thưởng, kèm bảo hiểm trễ chuyến miễn phí."
            advice["saving"] = amount * 0.05
            advice["action"] = "Dùng thẻ tín dụng thanh toán trên Agoda/Traveloka."
        else:
            advice["method"] = "Chuyển khoản"
            advice["reason"] = "Giao dịch an toàn, không rủi ro lộ thông tin."
            advice["saving"] = 0
            advice["action"] = "Chuyển tiền trực tiếp cho hãng bay/khách sạn."
            
    elif category == "Siêu thị & Tạp hóa":
        if "Thẻ tín dụng (Credit)" in cards:
            advice["method"] = "Thẻ tín dụng Hoàn tiền (Cashback)"
            advice["reason"] = "Các dòng thẻ Cashback (như VPBank StepUp, VIB Super Card) hoàn từ 5% - 10% tại siêu thị."
            advice["saving"] = amount * 0.08
            advice["action"] = "Quẹt thẻ vật lý hoặc Apple Pay tại máy POS."
        else:
            advice["method"] = "Quét mã VNPAY-QR"
            advice["reason"] = "Thường có mã giảm 10k-20k cho hóa đơn siêu thị."
            advice["saving"] = 15000
            advice["action"] = "Mở app ngân hàng quét mã QR tại quầy."
            
    else:
         advice["method"] = "Ví điện tử"
         advice["reason"] = "Nhận xu hoàn hoặc tích điểm thành viên."
         advice["saving"] = amount * 0.01
         advice["action"] = "Thanh toán bằng số dư ví."
         
    return advice

# 5. Xử lý sự kiện khi bấm nút
if st.sidebar.button("🚀 Kích hoạt Phân tích", use_container_width=True):
    if not user_cards:
        st.warning("⚠️ Cảnh báo: Vui lòng chọn ít nhất 1 loại Thẻ/Ví ở menu bên trái để thuật toán có dữ liệu xử lý.")
    else:
        with st.spinner("Đang chạy mô hình so sánh lợi ích..."):
            result = analyze_payment(amount, category, user_cards)
            
            # Hiển thị UI chia cột
            st.markdown("---")
            col1, col2 = st.columns([2.5, 1])
            
            with col1:
                st.success(f"🌟 **Khuyên dùng:** {result['method']}")
                st.info(f"💡 **Cơ sở phân tích:** {result['reason']}")
                
            with col2:
                st.metric(label="💰 Ước tính Sinh lời / Tiết kiệm", value=f"{int(result['saving']):,} ₫".replace(",", "."))
            
            with st.expander("🛠️ Xem hướng dẫn thao tác chi tiết", expanded=True):
                st.write(result['action'])
                st.progress(100)
